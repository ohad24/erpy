from setup import csrf, get_db, User, app, flask
from tools import psql_api
from flask_login import current_user, login_required, logout_user, login_user
from queries import q_main

index_blueprint = flask.Blueprint('index', 'index', template_folder='templates')


@index_blueprint.route('/')
def index():
    return flask.redirect(flask.url_for('index.home'))


@index_blueprint.route('/home')
def home():
    db = psql_api.PostgresAPI(get_db())
    db.exec_query('select now()', one=True)
    d = db.lod()
    return flask.render_template('home.html', d=d['now'])


# login route
@index_blueprint.route('/login', methods=["GET", "POST"])
def login():
    pg_api = psql_api.PostgresAPI(get_db())
    if flask.request.method == 'POST':
        username = flask.request.form['username']
        # password = passwords.hash_password(flask.request.form['password'])
        password = flask.request.form['password']
        pg_api.exec_query(q_main.get_user_id,
                          {'username': username, 'passkey': password},
                          True
                          )
        sql_data = pg_api.lod()
        if len(sql_data) > 0:
            user = User(sql_data['user_id'])
            login_user(user)
            flask.flash('התחברת בהצלחה', 'success')
            return redirect_dest(fallback=flask.url_for('index.home'))
        else:
            flask.flash('התחברות נכשלה', 'error')
    if 'url_args' not in flask.session:
        flask.session['url_args'] = dict(flask.request.args)
        if 'next' in flask.session['url_args']:
            flask.session['url_args'].pop('next')
    return flask.render_template('login.html', csrf=csrf)


def redirect_dest(fallback):
    dest = flask.request.args.get('next')
    d = flask.session['url_args']
    # print(d)
    try:
        dest_url = flask.url_for(dest, **d)
        flask.session.pop('url_args', None)
    except Exception as e:
        # print(e)
        return flask.redirect(fallback)
    return flask.redirect(dest_url)


# logout route
@index_blueprint.route('/logout')
@login_required
def logout():
    # user_instances.remove(current_user.id)
    logout_user()
    flask.flash('יצאת בהצלחה', 'success')
    return flask.redirect(flask.url_for('index.home'))


@index_blueprint.route('/users', methods=["GET", "POST"])
@login_required
def users():
    db = psql_api.PostgresAPI(get_db())
    if flask.request.method == 'POST':
        fd = flask.request.form
        db.exec_query(q_main.ins_user, {
            'user_name': fd['username'], 'user_class_id': fd['user-class-select-list'],
            'first_name': fd['f_name'], 'last_name': fd['l_name'],
            'passkey': fd['password'],
            'email': fd['email'], 'phone': fd['phone'], 'create_by': current_user.id}, one=True)
        user_id = db.lod()['user_id']
        for ut in fd.getlist('teams-select-list'):
            db.exec_query(q_main.ins_teams_assignment, {'team_id': ut,
                                                            'user_id': user_id})
        flask.flash('היוזר נוסף בהצלחה', 'success')
        return flask.redirect(flask.url_for('index.users'))
    db.exec_query(q_main.get_all_users)
    l_users = db.lod()
    db.exec_query(q_main.get_all_user_class)
    l_user_class = db.lod()
    db.exec_query(q_main.get_all_teams)
    l_teams = db.lod()
    return flask.render_template('users.html',
                                 l_users=l_users,
                                 l_user_class=l_user_class,
                                 l_teams=l_teams)


@index_blueprint.route('/teams', methods=["GET", "POST"])
@login_required
def teams():
    db = psql_api.PostgresAPI(get_db())
    if flask.request.method == 'POST':
        fd = flask.request.form
        db.exec_query(q_main.ins_team,
                          {'team_name': fd['team_name'],
                           'team_desc': fd['team_desc']})
        flask.flash('הקבוצה נפתחה בהצלחה', 'success')
        return flask.redirect(flask.url_for('index.teams'))
    db.exec_query(q_main.get_all_teams)
    l_teams = db.lod()
    return flask.render_template('teams.html',
                                 l_teams=l_teams)


app.register_blueprint(index_blueprint)
