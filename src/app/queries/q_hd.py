ins_ticket_category = """INSERT INTO ref_hd_ticket_category (parent_id, level, category_name, sla_days)
                         VALUES (%(parent_id)s, %(level)s,
                                 %(category_name)s, %(sla_days)s)
                         RETURNING id"""

get_top_ticket_category = """SELECT id, category_name FROM ref_hd_ticket_category
                             WHERE level = %(level)s - 1"""

get_all_ticket_category = """WITH RECURSIVE rel_tree AS (
                                SELECT id, parent_id, level, category_name,
                                       ARRAY [id] AS ancestry
                                FROM ref_hd_ticket_category WHERE PARENT_ID  = 0
                                UNION ALL
                                SELECT c.id, c.parent_id, c.level, 
                                       c.category_name, array_append(p.ancestry, c.id) AS ancestry
                                FROM ref_hd_ticket_category c JOIN rel_tree p ON c.parent_id = p.id
                             )
                             SELECT * FROM rel_tree ORDER BY ancestry, parent_id"""

get_children_cat_sql = """SELECT id, category_name 
                          FROM ref_hd_ticket_category
                          WHERE parent_id = %(parent_id)s
                          AND level = %(level)s"""

ins_ticket = """INSERT INTO hd_tickets (ticket_status_id, category3id, open_date,
                                            due_orig_date, create_by)
                VALUES (1, %(category3id)s, NOW(),
                            f_calc_orig_hd_ticket_sla_date(%(category3id)s), %(user_id)s)
                RETURNING id AS ticket_id"""
                    
ins_ticket_note = """INSERT INTO hd_ticket_notes (ticket_id, ticket_note_type_id, note_text, create_by) 
                     VALUES (%(ticket_id)s, %(ticket_note_id)s, %(note_text)s, %(user_id)s)"""

ins_ticket_file = """INSERT INTO hd_ticket_files (ticket_id, file_name, gen_file_name, 
                                                   mimetype, file_size, create_by)
                      VALUES (%(ticket_id)s, %(file_name)s, %(gen_file_name)s,
                              %(mimetype)s, %(file_size)s, %(create_by)s)"""

ins_cat3_teams = """INSERT INTO ref_hd_ticket_cat3_teams (cat3_id, team_id)
                    VALUES (%(cat3_id)s, %(team_id)s)"""

get_user_tickets = """
    WITH file_count as (
        SELECT ticket_id, count(*) as f_count FROM hd_ticket_files f
        GROUP BY ticket_id
    )
    SELECT t.id,
           t.ticket_status_id,
           s.ticket_status_name,
           f_heb_date(t.open_date) as open_date,
           f_heb_date(COALESCE(t.due_manager_date, t.due_orig_date)) as due_date,
           COALESCE(fc.f_count, 0) as f_count,
           cat3.category_name AS cat3_name,
           cat2.category_name AS cat2_name,
           cat1.category_name AS cat1_name
    FROM ref_hd_ticket_status s,
         ref_hd_ticket_category cat3,
         ref_hd_ticket_category cat2,
         ref_hd_ticket_category cat1,
         hd_tickets t
    LEFT JOIN file_count fc ON t.id = fc.ticket_id
    WHERE 1=1
    AND t.ticket_status_id = s.ticket_status_id
    AND t.category3id = cat3.id
    AND cat3.parent_id = cat2.id
    AND cat2.parent_id = cat1.id
    AND t.create_by = %(user_id)s"""

get_ticket_header = """
    SELECT t.id,
           t.ticket_status_id,
           s.ticket_status_name,
           f_heb_date(t.open_date) as open_date,
           f_heb_date(COALESCE(t.due_manager_date, t.due_orig_date)) as due_date,
           cat3.category_name AS cat3_name,
           cat3.id AS cat3_id,
           cat2.category_name AS cat2_name,
           cat2.id AS cat2_id,
           cat1.category_name AS cat1_name,
           cat1.id AS cat1_id,
           f_get_full_name(u1.first_name, u1.last_name) as create_by_f_name,
           f_get_full_name(u2.first_name, u2.last_name) as close_by_f_name
    FROM ref_hd_ticket_status s,
         ref_hd_ticket_category cat3,
         ref_hd_ticket_category cat2,
         ref_hd_ticket_category cat1,
         users u1,
         hd_tickets t
    LEFT JOIN users u2 ON t.close_by = u2.user_id
    WHERE 1=1
    AND t.ticket_status_id = s.ticket_status_id
    AND t.category3id = cat3.id
    AND cat3.parent_id = cat2.id
    AND cat2.parent_id = cat1.id
    AND t.create_by = u1.user_id
    AND t.id = %(ticket_id)s"""

ins_user_ticket_note = """INSERT INTO hd_ticket_notes (ticket_id, ticket_note_type_id,
                                                       note_text, create_by)
                          VALUES (%(ticket_id)s, %(ticket_note_type_id)s,
                                  %(note_text)s, %(create_by)s)"""

get_ticket_notes = """SELECT tn.*,
                             f_get_full_name(u.first_name, u.last_name) AS full_name,
                             f_heb_date(tn.create_date) AS heb_date,
                             to_char(tn.create_date, 'HH24:MI') AS time_
                      FROM hd_ticket_notes tn, users u
                      WHERE 1=1
                      AND tn.create_by = u.user_id
                      AND ticket_id = %(ticket_id)s
                      ORDER BY tn.create_date DESC"""

get_ticket_files = """SELECT * FROM hd_ticket_files
                      WHERE ticket_id = %(ticket_id)s"""

get_orig_filename = """SELECT file_name, mimetype FROM hd_ticket_files
                       WHERE gen_file_name=%(gen_file_name)s"""

update_ticket_header = """UPDATE hd_tickets SET category3id = %(category3id)s
                          WHERE id = %(ticket_id)s"""

get_1st_cat = """SELECT id, category_name FROM ref_hd_ticket_category WHERE level = 1"""