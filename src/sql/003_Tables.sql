SET CONSTRAINTS ALL DEFERRED;
--SET CONSTRAINTS ALL IMMEDIATE;

DROP TYPE IF EXISTS sex CASCADE;
CREATE TYPE sex AS ENUM ('male', 'female');


DROP DOMAIN IF EXISTS email CASCADE;
CREATE DOMAIN email AS VARCHAR CHECK (VALUE ~* '^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$');


DROP TABLE IF EXISTS ref_lang CASCADE;
CREATE TABLE ref_lang (
  lang_id SERIAL PRIMARY KEY NOT NULL,
  lang_name VARCHAR(45) UNIQUE NOT NULL,
  lang_code VARCHAR(3) UNIQUE NOT NULL
);


DROP TABLE IF EXISTS ref_translate CASCADE;
CREATE TABLE ref_translate (
  id SERIAL PRIMARY KEY NOT NULL,
  lang_id INT REFERENCES ref_lang (lang_id) NOT NULL,
  obj_name VARCHAR(45) NOT NULL,
  val_id INT NOT NULL,
  trans_text VARCHAR(45) NOT NULL
);


DROP TABLE IF EXISTS ref_user_class CASCADE;
CREATE TABLE ref_user_class (
  user_class_id SERIAL PRIMARY KEY NOT NULL,
  user_class_name VARCHAR(45) UNIQUE NOT NULL,
  permission_level INT CHECK (permission_level BETWEEN 1 AND 99) NOT NULL
);


DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY NOT NULL,
    user_name VARCHAR(40) UNIQUE NOT NULL,
    user_class_id INT REFERENCES ref_user_class (user_class_id) NOT NULL,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    passkey VARCHAR(64) NOT NULL,
    email EMAIL NOT NULL,
    phone VARCHAR(30) NOT NULL,
    office_phone VARCHAR(30),
    birth_date DATE,
    sex SEX,
    is_enable BOOLEAN DEFAULT true NOT NULL,
    is_auth BOOLEAN DEFAULT true NOT NULL,
    create_date TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    create_by INT DEFAULT 0 NOT NULL
);


DROP TABLE IF EXISTS teams CASCADE;
CREATE TABLE teams (
    team_id SERIAL PRIMARY KEY NOT NULL,
    team_name VARCHAR(40) UNIQUE NOT NULL,
    description VARCHAR(100)
);


DROP TABLE IF EXISTS teams_assignment;
CREATE TABLE teams_assignment (
    id SERIAL PRIMARY KEY NOT NULL,
    team_id INT REFERENCES teams (team_id) NOT NULL,
    user_id INT REFERENCES users (user_id) NOT NULL
);


DROP TABLE IF EXISTS hd_ticket_category;
CREATE TABLE hd_ticket_category(
    id SERIAL PRIMARY KEY NOT NULL,
    parent_id INT DEFAULT 0 NOT NULL,
    level INT NOT NULL,
    category_name VARCHAR(100),
    sla_days INT DEFAULT 0 NOT NULL,
    active BOOLEAN DEFAULT true NOT NULL,
    create_date TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    create_by INT DEFAULT 0 NOT NULL
);