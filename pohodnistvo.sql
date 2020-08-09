DROP TABLE IF EXISTS oseba;
DROP TABLE IF EXISTS drustva;
DROP TABLE IF EXISTS drzave;
DROP TABLE IF EXISTS gore;
DROP TABLE IF EXISTS gorovje;
DROP TABLE IF EXISTS obiskane;

CREATE TABLE oseba (
    id             INTEGER    PRIMARY KEY,
    ime            CHAR    	  NOT NULL,
    priimek        CHAR    	  NOT NULL,
    spol           CHAR    	  NOT NULL,
    starost		   INTEGER    NOT NULL,
    drustvo        CHAR       REFERENCES drustva (ime),
    uporabnik      CHAR,
    geslo          CHAR,
    polozaj        INTEGER
);

CREATE TABLE drustva (
    id             			 INTEGER    PRIMARY KEY,
    ime        				 CHAR       NOT NULL UNIQUE,
    leto_ustanovitve         INTEGER   	NOT NULL
);

CREATE TABLE drzave (
    id             			 INTEGER    PRIMARY KEY,
    ime        				 CHAR       NOT NULL UNIQUE,
	populacija          	 INTEGER   	NOT NULL,
    povrsina		         INTEGER   	NOT NULL
);

CREATE TABLE gorovje (
    id          INTEGER PRIMARY KEY,
	ime			CHAR    UNIQUE
);

CREATE TABLE gore (
    id                  INTEGER     PRIMARY KEY AUTOINCREMENT,
	prvi_pristop		INTEGER 	NOT NULL,
	ime					CHAR		NOT NULL,
	visina				INTEGER		NOT NULL,
	gorovje				CHAR REFERENCES gorovje (ime),
	drzava				CHAR REFERENCES drzave (ime)
);

CREATE TABLE obiskane (
    id_gore         INTEGER REFERENCES gore (id),
    id_osebe        INTEGER REFERENCES oseba (id),
    leto_pristopa   INTEGER
);