from setup import csrf, get_db, User, app, flask
from flask_login import current_user, login_required, logout_user, login_user
from queries import q_hd, q_main
from tools import psql_api, tools
import os
import json

hd = flask.Blueprint('hd', 'hd', url_prefix='/hd', template_folder='templates/help_desk')


@hd.route('/home')
def hd_home():
    l_user_tickets = []
    if current_user.is_authenticated:
        db = psql_api.PostgresAPI(get_db())
        db.exec_query(q_hd.get_user_tickets,
                      {'user_id': current_user.id})
        l_user_tickets = db.lod()
        flask.session['prv_page'] = flask.request.path
    return flask.render_template('hd_home.html',
                                 l_user_tickets=l_user_tickets)


@hd.route('/setup-hd-categories', methods=["GET", "POST"])
@login_required
def setup_hd_categories():
    db = psql_api.PostgresAPI(get_db())
    if flask.request.method == 'POST':
        fd = flask.request.form
        db.exec_query(q_hd.ins_ticket_category,
                      {'parent_id': 0 if int(fd['hd_category_level']) == 1 else fd['hd_category_parent_id'],
                       'level': fd['hd_category_level'],
                       'category_name': fd['hd_category_name'],
                       'sla_days': fd['hd_category_sla_days'] if int(fd['hd_category_level']) == 3 else 0}, one=True)
        if int(fd['hd_category_level']) == 3:
            cat3_id = db.lod()['id']
            for ut in fd.getlist('teams-select-list'):
                db.exec_query(q_hd.ins_cat3_teams, {'cat3_id': cat3_id,
                                                    'team_id': ut})
        flask.flash('הסיווג נוסף בהצלחה', 'success')
        return flask.redirect(flask.url_for('hd.setup_hd_categories'))
    db.exec_query(q_hd.get_all_ticket_category)
    category_data = db.lod()
    db.exec_query(q_main.get_all_teams)
    l_teams = db.lod()
    return flask.render_template('setup_category.html',
                                 category_data=category_data,
                                 l_teams=l_teams)


@hd.route('/open-hd-ticket', methods=["GET", "POST"])
@login_required
def open_hd_ticket():
    db = psql_api.PostgresAPI(get_db())
    if flask.request.method == 'POST':
        fd = flask.request.form
        db.exec_query(q_hd.ins_ticket,
                      {'category3id': fd['hd-cat-3'],
                       'assign_cust_id': fd['assign-cust'] if int(fd['assign-cust']) != 0 else current_user.id,
                       'create_by': current_user.id}, one=True)
        ticket_id = db.lod()['ticket_id']
        db.exec_query(q_hd.ins_ticket_note,
                      {'ticket_id': ticket_id, 'ticket_note_id': 1,
                       'note_text': fd['hd_ticket_note'],
                       'create_by': current_user.id})
        for i, file in enumerate(flask.request.files.getlist('hd_ticket_multi_file')):
            if file and tools.allowed_file(file.filename):
                gen_file_name, file_length, mimetype = tools.save_file('hd', file)
                db.exec_query(q_hd.ins_ticket_file,
                              {'ticket_id': ticket_id, 'file_name': file.filename,
                               'gen_file_name': gen_file_name, 'mimetype': mimetype,
                               'file_size': file_length, 'create_by': current_user.id})
        flask.flash('הפניה נפתחה בהצלחה - מספר {}'.format(ticket_id), 'success')
        return flask.redirect(flask.url_for('hd.hd_home'))
    db.exec_query(q_hd.get_1st_cat)
    cat_1_l = db.lod()
    db.exec_query(q_hd.get_user_ticket_assign_data,
                  {'current_user_id': current_user.id})
    assign_user_id_l = db.lod()
    return flask.render_template('open_ticket.html',
                                 cat_1_l=cat_1_l,
                                 assign_user_id_l=assign_user_id_l)


@hd.route('/my-team-ticket', methods=["GET", "POST"])
@login_required
def my_team_ticket():
    db = psql_api.PostgresAPI(get_db())
    db.exec_query(q_hd.get_my_teams_tickets_header,
                  {'user_id': current_user.id})
    l_my_teams_tickets = db.lod()
    flask.session['prv_page'] = flask.request.path
    return flask.render_template('my_team_ticket.html',
                                 l_my_teams_tickets=l_my_teams_tickets)


