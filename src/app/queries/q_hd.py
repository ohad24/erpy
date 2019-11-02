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

get_user_ticket_assign_data = """SELECT user_id,
                                        f_get_full_name(first_name, last_name) AS full_name 
                                 FROM users u
                                 WHERE user_id != %(current_user_id)s"""

ins_ticket = """INSERT INTO hd_tickets (ticket_status_id, category3id, open_date,
                                        due_orig_date, assign_cust_id, create_by)
                VALUES (1, %(category3id)s, NOW(), f_calc_orig_hd_ticket_sla_date(%(category3id)s),
                        %(assign_cust_id)s, %(create_by)s)
                RETURNING id AS ticket_id"""
                    
ins_ticket_note = """INSERT INTO hd_ticket_notes (ticket_id, ticket_note_type_id, note_text, create_by) 
                     VALUES (%(ticket_id)s, %(ticket_note_id)s, %(note_text)s, %(create_by)s)"""

ins_ticket_file = """INSERT INTO hd_ticket_files (ticket_id, file_name, gen_file_name, 
                                                   mimetype, file_size, create_by)
                      VALUES (%(ticket_id)s, %(file_name)s, %(gen_file_name)s,
                              %(mimetype)s, %(file_size)s, %(create_by)s)"""

ins_cat3_teams = """INSERT INTO ref_hd_ticket_cat3_teams (cat3_id, team_id)
                    VALUES (%(cat3_id)s, %(team_id)s)"""

get_user_tickets = """SELECT * FROM v_get_tickets_header
                      WHERE assign_cust_id = %(user_id)s"""

get_ticket_header = """SELECT * FROM v_get_tickets_header
                       WHERE id = %(ticket_id)s"""

get_my_teams_tickets_header = """SELECT * FROM v_get_tickets_header t
                                 WHERE EXISTS(
                                     SELECT 1
                                     FROM ref_hd_ticket_cat3_teams ct
                                     WHERE EXISTS (SELECT 1
                                                   FROM teams_assignment ta
                                                   WHERE ct.team_id = ta.team_id
                                                   AND user_id = %(user_id)s)
                                     AND t.category3id = ct.cat3_id)"""

ins_user_ticket_note = """INSERT INTO hd_ticket_notes (ticket_id, ticket_note_type_id,
                                                       note_text, create_by)
                          VALUES (%(ticket_id)s, %(ticket_note_type_id)s,
                                  %(note_text)s, %(create_by)s)"""

ins_user_ticket_note_log = """INSERT INTO hd_ticket_notes (ticket_id, ticket_note_type_id,
                                                           note_text, old_data, new_data, create_by)
                              VALUES (%(ticket_id)s, 4, %(note_text)s,
                                      %(old_data)s, %(new_data)s, %(create_by)s)"""

get_ticket_notes = """SELECT tn.*,
                             f_get_full_name(u.first_name, u.last_name) AS full_name,
                             f_heb_date(tn.create_date) AS heb_date,
                             to_char(tn.create_date, 'HH24:MI') AS time_,
                             nt.ticket_note_type_name
                      FROM users u,
                           ref_hd_ticket_note_type nt,
                           hd_ticket_notes tn
                      WHERE 1=1
                      AND tn.create_by = u.user_id
                      AND tn.ticket_note_type_id = nt.ticket_note_type_id
                      AND ticket_id = %(ticket_id)s
                      ORDER BY tn.create_date DESC"""

get_ticket_files = """SELECT * FROM hd_ticket_files
                      WHERE ticket_id = %(ticket_id)s"""

get_orig_filename = """SELECT file_name, mimetype FROM hd_ticket_files
                       WHERE gen_file_name=%(gen_file_name)s"""

update_ticket_header = """WITH cur_data AS (
                              SELECT category3id FROM hd_tickets
                              WHERE id = %(ticket_id)s
                          )
                          UPDATE hd_tickets t SET category3id = %(category3id)s
                          WHERE id = %(ticket_id)s
                          RETURNING (SELECT category3id FROM cur_data)"""

get_1st_cat = """SELECT id, category_name FROM ref_hd_ticket_category WHERE level = 1"""

# get_2nd_cat_by_1st = """SELECT id, category_name
#                         FROM ref_hd_ticket_category
#                         WHERE parent_id = %(category1id)s"""
#
# get_3rd_cat_by_2nd = """SELECT id, category_name
#                         FROM ref_hd_ticket_category
#                         WHERE parent_id = %(category2id)s"""

get_ticket_close_reason = """SELECT * FROM ref_hd_ticket_close_reason"""

close_ticket_status = """UPDATE hd_tickets SET close_date=NOW(),
                                               ticket_status_id=3,
                                               close_by = %(close_by)s,
                                               close_reason_id = %(close_reason_id)s
                         WHERE id=%(ticket_id)s"""