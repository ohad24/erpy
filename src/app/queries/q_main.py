get_user_details = """SELECT * FROM users
                      WHERE user_id = %(user_id)s"""

# for login route
get_user_id = """
    SELECT user_id FROM users
    WHERE (user_name = %(username)s OR email = %(username)s)
    AND passkey = %(passkey)s
    AND is_enable = true
    AND is_auth = true"""