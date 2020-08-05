#!/usr/bin/python
# -*- encoding: utf-8 -*-

# uvozimo bottle.py
from bottle import *
import sqlite3
import hashlib

# povezava do datoteke baza
baza_datoteka = 'pohodnistvo.db' 

# uvozimo ustrezne podatke za povezavo
# import auth_public as auth

# uvozimo psycopg2
# import psycopg2, psycopg2.extensions, psycopg2.extras
# psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki

import os

# privzete nastavitve
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)
ROOT = os.environ.get('BOTTLE_ROOT', '/')
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

# odkomentiraj, če želiš sporočila o napakah
#debug(True)

######################################################################
#ERR in druge dobrote
@error(404)
def napaka404(error):
    return '<h1>Stran ne obstaja</h1><img src="https://upload.wikimedia.org/wikipedia/commons/d/d4/S%C3%B8ren_Kierkegaard_%281813-1855%29_-_%28cropped%29.jpg" style="width:300px;height:450px;" alt="Kierkegaard"><h2>Tudi Kierkegaard se je spraševal o obstoju, nisi edini</h2>'

@error(403)
def napaka403(error):
    return '<h1>Do te strani nimaš dostopa!</h1><a href="\moje_drustvo", font-size:px>Nazaj na začetno stran.</a>'


def javiNapaka(napaka = None):
    napaka = request.get_cookie("napaka", secret=skrivnost)
    if napaka is None:
        response.delete_cookie('napaka')
    else:
        #path doloca za katere domene naj bo napaka, default je cela domena
        response.set_cookie('napaka', napaka, path="/", secret=skrivnost)
    return napaka

skrivnost = "NekaVelikaDolgaSmesnaStvar"

def dostop():
    uporabnik = request.get_cookie("uporabnik", secret=skrivnost)
    cur = baza.cursor()
    polozaj = cur.execute("SELECT polozaj FROM oseba WHERE uporabnik=?", (uporabnik, )).fetchone()
    if uporabnik:
        return [uporabnik,polozaj[0]]
    redirect('/prijava')

######################################################################
# OSNOVNE STRANI

def rtemplate(*largs, **kwargs):
    """
    Izpis predloge s podajanjem spremenljivke ROOT z osnovnim URL-jem.
    """
    return template(ROOT=ROOT, *largs, **kwargs)

@get('/')
def osnovna_stran():
    #če prijavljen/registriran potem glavna_stran.html stran sicer prijava.html
    return rtemplate('prijava.html', naslov='Prijava')

@get('/pohodnistvo')
def glavna_stran():
    user = dostop()
    return rtemplate('glavna_stran.html')

######################################################################
# PRIJAVA / REGISTRACIJA

#zakodirajmo geslo
def hashGesla(s):
    m = hashlib.sha256()
    m.update(s.encode("utf-8"))
    return m.hexdigest()

@get('/registracija')
def registracija_get():
    return rtemplate('registracija.html', naslov='Registracija')

@post('/registracija')
def registracija_post():
    #poberimo vnesene podatke
    identiteta = request.forms.identiteta
    uporabnik = request.forms.uporabnik
    geslo = request.forms.geslo
    cur = baza.cursor()

    if len(geslo)<1:
        #dodaj sporočilo napake: prekratko geslo
        javiNapaka(napaka="geslo je prekratko")
        redirect('/registracija')
        return

    identiteta2 = cur.execute("SELECT id FROM oseba WHERE uporabnik = ?", (uporabnik, )).fetchone()
    if identiteta2 != None and identiteta != identiteta2:
        #izberi drugo uporabnisko ime
        print('hello')
        javiNapaka(napaka="to uporabniško ime je zasedeno")
        redirect('/registracija')
        return

    zgostitev = hashGesla(geslo)
    #brez str() ima lahko težave s tipom podatkov
    cur.execute("UPDATE oseba SET uporabnik = ?, geslo = ?, polozaj = ? WHERE id = ?", (str(uporabnik), str(zgostitev), 0, str(identiteta)))
    #dolocimo osebo ki uporablja brskalnik
    response.set_cookie('uporabnik', uporabnik, secret=skrivnost)
    redirect('/moje_drustvo')

@get('/prijava')
def prijava():
    return rtemplate('prijava.html', naslov='Prijava')

