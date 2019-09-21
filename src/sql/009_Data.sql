INSERT INTO ref_user_class
             (user_class_name, permission_level)
             VALUES ('root', 99);

INSERT INTO users (user_name, user_class_id, first_name, last_name, passkey, email, phone)
                   VALUES ('erpy', 1, 'erpy', 'erpy', '1234', '1@1.com', '1111');