#!/usr/bin/python
# -*- encoding: utf-8 -*-

# uvozimo bottle.py
from bottle import *
    #import sqlite3
import hashlib
import datetime

# povezava do datoteke baza
    #baza_datoteka = 'pohodnistvo.db' 

# uvozimo ustrezne podatke za povezavo
import auth_public as auth

# uvozimo psycopg2
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki

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
    return '<h1>Stran ne obstaja</h1><img src="https://upload.wikimedia.org/wikipedia/commons/d/d4/S%C3%B8ren_Kierkegaard_%281813-1855%29_-_%28cropped%29.jpg" style="width:300px;height:450px;" alt="Kierkegaard"><h2>Tudi Kierkegaard se je spraševal o obstoju, nisi edini</h2><a href="/pohodnistvo", font-size:px>Nazaj na začetno stran.</a>'

@error(403)
def napaka403(error):
    return '<h1>Do te strani nimaš dostopa!</h1><a href="/pohodnistvo", font-size:px>Nazaj na začetno stran.</a>'


def javiNapaka(napaka = None):
    sporocilo = request.get_cookie("napaka", secret=skrivnost)
    if napaka is None:
        response.delete_cookie('napaka')
    else:
        #path doloca za katere domene naj bo napaka, default je cela domena
        response.set_cookie('napaka', napaka, path="/", secret=skrivnost)
    return sporocilo

skrivnost = "NekaVelikaDolgaSmesnaStvar"

def dostop():
    uporabnik = request.get_cookie("uporabnik", secret=skrivnost)
    cur = baza.cursor()
    #povezava na bazo ne deluje, oziroma bere bazo kot prazno? HELP pls
    if uporabnik:
        cur.execute("""
                    SELECT polozaj FROM oseba 
                    WHERE uporabnik = %s""", (uporabnik,))
        polozaj = cur.fetchone()
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
    dostop
    #če prijavljen/registriran potem glavna_stran.html stran sicer prijava.html
    redirect('/pohodnistvo')

@get('/pohodnistvo')
def glavna_stran():
    dostop()
    return rtemplate('glavna_stran.html', 
                    naslov='Pohodništvo')

@get('/o_projektu')
def o_projektu():
    return rtemplate('o_projektu.html')

######################################################################
# PRIJAVA / REGISTRACIJA

#zakodirajmo geslo
def hashGesla(s):
    m = hashlib.sha256()
    m.update(s.encode("utf-8"))
    return m.hexdigest()

@get('/registracija')
def registracija_get():
    napaka = javiNapaka()
    return rtemplate('registracija.html', 
                    naslov='Registracija', 
                    napaka = napaka)

@post('/registracija')
def registracija_post():
    #poberimo vnesene podatke
    identiteta = request.forms.identiteta
    uporabnik = request.forms.uporabnik
    geslo = request.forms.geslo
    cur = baza.cursor()
    iden = None

    try: 
        cur.execute("""
                    SELECT ime FROM oseba 
                    WHERE id = %s""", (identiteta,))
        iden = cur.fetchone()
    except:
        iden = None

    if iden is None:
        #id ne obstaja, ni član društva
        javiNapaka(napaka="Nisi (še) član društva, zato tvoj ID ne obstaja v bazi")
        redirect('/registracija')
        return

    if len(geslo)<4:
        #dolzina gesla
        javiNapaka(napaka="Geslo prekratko. Dolžina gesla mora biti vsaj 5")
        redirect('/registracija')
        return

    cur.execute("""
                SELECT id FROM oseba 
                WHERE uporabnik = %s""", (uporabnik,))
    
    identiteta2 = cur.fetchone()
    if identiteta2 != None and identiteta != identiteta2:
        #enolicnost uporabnikov
        javiNapaka(napaka="To uporabniško ime je zasedeno")
        redirect('/registracija')
        return

    zgostitev = hashGesla(geslo)
    #brez str() ima lahko težave s tipom podatkov
    cur.execute("UPDATE oseba SET uporabnik = %s, geslo = %s, polozaj = %s WHERE id = %s", (str(uporabnik), str(zgostitev), 0, str(identiteta)))
    #dolocimo osebo ki uporablja brskalnik (z njo dolocimo cookie)
    response.set_cookie('uporabnik', uporabnik, secret=skrivnost)
    redirect('/pohodnistvo')

