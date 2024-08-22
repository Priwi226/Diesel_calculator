# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 00:31:54 2024

@author: priwi
peterpriwitzer@gmail.com
"""

import sqlite3
from datetime import datetime 

def convert_datum(datum):
    #### tu moze vznikat ten skurveny buck !!!
    datum_objekt = datetime.strptime(datum, "%d.%m.%Y")
    prevod_na_str = str(datum_objekt)
    return prevod_na_str
    
def lese_datenbank(anfangsdatum, enddatum, diesel_output, adblue_output, benzin_output):
    print(f"Anfangsdatum: {anfangsdatum}{type}")
    print(f"Enddatum: {enddatum}{type}")
    #### WICHTIG BUG aus die reie 20-23 nur 21 frei lassen sonst ist falsche datum format. Warum ? //kein ahnung
    # anfangsdatum = convert_datum(anfangsdatum)
    enddatum = convert_datum(enddatum)
    # anfangsdatum = (str(anfangsdatum))
    # enddatum = (str(enddatum))
    # print(f"Anfangsdatum: {anfangsdatum}{type}")
    # print(f"Enddatum: {enddatum}{type}")
    # ####### SQLite verknupfung 
    # print("Verbindung zur Datenbank herstellen...")
    conn = sqlite3.connect('Verbrauch.db')
    c = conn.cursor()
    # print("Verbindung zur Datenbank erfolgreich hergestellt.")


    diesel_data = []
    adblue_data = []
    benzin_data = []

    # datensuchen in databaze 
    if diesel_output:
        print("Durchführen der Abfrage auf die Diesel-Tabelle...")
        c.execute("SELECT * FROM Diesel WHERE datum BETWEEN ? AND ?", (anfangsdatum, enddatum))
        diesel_data = c.fetchall()
        print("Abfrage auf die Diesel-Tabelle erfolgreich durchgeführt.")

    if adblue_output:
        print("Durchführen der Abfrage auf die AdBlue-Tabelle...")
        c.execute("SELECT * FROM AdBlue WHERE datum BETWEEN ? AND ?", (anfangsdatum, enddatum))
        adblue_data = c.fetchall()
        print("Abfrage auf die AdBlue-Tabelle erfolgreich durchgeführt.")

    if benzin_output:
        print("Durchführen der Abfrage auf die Benzin-Tabelle...")
        c.execute("SELECT * FROM Benzin WHERE datum BETWEEN ? AND ?", (anfangsdatum, enddatum))
        benzin_data = c.fetchall()
        print("Abfrage auf die Benzin-Tabelle erfolgreich durchgeführt.")

    # Zavření připojení k databázi
    print("Verbindung beendung")
    conn.close()

    # PRINT Daten 
    print("\nDiesel-Tabelle:\n", diesel_data)
    print("\nAdBlue-Tabelle:\n", adblue_data)
    print("\nBenzin-Tabelle:\n", benzin_data)

    return diesel_data, adblue_data, benzin_data


# anfangsdatum = '01.05.2024'
# enddatum = '07.06.2024'

# print(f"!!!!!!!!!!!!! anfang: {anfangsdatum}, type: {type(anfangsdatum)}")
# print(f"!!!!!!!!!!!!! enddatum: {enddatum}, type: {type(enddatum)}")

    # posrati datum a format 
    # predpokladam dovod bugu v subore Verbraucht kde sa formatovanie urcuje trochu inak ako pri vkladani priamo do databy !!! //Nemusi byt pravda ""nechce sa mi testovat ""
# diesel_output = 1
# adblue_output = 1
# benzin_output = 1

# lese_datenbank(anfangsdatum, enddatum, diesel_output, adblue_output, benzin_output)