@post('/prijava')
def prijava_post():
    #poberimo vnesene podatke
    uporabnik = request.forms.uporabnik
    geslo = request.forms.geslo
    cur = baza.cursor()
    hashGeslo = None
    try: 
        hashGeslo = cur.execute("SELECT geslo FROM oseba WHERE uporabnik = ?", (uporabnik, )).fetchone()
        hashGeslo = hashGeslo[0]
    except:
        hashGeslo = None
    if hashGeslo is None:
        #dodaj napako, če hashGeslo none potem ni registriran
        redirect('/prijava')
        return
    if hashGesla(geslo) != hashGeslo:
        #geslo ni pravilno
        redirect('/prijava')
        return
    response.set_cookie('uporabnik', uporabnik, secret=skrivnost)
    redirect('/moje_drustvo')

@get('/odjava')
def odjava():
    response.delete_cookie('uporabnik')
    redirect('/prijava')
    
######################################################################
# DRUŠTVO

@get('/moje_drustvo')
def moje_drustvo():
    user = dostop()
    uporabnik = str(user[0])
    cur = baza.cursor()
    drustvo = cur.execute("SELECT drustvo FROM oseba WHERE uporabnik = ?", (uporabnik, )).fetchone()
    osebe = cur.execute("SELECT id, ime, priimek, spol, starost FROM oseba WHERE drustvo = ? ORDER BY oseba.priimek", (str(drustvo[0]), ))
    polozaj = int(user[1])
    if polozaj > 0:
        return rtemplate('moje_drustvo_predsednik.html', osebe=osebe)
    else:
        return rtemplate('moje_drustvo.html', osebe=osebe)

@get('/osebe/dodaj_osebo_drustvo')
def dodaj_osebo_drustvo():
    user = dostop()
    if int(user[1]) > 0:
        return rtemplate('dodaj_osebo.html')
    else:
        return napaka403(error)

######################################################################
# OSEBE

@get('/osebe')
def osebe():
    user = dostop()
    cur = baza.cursor()
    osebe = cur.execute("""
    SELECT id, ime, priimek, spol, starost, drustvo FROM oseba
        ORDER BY oseba.priimek
    """)
    if int(user[1]) == 2:
        return rtemplate('osebe.html', osebe=osebe, naslov='Pohodniki')
    else:
        return napaka403(error)

@get('/osebe/dodaj_osebo')
def dodaj_osebo():
    user = dostop()
    if int(user[1]) == 2:
        return rtemplate('dodaj_osebo.html')
    else:
        return napaka403(error)

@post('/osebe/dodaj_osebo')
def dodaj_osebo_post():
    user = dostop()
    # ce napises samo request.forms.ime pri meni ne deluje
    ime = request.forms.get('ime')
    priimek = request.forms.get('priimek')
    spol = request.forms.get('spol')
    if spol == 'Male':
        pass
    else:
        spol = 'Female'
    starost = request.forms.get('starost')
    cur = baza.cursor()
    cur.execute("INSERT INTO oseba (ime, priimek, spol, starost) VALUES (?, ?, ?, ?)", (ime, priimek, spol, starost))
    redirect('/osebe')

@get('/osebe/uredi/<id>')
def uredi_osebo(id):
    user = dostop()
    cur = baza.cursor()
    identiteta = cur.execute("SELECT id FROM oseba WHERE uporabnik = ?", (str(user[0]),)).fetchone()
    oseba = cur.execute("SELECT id, ime, priimek, spol, starost FROM oseba WHERE id = ?", (id,)).fetchone()
    if identiteta == id or int(user[1])==2:
        return rtemplate('oseba-id.html', oseba=oseba, naslov="Pohodnik <id>")
    else:
        return napaka403(error)

@post('/osebe/uredi/<id>')
def uredi_osebo_post(id):
    user = dostop()
    ime = request.forms.get('ime')
    priimek = request.forms.get('priimek')
    spol = request.forms.get('spol')
    starost = request.forms.get('starost')
    cur = baza.cursor()
    cur.execute("UPDATE oseba SET ime = ?, priimek = ?, spol = ?, starost = ? WHERE id = ?", 
        (ime, priimek, spol, starost, id))
    redirect('/osebe')