@get('/prijava')
def prijava():
    napaka = javiNapaka()
    return rtemplate('prijava.html', 
                    naslov='Prijava', 
                    napaka=napaka)

@post('/prijava')
def prijava_post():
    #poberimo vnesene podatke
    uporabnik = request.forms.uporabnik
    geslo = request.forms.geslo
    cur = baza.cursor()
    hashGeslo = None
    try: 
        cur.execute("SELECT geslo FROM oseba WHERE uporabnik = %s", (uporabnik,))
        hashGeslo = cur.fetchone()
        hashGeslo = hashGeslo[0]
    except:
        hashGeslo = None
    if hashGeslo is None:
        javiNapaka('Niste še registrirani')
        redirect('/prijava')
        return
    if hashGesla(geslo) != hashGeslo:
        javiNapaka('Geslo ni pravilno')
        redirect('/prijava')
        return
    response.set_cookie('uporabnik', uporabnik, secret=skrivnost)
    redirect('/pohodnistvo')

@get('/odjava')
def odjava():
    response.delete_cookie('uporabnik')
    response.delete_cookie('identiteta')
    redirect('/prijava')
    
######################################################################
# MOJE DRUŠTVO

@get('/moje_drustvo')
def moje_drustvo():
    user = dostop()
    uporabnik = str(user[0])
    cur = baza.cursor()

    cur.execute("""SELECT drustvo FROM oseba 
                WHERE uporabnik = %s""", (uporabnik,))
    drustvo = cur.fetchone()

    cur.execute("""SELECT id, ime, priimek, spol, starost 
                FROM oseba WHERE drustvo = %s 
                ORDER BY oseba.priimek""", (str(drustvo[0]),))
    osebe = cur.fetchall()

    polozaj = int(user[1])
    return rtemplate('moje_drustvo.html', 
                    osebe=osebe, 
                    polozaj = polozaj)


@get('/osebe/dodaj_osebo_drustvo')
def dodaj_osebo_drustvo():
    user = dostop()
    if int(user[1]) > 0:
        redirect('/osebe/dodaj_osebo')
    else:
        return napaka403(error)

######################################################################
# OSEBE

@get('/osebe')
def osebe():
    user = dostop()
    cur = baza.cursor()
    cur.execute("""
                SELECT id, ime, priimek, spol, starost, drustvo FROM oseba
                ORDER BY oseba.priimek""")
    osebe = cur.fetchall()
    if int(user[1]) == 2:
        return rtemplate('osebe.html', 
                        osebe=osebe, 
                        naslov='Pohodniki')
    else:
        return napaka403(error)

@get('/osebe/dodaj_osebo')
def dodaj_osebo():
    user = dostop()
    cur.execute("""
                SELECT drustva.ime FROM drustva
                ORDER BY drustva.ime""")
    drustvo = cur.fetchall()
    #naredimo list iz tuple
    drustvo = [x[0] for x in drustvo]
    
    if int(user[1]) == 2:
        return rtemplate('dodaj_osebo.html', 
                        drustvo=drustvo)
    else:
        return napaka403(error)

@post('/osebe/dodaj_osebo')
def dodaj_osebo_post():
    ime = request.forms.get('ime')
    priimek = request.forms.get('priimek')
    spol = request.forms.get('spol')
    if spol == 'Male':
        pass
    else:
        spol = 'Female'
    starost = request.forms.get('starost')
    drustvo = request.forms.get('drustvo')
    cur = baza.cursor()
    cur.execute("""INSERT INTO oseba (ime, priimek, spol, starost, drustvo) 
                VALUES (%s, %s, %s, %s, %s)""", (ime, priimek, spol, starost, drustvo))
    redirect('/osebe')

