from setup import app, hostname, flask, csrf, get_db, User
from tools import psql_api
from flask_login import current_user, login_required, logout_user, login_user
from queries import q_main

@app.context_processor
def load_data():  # no content
    return {"app_name": "erpy",
            "hostname": hostname,
            "env": app.env}

@app.route('/')
def index():
    return flask.redirect(flask.url_for('home'))


@app.route('/home')
def home():
    db = psql_api.PostgresAPI(get_db())
    db.exec_query('select now()', one=True)
    d = db.lod()
    return flask.render_template('home.html', d=d['now'])


# login route
@app.route('/login', methods=["GET", "POST"])
def login():
    pg_api = psql_api.PostgresAPI(get_db())
    if flask.request.method == 'POST':
    #     app.logger.debug(flask.session['next'])  # the get the create case form data
        username = flask.request.form['username']
        # print(flask.request.form)
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
            # if flask.session['next']:
    #             return flask.redirect(flask.url_for(flask.session['next']))
    #         return flask.redirect(flask.url_for('index'))
            return redirect_dest(fallback=flask.url_for('index'))
        else:
            flask.flash('התחברות נכשלה', 'error')
    # flask.session['next'] = flask.request.args.get('next', None)
    if not 'url_args' in flask.session:
        flask.session['url_args'] = dict(flask.request.args)
        if 'next' in flask.session['url_args']:
            flask.session['url_args'].pop('next')
            # print(flask.session['url_args'])
    return flask.render_template('login.html', csrf=csrf)


def redirect_dest(fallback):
    dest = flask.request.args.get('next')
    d = flask.session['url_args']
    # print(d)
    try:
        dest_url = flask.url_for(dest, **d)
        flask.session.pop('url_args', None)
    except Exception as e:
        print(e)
        return flask.redirect(fallback)
    return flask.redirect(dest_url)

# logout route
@app.route('/logout')
@login_required
def logout():
    # user_instances.remove(current_user.id)
    logout_user()
    flask.flash('יצאת בהצלחה', 'success')
    return flask.redirect(flask.url_for('index'))