@post('/osebe/brisi/<id>')
def brisi_osebo(id):
    user = dostop()
    if int(user[1])==2:
        return cur.execute("DELETE FROM oseba WHERE id = ?", (id, ))
    else:
        return napaka403(error)
    redirect('/osebe')

@get('/osebe/<id>')
def lastnosti_osebe(id):
    user = dostop()
    cur = baza.cursor()
    drustvo = cur.execute("SELECT drustvo FROM oseba WHERE uporabnik = ?", (str(user[0]),)).fetchone()
    drustvoID = cur.execute("SELECT drustvo FROM oseba WHERE id = ?", (id,)).fetchone()
    oseba = cur.execute("SELECT id, ime, priimek, spol, starost FROM oseba WHERE id = ?", (id,)).fetchone()
    if drustvo == drustvoID or int(user[1])==2:
        return rtemplate('oseba-id.html', oseba=oseba, naslov="Pohodnik <id>")
    else:
        return napaka403(error)

######################################################################
# GORE

@get('/gore')
def gore():
    cur = baza.cursor()
    gore = cur.execute("""
    SELECT prvi_pristop, ime, visina, gorovje, drzava FROM gore
        ORDER BY gore.ime
    """)
    return rtemplate('gore.html', gore=gore)

@get('/dodaj_goro')
def dodaj_goro():
    user = dostop()
    cur = baza.cursor()
    gorovje = cur.execute("""
    SELECT gorovje.ime FROM gorovje
        ORDER BY gorovje.ime
    """).fetchall()
    #naredimo list iz tuple
    gorovje_list = [x[0] for x in gorovje]
    drzave = cur.execute("""
    SELECT drzave.ime FROM drzave
        ORDER BY drzave.ime
    """).fetchall()
    drzave_list = [y[0] for y in drzave]
    return rtemplate('dodaj_goro.html', gorovje=gorovje_list, drzave=drzave_list, naslov='Dodaj goro')

@post('/dodaj_goro')
def dodaj_goro_post():
    ime = request.forms.get('ime_gore')
    visina = request.forms.get('visina')
    prvi_pristop = request.forms.get('prvi_pristop')
    cur = baza.cursor()

    drzava = request.forms.get('drzava')
    id_drzava = cur.execute("SELECT id FROM drzave WHERE ime = ?",(drzava,)).fetchone()
    gorovje = request.forms.get('gorovje')
    id_gorovje = cur.execute("SELECT id FROM gorovje WHERE ime = ?",(gorovje,)).fetchone()

    cur.execute("""INSERT INTO gore (prvi_pristop, ime, visina, gorovje, drzava)
        VALUES (?, ?, ?, ?, ?)""",
         (int(prvi_pristop), str(ime), int(visina), str(gorovje), str(drzava)))
    redirect('/gore')

######################################################################
# DRUSTVA

@get('/drustva')
def drustva():
    user = dostop()
    cur = baza.cursor()
    drustva = cur.execute("""
    SELECT id, stevilo_clanov, ime, leto_ustanovitve FROM drustva
        ORDER BY drustva.ime
    """)
    return rtemplate('drustva.html', drustva=drustva, naslov='Društva')


######################################################################
# Za STATIC datoteke(slike)

@get('/static/<filename:path>')
def static(filename):
    #pomoje tukaj ne rabmo user = dostop(), ker drugace ne nalozi nobenih slik, če nisi prijavljen
    #user = dostop()
    return static_file(filename, root='static')

######################################################################
# O PROJEKTU

@get('/o_projektu')
def o_projektu():
    return rtemplate('o_projektu.html')

######################################################################
# Glavni program

# priklopimo se na bazo
# conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, geslo=auth.geslo, port=DB_PORT)
# conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT) # onemogočimo transakcije
# cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

######################################################################
baza = sqlite3.connect(baza_datoteka, isolation_level=None)
baza.set_trace_callback(print) # izpis sql stavkov v terminal (za debugiranje pri razvoju)
# zapoved upoštevanja omejitev FOREIGN KEY
cur = baza.cursor()
cur.execute("PRAGMA foreign_keys = ON;")

# poženemo strežnik na podanih vratih, npr. http://localhost:8080/
run(host='localhost', port=SERVER_PORT, reloader=RELOADER)