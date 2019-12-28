CREATE USER erpy WITH
    LOGIN
    SUPERUSER
    CREATEDB
    CREATEROLE
    INHERIT
    NOREPLICATION
    CONNECTION LIMIT -1
    PASSWORD :postgres_password;

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

GRANT ALL PRIVILEGES ON DATABASE :postgres_db TO erpy;
