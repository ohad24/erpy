from setup import csrf, get_db, User, app, flask
from tools import psql_api
from flask_login import current_user, login_required, logout_user, login_user
from queries import q_hd

hd = flask.Blueprint('hd', 'hd', url_prefix='/hd', template_folder='templates/help_desk')


@hd.route('/home')
def hd_home():
    db = psql_api.PostgresAPI(get_db())
    db.exec_query('select now()', one=True)
    d = db.lod()
    return flask.render_template('hd_home.html', d=d['now'])


@hd.route('/setup-hd-categories', methods=["GET", "POST"])
def setup_hd_categories():
    db = psql_api.PostgresAPI(get_db())
    if flask.request.method == 'POST':
        # print(flask.request.form)
        form_data = flask.request.form
        # print(form_data['hd_category_level'])
        db.exec_query(q_hd.ins_ticket_category,
                      {'parent_id': 0 if int(form_data['hd_category_level']) == 1 else form_data['hd_category_parent_id'],
                       'level': form_data['hd_category_level'],
                       'category_name': form_data['hd_category_name'],
                       'sla_days': form_data['hd_category_sla_days'] if int(form_data['hd_category_level']) == 3 else 0})
        return flask.redirect(flask.url_for('hd.setup_hd_categories'))
    db.exec_query(q_hd.get_all_ticket_category)
    return flask.render_template('setup_category.html',
                                 category_data=db.lod())


@hd.route('/open-hd-ticket', methods=["GET", "POST"])
def open_hd_ticket():
    db = psql_api.PostgresAPI(get_db())
    db.exec_query('SELECT id, category_name FROM ref_hd_ticket_category WHERE level = 1')
    cat_1_l = db.lod()
    return flask.render_template('open_ticket.html',
                                 cat_1_l=cat_1_l)


@hd.route('/_update_select_category', methods=['GET'])
def update_select_category():
    db = psql_api.PostgresAPI(get_db())
    db.exec_query(q_hd.get_top_ticket_category,
                  {'level': flask.request.args['hd_category_level']})
    return flask.jsonify(db.lod())


@hd.route('/_get_children_category', methods=['GET'])
def get_children_category():
    db = psql_api.PostgresAPI(get_db())
    db.exec_query(q_hd.get_children_cat_sql,
                  {'parent_id': flask.request.args['cat_id'],
                   'level': flask.request.args['cat_level']
                   })
    return flask.jsonify(db.lod())


app.register_blueprint(hd)