@get('/osebe/uredi/<identiteta>')
def uredi_osebo(identiteta):
    user = dostop()
    cur = baza.cursor()
    response.set_cookie('identiteta',identiteta,secret=skrivnost)

    cur.execute("""SELECT drustva.ime FROM drustva ORDER BY drustva.ime""")
    drustvo = cur.fetchall()
    #naredimo list iz tupla
    drustvo = list(drustvo)

    #bomo dali v naslov tab-a
    cur.execute("""SELECT ime, priimek 
                FROM oseba WHERE id = %s""", (str(identiteta),))
    ime = cur.fetchone()

    #jaz sem ta ki uporablja brskalnik
    cur.execute("""SELECT id FROM oseba 
                WHERE uporabnik = %s""", (str(user[0]),))
    jaz = cur.fetchone()

    #oseba katere stran urejam
    cur.execute("""SELECT id, ime, priimek, spol, starost, drustvo 
                FROM oseba WHERE id = %s""", (identiteta,))
    oseba = cur.fetchone()

    if identiteta == jaz or int(user[1])==2:
        return rtemplate('oseba-edit.html', 
                        oseba=oseba, 
                        drustvo=drustvo, 
                        naslov="Urejanje "+ime[0]+' '+ime[1])
    else:
        return napaka403(error)

@post('/osebe/uredi/<identiteta>')
def uredi_osebo_post(identiteta):
    ime = request.forms.get('ime')
    priimek = request.forms.get('priimek')
    spol = request.forms.get('spol')
    starost = request.forms.get('starost')

    cur = baza.cursor()
    cur.execute("UPDATE oseba SET ime = %s, priimek = %s, spol = %s, starost = %s WHERE id = %s", 
                (str(ime), str(priimek), str(spol), int(starost), int(identiteta)))
    redirect('/moje_drustvo')


@post('/osebe/brisi/<identiteta>')
def brisi_osebo(identiteta):
    user = dostop()
    if int(user[1])==2:
        cur.execute("DELETE FROM oseba WHERE id = %s", (identiteta,))
    else:
        return napaka403(error)
    redirect('/osebe')

@get('/osebe/<identiteta>')
def lastnosti_osebe(identiteta):
    user = dostop()
    #dolocim identiteto osebe, kjer bom brskal (admin ni nujno enak identiteti kjer ureja)
    response.set_cookie('identiteta',identiteta,secret=skrivnost)

    cur = baza.cursor()

    cur.execute("SELECT drustvo FROM oseba WHERE uporabnik = %s", (str(user[0]),))
    drustvo = cur.fetchone()
    cur.execute("SELECT drustvo FROM oseba WHERE id = %s", (identiteta,))
    drustvoID = cur.fetchone()
    cur.execute("""SELECT id, ime, priimek, spol, starost, drustvo 
                FROM oseba WHERE id = %s""", (identiteta,))
    oseba = cur.fetchone()

    #ta ki lahko dodaja hribe v tabelo obiskani za določenega posameznika je admin in oseba sama
    cur.execute("SELECT id FROM oseba WHERE uporabnik = %s", (str(user[0]),))
    jaz = cur.fetchone()
    #to preverim s spremenljivko dodaj, ki je true kadar lahko dodam
    dodaj = False
    if jaz[0] == identiteta or user[1]==2:
        dodaj = True

    #najvisji osvojen vrh
    cur.execute("""
                SELECT visina, ime FROM gore 
                WHERE id IN 
                (SELECT id_gore FROM obiskane 
                WHERE id_osebe = %s) ORDER BY gore.visina""", (identiteta,))
    najvisji_osvojen_vrh = cur.fetchall()
    if najvisji_osvojen_vrh != []:
        najvisji_osvojen_vrh = najvisji_osvojen_vrh[-1]
    else:
        najvisji_osvojen_vrh = (None, None)

    #stevilo gora, na katerih je bil pohodnik
    cur.execute("""
                SELECT COUNT(id_gore) FROM obiskane
                WHERE id_osebe = %s""", (identiteta,))
    stevilo_osvojenih_gor = cur.fetchone()

    #vse gore na katerih je bil/bila
    #izberem zeljene podatke iz gore za nek id v
    # ('where id in', ker 'where id =' dela samo za enega) id_gore iz obiskanih, kjer id isti kot stran 
    cur.execute("""
                SELECT id, ime, visina, gorovje, drzava FROM gore 
                WHERE id IN (SELECT id_gore FROM obiskane
                WHERE id_osebe = %s) ORDER BY ime""", (identiteta,))
    vse_osvojene_gore = cur.fetchall()
    
    for i in range(len(vse_osvojene_gore)):
        identiteta_gore = (vse_osvojene_gore[i])[0]
        cur.execute("""
                    SELECT leto_pristopa FROM obiskane
                    WHERE id_gore = %s""", (identiteta_gore,))
        leto_pristopa_gora = cur.fetchone()

        vse_osvojene_gore[i] = list(vse_osvojene_gore[i])
        vse_osvojene_gore[i].pop(0)
        vse_osvojene_gore[i].append(leto_pristopa_gora[0])

    if drustvo == drustvoID or int(user[1])==2:
        return rtemplate('oseba-id.html',  
                        oseba=oseba, 
                        stevilo_osvojenih_gor=stevilo_osvojenih_gor[0],
                        najvisji_osvojen_vrh=najvisji_osvojen_vrh, 
                        vse_osvojene_gore=vse_osvojene_gore,
                        naslov='Pohodnik {0} {1}'.format(oseba[1], oseba[2]), 
                        identiteta=identiteta, 
                        dodaj=dodaj)
    else:
        return napaka403(error)

