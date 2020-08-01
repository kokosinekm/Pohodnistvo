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
# debug(True)

######################################################################
# OSNOVNE STRANI

def rtemplate(*largs, **kwargs):
    """
    Izpis predloge s podajanjem spremenljivke ROOT z osnovnim URL-jem.
    """
    return template(ROOT=ROOT, *largs, **kwargs)

@get('/')
def osnovna_stran():
    redirect('/pohodnistvo')

@get('/pohodnistvo')
def glavna_stran():
    return rtemplate('glavna_stran.html')

######################################################################
# PRIJAVA / REGISTRACIJA

@get('/pohodnistvo/registracija')
def registracija():
    return rtemplate('registracija.html')

######################################################################
# OSEBE

@get('/osebe')
def osebe():
    cur = baza.cursor()
    osebe = cur.execute("""
    SELECT id, ime, priimek, spol, starost FROM oseba
        ORDER BY oseba.priimek
    """)
    return rtemplate('osebe.html', osebe=osebe)

@get('/dodaj_osebo')
def dodaj_osebo():
    return rtemplate('dodaj_osebo.html')

@post('/dodaj_osebo')
def dodaj_osebo_post():
    # ce napises samo request.forms.ime pri meni ne deluje
    ime = request.forms.get('ime')
    priimek = request.forms.get('priimek')
    spol = request.forms.get('moski')
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
    return template('oseba-edit.html', oseba=oseba, naslov="Uredi osebo")

@post('/osebe/brisi/<id>')
def brisi_osebo(id):
    cur.execute("DELETE FROM oseba WHERE id = ?", (id, ))
    redirect('/osebe')

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
    return rtemplate('dodaj_goro.html')

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
    return rtemplate('drustva.html', drustva=drustva)

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
# conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=DB_PORT)
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