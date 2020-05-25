DROP TABLE IF EXISTS oseba;
DROP TABLE IF EXISTS drustva;
DROP TABLE IF EXISTS drzave;
DROP TABLE IF EXISTS drustva;
DROP TABLE IF EXISTS drustva;

CREATE TABLE oseba (
    id             INTEGER    PRIMARY KEY,
    ime            CHAR    	  NOT NULL,
    priimek        CHAR    	  NOT NULL,
    spol           CHAR    	  NOT NULL,
    starost		   INTEGER    NOT NULL
);

CREATE TABLE drustva (
    id             			 INTEGER    PRIMARY KEY,
    stevilo_clanov           INTEGER   	NOT NULL,
    ime        				 CHAR       NOT NULL,
    leto_ustanovitve         INTEGER   	NOT NULL
);

CREATE TABLE drzave (
    id             			 INTEGER    PRIMARY KEY,
    ime        				 CHAR       NOT NULL,
	populacija          	 INTEGER   	NOT NULL,
    povrsina		         INTEGER   	NOT NULL
);

CREATE TABLE gorovje (
	ime			CHAR NOT NULL
);

CREATE TABLE gore (
	prvi_pristop		INTEGER 	NOT NULL,
	ime					CHAR		NOT NULL,
	visina				INTEGER		NOT NULL,
	gorovje				CHAR REFERENCES gorovje (ime) 
	drzava				CHAR REFERENCES drzave 	(ime)
);