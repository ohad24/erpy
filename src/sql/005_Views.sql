DROP VIEW IF EXISTS v_get_user_details;
CREATE OR REPLACE VIEW v_get_user_details AS
    SELECT t.user_id,
           t.user_name,
           t.user_class_id,
           c.user_class_name,
           c.permission_level,
           t.first_name,
           t.last_name,
           t.email,
           t.phone,
           t.sex,
           t.birth_date,
           t.is_enable,
           t.is_auth,
           t.create_date,
           t.create_by
    FROM users t,
         ref_user_class c
    WHERE t.user_class_id = c.user_class_id;