@get('/osebe/dodaj goro')
def osvojena_gora():
    dostop()
    cur = baza.cursor()
    cur.execute("""SELECT id, prvi_pristop, ime, visina, gorovje, drzava 
                FROM gore ORDER BY ime""")
    gore = cur.fetchall()
    return rtemplate('dodaj_osvojeno_goro.html', 
                    gore=gore, 
                    naslov='Nov osvojen hrib')

@post('/osebe/dodaj goro')
def osvojena_gora_post():
    cur = baza.cursor()
    #seznam gora
    gore = cur.execute("SELECT id FROM gore")
    gore = list(cur.fetchall())

    identiteta = request.get_cookie('identiteta', secret=skrivnost)

    #osvojene gore
    cur.execute("SELECT id_gore, leto_pristopa FROM obiskane WHERE id_osebe = %s",(identiteta,))
    prej_osvojene_vse = cur.fetchall()
    prej_osvojene = [i[0] for i in prej_osvojene_vse]
    osvojene = []

    time = datetime.datetime.now()

    #cursor nam vrne seznam tuplov [(int,), ...]
    for i in gore:
        #element gore je tuple oblike (integer,)
        i=i[0]
        #zapeljem se čez vse gore in pogledam, če je že osvojen
        j = request.forms.get(str(i))
        if j and int(j) not in prej_osvojene:
            leto = int(time.year)
            osvojene.append((int(j),leto))
    
    if prej_osvojene_vse != []:
        for i in prej_osvojene_vse:
            osvojene.append(i)
    #sčistim bazo že osvojenih za naš id in dodam osvojene in leto
    cur.execute("DELETE FROM obiskane WHERE id_osebe = %s", (identiteta,))
    for gora in osvojene:
        cur.execute("INSERT INTO obiskane (id_gore, id_osebe, leto_pristopa) VALUES (%s, %s, %s)",(int(gora[0]), str(identiteta), gora[1]))
    redirect('/osebe/'+str(identiteta))


######################################################################
# GORE

@get('/gore')
def gore():
    cur = baza.cursor()
    cur.execute("""
                SELECT prvi_pristop, ime, visina, gorovje, drzava 
                FROM gore ORDER BY ime
                """)
    gore = cur.fetchall()
    return rtemplate('gore.html', gore=gore)

@get('/gore/dodaj goro')
def dodaj_goro():
    dostop()
    cur = baza.cursor()
    cur.execute("""
                SELECT gorovje.ime FROM gorovje
                ORDER BY gorovje.ime
                """)
    gorovje = cur.fetchall()
    #naredimo list iz tuple
    gorovje = [x[0] for x in gorovje]

    cur.execute("""
                SELECT drzave.ime FROM drzave
                ORDER BY drzave.ime
                """)
    drzave = cur.fetchall()
    drzave = [y[0] for y in drzave]

    return rtemplate('dodaj_goro.html', 
                    gorovje=gorovje, 
                    drzave=drzave, 
                    naslov='Dodaj goro')

