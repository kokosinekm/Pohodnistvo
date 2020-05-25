#!/usr/bin/python
# -*- encoding: utf-8 -*-

# uvozimo bottle.py
from bottle import *
import sqlite3
import hashlib

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

@get('/osebe')
def osebe():
    return rtemplate('osebe.html')

@get('/gore')
def gore():
    return rtemplate('gore.html')

@get('/drustva')
def drustva():
    return rtemplate('drustva.html')

######################################################################
# STRANI ZA DODAJANJE

@get('/dodaj_goro')
def dodaj_goro():
    return rtemplate('dodaj_goro.html')

@post('/dodaj_goro')
def dodaj_goro_post():
    #sql, ki bo dejansko dodal goro v tabelo
    redirect('/gore')

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

# poženemo strežnik na podanih vratih, npr. http://localhost:8080/
run(host='localhost', port=SERVER_PORT, reloader=RELOADER)