# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 23:45:35 2024

@author: priwi
peterpriwitzer@gmail.com
"""

import sqlite3           ## Svina zasrata neznasam ta ! ale za to isla velice dobre tentok rat 

# verknupfung databaze / neu stellen
conn = sqlite3.connect('Verbrauch.db')


cur = conn.cursor()

# Diesel/AdBlue/Benzin  karte   alle sind gleiche 
cur.execute('''CREATE TABLE IF NOT EXISTS Diesel (
                id INTEGER PRIMARY KEY,
                datum TEXT,
                zeit TEXT,
                km REAL,
                kennzeichen TEXT,
                tankstelle TEXT,
                menge REAL,
                preis_pro_l REAL,
                gesamte_preis REAL,
                steuer REAL,
                inklusiv_steuer REAL,
                gas TEXT,
                formatted_address TEXT,
                link TEXT)''')


cur.execute('''CREATE TABLE IF NOT EXISTS AdBlue (
                id INTEGER PRIMARY KEY,
                datum TEXT,
                zeit TEXT,
                km REAL,
                kennzeichen TEXT,
                tankstelle TEXT,
                menge REAL,
                preis_pro_l REAL,
                gesamte_preis REAL,
                steuer REAL,
                inklusiv_steuer REAL,
                gas TEXT,
                formatted_address TEXT,
                link TEXT)''')


cur.execute('''CREATE TABLE IF NOT EXISTS Benzin (
                id INTEGER PRIMARY KEY,
                datum TEXT,
                zeit TEXT,
                km REAL,
                kennzeichen TEXT,
                tankstelle TEXT,
                menge REAL,
                preis_pro_l REAL,
                gesamte_preis REAL,
                steuer REAL,
                inklusiv_steuer REAL,
                gas TEXT,
                formatted_address TEXT,
                link TEXT)''')

# schpeichern 
conn.commit()
conn.close()