@post('/gore/dodaj goro')
def dodaj_goro_post():
    ime = request.forms.get('ime_gore')
    visina = request.forms.get('visina')
    prvi_pristop = request.forms.get('prvi_pristop')
    drzava = request.forms.get('drzava')
    gorovje = request.forms.get('gorovje')

    cur = baza.cursor()

    cur.execute("""INSERT INTO gore (prvi_pristop, ime, visina, gorovje, drzava)
        VALUES (%s, %s, %s, %s, %s)""",
         (int(prvi_pristop), str(ime), int(visina), str(gorovje), str(drzava)))
    redirect('/gore')

######################################################################
# DRUSTVA

@get('/drustva')
def drustva():
    user = dostop()
    cur = baza.cursor()
    cur.execute("""
                SELECT id, ime, leto_ustanovitve FROM drustva
                ORDER BY drustva.ime
                """)
    drustva = cur.fetchall()
    return rtemplate('drustva.html', 
                    drustva=drustva, 
                    naslov='Društva')

@get('/drustva/<ime>')
def drustva_id(ime):
    user = dostop()
    cur = baza.cursor()
    cur.execute("""
                SELECT id, ime, leto_ustanovitve FROM drustva
                WHERE ime = %s""",(ime,))
    drustvo = cur.fetchone()

    cur.execute("""
                SELECT COUNT (oseba.drustvo) FROM oseba
	            WHERE oseba.drustvo = 
                (SELECT ime FROM drustva WHERE ime = %s)""",(ime,))
    stevilo_clanov_drustvo = cur.fetchone()

    cur.execute("""
                SELECT id, ime, priimek, spol, starost FROM oseba
	            WHERE oseba.drustvo = 
                (SELECT ime FROM drustva WHERE ime = %s)""",(ime,))
    clani_drustva = cur.fetchall()

    stevilo_vseh = 0
    najvisja_gora = [0,None]
    for clan in clani_drustva:
        identiteta = clan[0]
        #stevilo osvojenih gora za posameznika
        cur.execute("""
                    SELECT COUNT (id_gore) FROM obiskane 
                    WHERE id_osebe = %s""",(identiteta,))
        
        osvojenih_gora = cur.fetchone()
        stevilo_vseh += osvojenih_gora[0]

        #najvisja gora za posameznika
        cur.execute("""
                    SELECT visina, ime FROM gore WHERE 
                    id IN (SELECT id_gore FROM obiskane 
                    WHERE id_osebe = %s) ORDER BY visina""", (identiteta,))
        najvisji_osvojen_vrh = cur.fetchall()

        if najvisji_osvojen_vrh != []:
            najvisji_osvojen_vrh = najvisji_osvojen_vrh[-1]
            if najvisji_osvojen_vrh[1] is not None and najvisji_osvojen_vrh[0] is not None:
                if najvisja_gora[0] <= najvisji_osvojen_vrh[0]:
                    najvisja_gora = najvisji_osvojen_vrh

    #naredimo list iz tuple
    clani_drustva = [(x[1], x[2], x[3], x[4]) for x in clani_drustva]       

    if int(user[1]) == 2:
        return rtemplate('drustvo-id.html', 
                        drustvo=drustvo,
                        stevilo_clanov_drustvo=stevilo_clanov_drustvo[0],
                        clani_drustva=clani_drustva,
                        naslov='Društvo {0}'.format(ime), 
                        vse = stevilo_vseh, 
                        najvisja = najvisja_gora)
    else:
        return napaka403(error)
        
######################################################################
# Za STATIC datoteke(slike)

@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='static')

######################################################################
# Glavni program

#baza sqlite3 v tej mapi (pohodnistvo.db)
    #baza = sqlite3.connect(baza_datoteka, isolation_level=None)
    #baza.set_trace_callback(print) # izpis sql stavkov v terminal (za debugiranje pri razvoju)
    #cur = baza.cursor()

# priklopimo se na bazo na fmf
baza = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=DB_PORT)
baza.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

cur = baza.cursor(cursor_factory=psycopg2.extras.DictCursor)

# zapoved upoštevanja omejitev FOREIGN KEY
#cur.execute("PRAGMA foreign_keys = ON;")

# poženemo strežnik na podanih vratih, npr. http://localhost:8080/
run(host='localhost', port=SERVER_PORT, reloader=RELOADER)