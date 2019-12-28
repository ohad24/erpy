CREATE USER erpy WITH
    LOGIN
    SUPERUSER
    CREATEDB
    CREATEROLE
    INHERIT
    NOREPLICATION
    CONNECTION LIMIT -1
    PASSWORD :postgres_password; --FIXME: set password variable
GRANT postgres TO erpy WITH ADMIN OPTION; --FIXME: remove this (or alter)
-- check DB TZ on dba
ALTER USER erpy SET timezone=:tz;

DROP DATABASE IF EXISTS :postgres_db;

-- create db
CREATE DATABASE :postgres_db
    WITH
    OWNER = erpy
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1
    LC_COLLATE = 'he_IL.utf8'
	  LC_CTYPE = 'he_IL.utf8'
	  TEMPLATE 'template0';

ALTER DATABASE :postgres_db SET lc_time TO :lang;

-- GRANT CONNECT ON DATABASE :env TO :app_user;
-- SET lc_time TO 'he_IL.utf8';


-- CREATE USER :app_user WITH PASSWORD 'py_app321!';
-- ALTER USER :app_user SET timezone='Asia/Jerusalem';


