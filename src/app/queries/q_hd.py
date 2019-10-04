ins_ticket_category = """INSERT INTO ref_hd_ticket_category (parent_id, level, category_name, sla_days)
                         VALUES (%(parent_id)s, %(level)s,
                                 %(category_name)s, %(sla_days)s)"""

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
                    
ins_ticket_note = """INSERT INTO hd_ticket_notes (ticket_id, ticket_note_id, note_text, create_by) 
                     VALUES (%(ticket_id)s, %(ticket_note_id)s, %(note_text)s, %(user_id)s)"""