ins_ticket_category = """INSERT INTO hd_ticket_category (parent_id, level, category_name)
                            VALUES (%(parent_id)s, %(level)s, %(category_name)s)"""

get_top_ticket_category = """SELECT id, category_name FROM hd_ticket_category
                             WHERE level = %(level)s - 1"""

get_all_ticket_category = """WITH RECURSIVE rel_tree AS (
                                SELECT id, parent_id, level, category_name,
                                       ARRAY [id] AS ancestry
                                FROM hd_ticket_category WHERE PARENT_ID  = 0
                                UNION ALL
                                SELECT c.id, c.parent_id, c.level, 
                                       c.category_name, array_append(p.ancestry, c.id) AS ancestry
                                FROM hd_ticket_category c JOIN rel_tree p ON c.parent_id = p.id
                             )
                             SELECT * FROM rel_tree ORDER BY ancestry, parent_id"""