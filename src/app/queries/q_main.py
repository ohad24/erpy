get_user_details = """SELECT * FROM v_get_user_details
                      WHERE user_id = %(user_id)s"""

# for login route
get_user_id = """SELECT user_id FROM users
                 WHERE (user_name = %(username)s OR email = %(username)s)
                 AND passkey = %(passkey)s
                 AND is_enable = true
                 AND is_auth = true"""

ins_user = """INSERT INTO users (user_name, user_class_id, first_name, last_name, 
                                 passkey, email, phone, create_by)
              VALUES (%(user_name)s, %(user_class_id)s, %(first_name)s, %(last_name)s,
                      %(passkey)s, %(email)s, %(phone)s, %(create_by)s)
              RETURNING user_id"""

ins_teams_assignment = """INSERT INTO teams_assignment (team_id, user_id) 
                          VALUES (%(team_id)s, %(user_id)s)"""