DROP TABLE IF EXISTS obiskane;
DROP TABLE IF EXISTS gore;
DROP TABLE IF EXISTS drzave;
DROP TABLE IF EXISTS gorovje;
DROP TABLE IF EXISTS oseba;
DROP TABLE IF EXISTS drustva;

CREATE TABLE drustva (
    id             			 INTEGER    PRIMARY KEY,
    ime        				 TEXT       NOT NULL UNIQUE,
    leto_ustanovitve         INTEGER   	NOT NULL
);

CREATE TABLE oseba (
    id             INTEGER    PRIMARY KEY,
    ime            TEXT    	  NOT NULL,
    priimek        TEXT    	  NOT NULL,
    spol           TEXT    	  NOT NULL,
    starost		   INTEGER    NOT NULL,
    drustvo        TEXT       REFERENCES drustva (ime),
    uporabnik      TEXT,
    geslo          TEXT,
    polozaj        INTEGER
);

CREATE TABLE drzave (
    id             			 INTEGER    PRIMARY KEY,
    ime        				 TEXT       NOT NULL UNIQUE,
	populacija          	 INTEGER   	NOT NULL,
    povrsina		         INTEGER   	NOT NULL
);

CREATE TABLE gorovje (
    id          INTEGER PRIMARY KEY,
	ime			TEXT    UNIQUE
);

CREATE TABLE gore (
    id                  SERIAL     PRIMARY KEY,
	prvi_pristop		INTEGER 	NOT NULL,
	ime					TEXT		NOT NULL,
	visina				INTEGER		NOT NULL,
	gorovje				TEXT REFERENCES gorovje (ime),
	drzava				TEXT REFERENCES drzave (ime)
);

CREATE TABLE obiskane (
    id_gore    INTEGER REFERENCES gore (id),
    id_osebe   INTEGER REFERENCES oseba (id)
);