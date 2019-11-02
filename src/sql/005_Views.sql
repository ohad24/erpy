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


DROP VIEW IF EXISTS v_get_tickets_header;
CREATE OR REPLACE VIEW v_get_tickets_header AS
    SELECT t.id,
           t.ticket_status_id,
           s.ticket_status_name,
           f_heb_date(t.open_date) AS open_date,
           f_heb_date(COALESCE(t.due_manager_date, t.due_orig_date)) AS due_date,
           COALESCE(fc.f_count, 0) as f_count,
           cat3.category_name AS cat3_name,
           cat3.id AS cat3_id,
           cat2.category_name AS cat2_name,
           cat2.id AS cat2_id,
           cat1.category_name AS cat1_name,
           cat1.id AS cat1_id,
           f_get_full_name(u1.first_name, u1.last_name) AS create_by_f_name,
           f_get_full_name(u2.first_name, u2.last_name) AS close_by_f_name,
           f_get_full_name(u3.first_name, u3.last_name) AS assign_cust_name,
           COALESCE(f_heb_date(t.close_date), '-') AS close_date,
           t.close_reason_id,
           COALESCE(cr.ticket_close_reason_name, '-') AS ticket_close_reason_name,
           tn.note_text AS open_note_desc,
           t.assign_cust_id,
           t.create_by,
           t.category3id
    FROM ref_hd_ticket_status s,
         ref_hd_ticket_category cat3,
         ref_hd_ticket_category cat2,
         ref_hd_ticket_category cat1,
         users u1,
         users u3,
         hd_tickets t
    LEFT JOIN users u2 ON t.close_by = u2.user_id
    LEFT JOIN ref_hd_ticket_close_reason cr ON t.close_reason_id = cr.ticket_close_reason_id
    LEFT JOIN LATERAL (SELECT ticket_id, count(*) AS f_count
                       FROM hd_ticket_files f
                       WHERE t.id = f.ticket_id
                       GROUP BY ticket_id) AS fc ON true
    INNER JOIN (SELECT f.ticket_id, f.note_text FROM hd_ticket_notes f
                WHERE f.ticket_note_type_id = 1) AS tn ON tn.ticket_id = t.id
    WHERE 1=1
    AND t.ticket_status_id = s.ticket_status_id
    AND t.category3id = cat3.id
    AND cat3.parent_id = cat2.id
    AND cat2.parent_id = cat1.id
    AND t.create_by = u1.user_id
    AND t.assign_cust_id = u3.user_id;