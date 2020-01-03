get_user_details = """SELECT * FROM v_get_user_details
                      WHERE user_id = %(user_id)s"""

get_all_users = """SELECT * FROM v_get_user_details"""

get_all_user_class = """SELECT user_class_id, user_class_name 
                        FROM ref_user_class"""

# for login route
get_user_id = """SELECT user_id FROM users
                 WHERE (user_name = %(username)s OR email = %(username)s)
                 AND passkey = f_hash_pass(%(passkey)s)
                 AND is_enable = true
                 AND is_auth = true"""

ins_user = """INSERT INTO users (user_name, user_class_id, first_name, last_name, 
                                 passkey, email, phone, create_by)
              VALUES (%(user_name)s, %(user_class_id)s, %(first_name)s, %(last_name)s,
                      f_hash_pass(%(passkey)s), %(email)s, %(phone)s, %(create_by)s)
              RETURNING user_id"""

ins_teams_assignment = """INSERT INTO teams_assignment (team_id, user_id) 
                          VALUES (%(team_id)s, %(user_id)s)"""

ins_team = """INSERT INTO teams (team_name, description) 
              VALUES (%(team_name)s, %(team_desc)s)"""

get_all_teams = """select team_id, team_name, description from teams"""


ins_email = """INSERT INTO emails (email_status, recipients, subject, body, create_by)
               VALUES (%(email_status)s, %(recipients)s, %(subject)s, %(body)s, %(create_by)s)"""