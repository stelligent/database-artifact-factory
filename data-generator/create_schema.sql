DROP TABLE IF EXISTS person;

CREATE TABLE person (
  id SERIAL,
  firstname varchar(50),
  lastname varchar(50),
  state char(2)
);
