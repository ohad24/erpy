import flask
from flask_login import UserMixin, LoginManager, current_user
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
import socket
import psycopg2
from psycopg2 import pool
from functools import wraps
import os
from tools import psql_api
from queries import q_main

hostname = socket.gethostname()

l_directory = ['users_files/hd']
for dir in l_directory:
    if not os.path.exists(dir):
        os.makedirs(dir)

app = flask.Flask('erpy')
app.secret_key = os.environ['ERPY_APP_KEY']

login_manager = LoginManager()
login_manager.init_app(app)

Bootstrap(app)
csrf = CSRFProtect(app)

# https://stackoverflow.com/questions/54638374/psycopg2-flask-tying-connection-to-before-request-teardown-appcontext
app.config['postgreSQL_pool'] = psycopg2.pool.SimpleConnectionPool(1, 20, user=os.environ['ERPY_PG_USER'],
                                                                   password=os.environ['ERPY_PG_PASS'],
                                                                   host=os.environ['ERPY_PG_HOST'],
                                                                   port=os.environ['ERPY_PG_PORT'],
                                                                   database=os.environ['ERPY_PG_DB'],
                                                                   options='-c search_path=erpy')


def get_db():
    if 'db' not in flask.g:
        flask.g.db = app.config['postgreSQL_pool'].getconn()
    return flask.g.db


@app.teardown_appcontext
def close_conn(e):
    db = flask.g.pop('db', None)
    if db is not None:
        app.config['postgreSQL_pool'].putconn(db)


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # if current_user.permission_level < roles[0]:
            #     flask.abort(403)
            return f(*args, **kwargs)

        return wrapped

    return wrapper


class User(UserMixin):
    def __init__(self, user_id):
        # print('pg_con status: {}'.format(pg_con.status))
        self.pg_api = psql_api.PostgresAPI(get_db())
        self.pg_api.exec_query(q_main.get_user_details,
                               {'user_id': user_id},
                               one=True)
        sql_data = self.pg_api.lod()
        self.id = sql_data['user_id']
        self.username = sql_data['user_name']
        self.user_class_id = sql_data['user_class_id']
        self.user_class_name = sql_data['user_class_name']
        self.permission_level = sql_data['permission_level']
        self.first_name = sql_data['first_name']
        self.last_name = sql_data['last_name']
        self.email = sql_data['email']
        self.phone = sql_data['phone']
        self.sex = sql_data['sex']
        self.is_enable = sql_data['is_enable']
        self.is_auth = sql_data['is_auth']
        self.full_name = self.first_name + ' ' + self.last_name


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.context_processor
def load_data():  # no content]
    url = str(flask.request.url_rule)
    sub_route = url.split('/')[1]
    return {"app_name": "erpy",
            "hostname": hostname,
            "env": app.env,
            "sub_route": sub_route}
