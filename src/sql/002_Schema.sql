DROP SCHEMA IF EXISTS erpy CASCADE;
CREATE SCHEMA erpy AUTHORIZATION erpy;

ALTER ROLE erpy SET search_path TO erpy;
--ALTER DATABASE prod SET search_path TO plant_app;