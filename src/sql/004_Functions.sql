-- DROP FUNCTION f_heb_date;
CREATE OR REPLACE FUNCTION f_heb_date(v_date timestamptz)
RETURNS VARCHAR AS $$
BEGIN
RETURN to_char(v_date::date, 'TMDay, DD TMMonth YYYY');
END$$ LANGUAGE plpgsql;


-- DROP FUNCTION f_html_date;
CREATE OR REPLACE FUNCTION f_html_date(v_date timestamptz)
RETURNS VARCHAR AS $$
BEGIN
RETURN to_char(v_date::date, 'yyyy-MM-dd');
END$$ LANGUAGE plpgsql;


-- DROP FUNCTION f_get_full_name;
CREATE OR REPLACE FUNCTION f_get_full_name(first_name varchar, last_name varchar)
RETURNS VARCHAR AS $$
BEGIN
RETURN first_name || ' ' || last_name;
END$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION f_calc_orig_hd_ticket_sla_date(category3id INT)
RETURNS DATE AS $$
DECLARE v_due_orig_date DATE;
BEGIN
    SELECT now() + interval '1' day * sla_days INTO v_due_orig_date
    FROM ref_hd_ticket_category
    WHERE id = category3id;
    RETURN v_due_orig_date;
END $$ LANGUAGE plpgsql;