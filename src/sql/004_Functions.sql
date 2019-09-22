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
