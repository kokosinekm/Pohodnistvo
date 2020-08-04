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
debug(True)

######################################################################
#ERR in druge dobrote
@error(404)
def napaka404(error):
    return '<h1>Stran ne obstaja</h1><img src="https://upload.wikimedia.org/wikipedia/commons/d/d4/S%C3%B8ren_Kierkegaard_%281813-1855%29_-_%28cropped%29.jpg" style="width:300px;height:450px;" alt="Kierkegaard"><h2>Tudi Kierkegaard se je spraševal o obstoju, nisi edini</h2>'

def nastaviSporocilo(sporocilo = None):
    # global napaka Sporocilo
    sporocilo = request.get_cookie("sporocilo", secret=skrivnost)
    if sporocilo is None:
        response.delete_cookie('sporocilo')
    else:
        #path doloca za katere domene naj bo sporocilo, default je cela domena
        response.set_cookie('sporocilo', sporocilo, path="/", secret=skrivnost)
    return sporocilo

skrivnost = "NekaVelikaDolgaSmesnaStvar"
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
    return rtemplate('prijava.html')

@get('/pohodnistvo')
def glavna_stran():
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
    return rtemplate('registracija.html')

@post('/registracija')
def registracija_post():
    #poberimo vnesene podatke
    identiteta = request.forms.identiteta
    uporabnik = request.forms.uporabnik
    geslo = request.forms.geslo
    cur = baza.cursor()

    if uporabnik is None:
        #dodaj sporočilo napake
        redirect('/registracija')
        return
    if len(geslo)<1:
        #dodaj sporočilo napake: prekratko geslo
        redirect('/registracija')
        return

    identiteta2 = cur.execute("SELECT id FROM oseba WHERE uporabnik = ?", (uporabnik, )).fetchone()
    if identiteta2 != None and identiteta != identiteta2:
        #izberi drugo uporabnisko ime
        redirect('/registracija')
        return

    zgostitev = hashGesla(geslo)
    #brez str() ima lahko težave s tipom podatkov
    cur.execute("UPDATE oseba SET uporabnik = ?, geslo = ? WHERE id = ?", (str(uporabnik), str(zgostitev), str(identiteta)))
    #dolocimo osebo ki uporablja brskalnik
    response.set_cookie('uporabnik', uporabnik, secret=skrivnost)
    redirect('/moje_drustvo')

@get('/prijava')
def prijava():
    return rtemplate('prijava.html')

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
# DRUŠTVO in VREME

@get('/moje_drustvo')
def moje_drustvo():
    uporabnik = request.get_cookie("uporabnik", secret=skrivnost)
    cur = baza.cursor()
    drustvo = cur.execute("SELECT drustvo FROM oseba WHERE uporabnik = ?", (uporabnik, )).fetchone()
    osebe = cur.execute("SELECT id, ime, priimek, spol, starost FROM oseba WHERE drustvo = ? ORDER BY oseba.priimek", (str(drustvo[0]), ))
    print(osebe)
    return rtemplate('moje_drustvo.html', osebe=osebe)

######################################################################
# OSEBE

@get('/osebe')
def osebe():
    cur = baza.cursor()
    osebe = cur.execute("""
    SELECT id, ime, priimek, spol, starost FROM oseba
        ORDER BY oseba.priimek
    """)
    return rtemplate('osebe.html', osebe=osebe, naslov='Pohodniki')

@get('/osebe/dodaj_osebo')
def dodaj_osebo():
    return rtemplate('dodaj_osebo.html')

@post('/osebe/dodaj_osebo')
def dodaj_osebo_post():
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
    cur = baza.cursor()
    oseba = cur.execute("SELECT id, ime, priimek, spol, starost FROM oseba WHERE id = ?", (id,)).fetchone()
    return rtemplate('oseba-edit.html', oseba=oseba, naslov="Uredi osebo")

@post('/osebe/uredi/<id>')
def uredi_osebo_post(id):
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
    cur.execute("DELETE FROM oseba WHERE id = ?", (id, ))
    redirect('/osebe')

@get('/osebe/<id>')
def lastnosti_osebe(id):
    cur = baza.cursor()
    oseba = cur.execute("SELECT id, ime, priimek, spol, starost FROM oseba WHERE id = ?", (id,)).fetchone()
    return rtemplate('oseba-id.html', oseba=oseba, naslov="Pohodnik <id>")

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
    cur = baza.cursor()
    gorovje = cur.execute("""
    SELECT gorovje.ime FROM gorovje
        ORDER BY gorovje.ime
    """).fetchall()
    drzave = cur.execute("""
    SELECT drzave.ime FROM drzave
        
        ORDER BY drzave.ime
    """).fetchall()
    return rtemplate('dodaj_goro.html', gorovje=gorovje, drzave=drzave, naslov='Dodaj goro')

@post('/dodaj_goro')
def dodaj_goro_post():
    ime = request.forms.get('ime_gore')
    visina = request.forms.get('visina')
    prvi_pristop = request.forms.get('prvi_pristop')
    cur = baza.cursor()
    cur.execute("INSERT INTO gore (prvi_pristop, ime, visina, gorovje, drzava) VALUES (?, ?, ?, ?, ?)", (prvi_pristop, ime, visina))
    redirect('/gore')

######################################################################
# DRUSTVA

@get('/drustva')
def drustva():
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