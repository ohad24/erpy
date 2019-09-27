from setup import csrf, get_db, User, app, flask
from tools import psql_api
from flask_login import current_user, login_required, logout_user, login_user
from queries import q_main

hd = flask.Blueprint('hd', 'hd', url_prefix='/hd', template_folder='help_desk')


@hd.route('/home')
def hd_home():
    db = psql_api.PostgresAPI(get_db())
    db.exec_query('select now()', one=True)
    d = db.lod()
    return flask.render_template('home.html', d=d['now'])


app.register_blueprint(hd)