@hd.route('/ticket', methods=["GET", "POST"])
@login_required
def ticket():
    prv_page = ''
    if 'prv_page' in flask.session.keys():
        prv_page = flask.session['prv_page']
        flask.session.pop('prv_page')
    ticket_id = flask.request.args.get('id', default=None, type=int)
    db = psql_api.PostgresAPI(get_db())
    db.exec_query(q_hd.get_1st_cat)
    cat_1_l = db.lod()
    db.exec_query(q_hd.get_ticket_close_reason)
    close_reason_l = db.lod()
    return flask.render_template('ticket.html',
                                 ticket_id=ticket_id,
                                 cat_1_l=cat_1_l,
                                 close_reason_l=close_reason_l,
                                 prv_page=prv_page)


@hd.route('/_get_ticket_header', methods=['GET'])
@login_required
def get_ticket_header():
    db = psql_api.PostgresAPI(get_db())
    db.exec_query(q_hd.get_ticket_header,
                  {'ticket_id': flask.request.args['ticket_id']},
                  one=True)
    return flask.jsonify(db.lod())


@hd.route('/_set_ticket_header', methods=['POST'])
@login_required
def set_ticket_header():
    db = psql_api.PostgresAPI(get_db())
    fd = flask.request.form
    db.exec_query(q_hd.update_ticket_category, {'category3id': fd['cat_3_id'],
                                                'ticket_id': fd['ticket_id']}, one=True)
    old_category3id = db.lod()
    new_category3id = {'category3id': fd['cat_3_id']}
    note_text = "עדכון סיווג"
    db.exec_query(q_hd.ins_user_ticket_note_log, {'ticket_id': fd['ticket_id'],
                                                  'note_text': note_text,
                                                  'old_data': json.dumps(old_category3id),
                                                  'new_data': json.dumps(new_category3id),
                                                  'create_by': current_user.id})
    return flask.jsonify(None)


@hd.route('/_add_ticket_user_note', methods=['POST'])
@login_required
def add_ticket_user_note():
    db = psql_api.PostgresAPI(get_db())
    fd = flask.request.form
    db.exec_query(q_hd.ins_user_ticket_note, {'ticket_id': fd['ticket_id'],
                                              'ticket_note_type_id': 2,
                                              'note_text': fd['note_text'],
                                              'create_by': current_user.id})
    return flask.jsonify(None)


@hd.route('/_close_ticket', methods=['POST'])
@login_required
def close_ticket():
    db = psql_api.PostgresAPI(get_db())
    fd = flask.request.form
    db.exec_query(q_hd.ins_user_ticket_note, {'ticket_id': fd['ticket_id'],
                                              'ticket_note_type_id': 3,
                                              'note_text': fd['note_text'],
                                              'create_by': current_user.id})
    db.exec_query(q_hd.close_ticket_status, {'close_by': current_user.id,
                                             'close_reason_id': fd['close_reason_id'],
                                             'ticket_id': fd['ticket_id']})
    return flask.jsonify(None)


@hd.route('/_get_ticket_user_notes', methods=['GET'])
@login_required
def get_ticket_user_notes():
    db = psql_api.PostgresAPI(get_db())
    db.exec_query(q_hd.get_ticket_notes,
                  {'ticket_id': flask.request.args['ticket_id']})
    return flask.jsonify(db.lod())


@hd.route('/_get_ticket_user_files', methods=['GET'])
@login_required
def get_ticket_user_files():
    db = psql_api.PostgresAPI(get_db())
    db.exec_query(q_hd.get_ticket_files,
                  {'ticket_id': flask.request.args['ticket_id']})
    return flask.jsonify(db.lod())


@hd.route('/users_files/<gen_file_name>')
@login_required
def download_hd_ticket_file(gen_file_name):
    db = psql_api.PostgresAPI(get_db())
    db.exec_query(q_hd.get_orig_filename,
                  {'gen_file_name': gen_file_name}, one=True)
    full_path = os.path.join(app.config['UPLOAD_FOLDER'], 'hd')
    file_data = db.lod()
    return flask.send_from_directory(full_path,
                                     gen_file_name,
                                     attachment_filename=file_data['file_name'],
                                     as_attachment=True,
                                     mimetype=file_data['mimetype'])


@hd.route('/_update_select_category', methods=['GET'])
@login_required
def update_select_category():
    db = psql_api.PostgresAPI(get_db())
    db.exec_query(q_hd.get_top_ticket_category,
                  {'level': flask.request.args['hd_category_level']})
    return flask.jsonify(db.lod())


@hd.route('/_get_children_category', methods=['GET'])
@login_required
def get_children_category():
    db = psql_api.PostgresAPI(get_db())
    db.exec_query(q_hd.get_children_cat_sql,
                  {'parent_id': flask.request.args['cat_id'],
                   'level': flask.request.args['cat_level']
                   })
    return flask.jsonify(db.lod())


app.register_blueprint(hd)
