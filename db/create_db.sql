DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS listings;
DROP TABLE IF EXISTS photos;
DROP TABLE IF EXISTS user_photo;
DROP TABLE IF EXISTS listing_photo;

CREATE TABLE users
(
  username VARCHAR(32) NOT NULL
    CONSTRAINT users_pkey
    PRIMARY KEY,
  email   VARCHAR(128) NOT NULL,
  pass    VARCHAR(64)  NOT NULL,
  address_id VARCHAR(128),
  city VARCHAR(64),
  state VARCHAR(2),
  zipcode INTEGER,
  country VARCHAR(64),
  other_address_details VARCHAR(128),
  rating  INTEGER
);

CREATE UNIQUE INDEX user_email_uindex
  ON users (username);

CREATE TABLE transactions
(
  id           SERIAL       NOT NULL
    CONSTRAINT transactions_pkey
    PRIMARY KEY,
  buyer_name   VARCHAR(32) NOT NULL,
  seller_name  VARCHAR(32) NOT NULL,
  timestamp    INTEGER      NOT NULL
);

CREATE UNIQUE INDEX transactions_id_uindex
  ON transactions (id);

CREATE TABLE listings
(
  id             SERIAL     NOT NULL
    CONSTRAINT listing_pkey
    PRIMARY KEY,
  name           VARCHAR(64) NOT NULL,
  price_per_unit INTEGER,
  unit           VARCHAR(32),
  seller_name    VARCHAR(32),
  harvested      VARCHAR(32),
  quantity       INTEGER
);

CREATE UNIQUE INDEX listings_id_uindex
  ON listings (id);

create table photos
(
	id serial not null
		constraint photos_pkey
			primary key
)
;

create unique index photos_id_uindex
	on photos (id)
;

create table user_photo
(
	photo_id integer,
	user_id varchar(32)
)
;

create table listing_photo
(
  photo_id integer,
  listing_id integer
)
;
