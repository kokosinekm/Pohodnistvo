import sqlite3

baza_datoteka = 'pohodnistvo.db'

def uvoziSQL(cur, datoteka):
    with open(datoteka, encoding="utf8") as f:
        koda = f.read()
        cur.executescript(koda)

# Uvoz preko SQL skript
with sqlite3.connect(baza_datoteka) as baza:
    cur = baza.cursor()
    uvoziSQL(cur, 'pohodnistvo.sql')
    uvoziSQL(cur, 'Podatki/Drustva.sql')
    uvoziSQL(cur, 'Podatki/Drzave.sql')
    uvoziSQL(cur, 'Podatki/Gore.sql')
    uvoziSQL(cur, 'Podatki/Gorovje.sql')
    uvoziSQL(cur, 'Podatki/Osebe.sql')