drop database "NewSurvey";
create database "NewSurvey";

\c "NewSurvey"

grant USAGE on SCHEMA public TO dataportal;
grant usage on all sequences in schema public to dataportal;
grant select, insert, update on all tables in schema public to dataportal;
grant create on DATABASE "NewSurvey" to dataportal;

CREATE EXTENSION unaccent;
ALTER FUNCTION unaccent(text) IMMUTABLE;

CREATE EXTENSION postgis;
CREATE EXTENSION hstore;
