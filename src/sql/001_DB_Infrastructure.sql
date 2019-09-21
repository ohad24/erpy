CREATE USER erpy WITH
    LOGIN
    SUPERUSER
    CREATEDB
    CREATEROLE
    INHERIT
    NOREPLICATION
    CONNECTION LIMIT -1
    PASSWORD 'erpy'; --FIXME: set password variable
GRANT postgres TO erpy WITH ADMIN OPTION; --FIXME: remove this (or alter)
-- check DB TZ on dba
ALTER USER erpy SET timezone='Asia/Jerusalem';

DROP DATABASE IF EXISTS :env;

-- create db
CREATE DATABASE :env
    WITH
    OWNER = erpy
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1
    LC_COLLATE = 'he_IL.utf8'
	  LC_CTYPE = 'he_IL.utf8'
	  TEMPLATE 'template0';

ALTER DATABASE :env SET lc_time TO 'he_IL.utf8';

-- GRANT CONNECT ON DATABASE :env TO :app_user;
-- SET lc_time TO 'he_IL.utf8';


-- CREATE USER :app_user WITH PASSWORD 'py_app321!';
-- ALTER USER :app_user SET timezone='Asia/Jerusalem';


