# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 00:31:54 2024

@author: priwi
peterpriwitzer@gmail.com
"""
import sqlite3

def databaze_kontrole(tablename, datum, zeit, kennzeichen, tankstelle):
    conn = sqlite3.connect('Verbrauch.db')
    cur = conn.cursor()
    sql_command = f'''SELECT * FROM {tablename}
                     WHERE datum = ? AND zeit = ? AND kennzeichen = ? AND tankstelle = ?'''
    data = (datum, zeit, kennzeichen, tankstelle)
    cur.execute(sql_command, data)
    daten_existiert  = cur.fetchone() is not None
    conn.close()
    return daten_existiert

def daten_schreibe(tablename, datum, zeit, km, kennzeichen, tankstelle, menge, preis_pro_l, gesamte_preis, steuer, inklusiv_steuer, gas, formatted_address, link):
    if databaze_kontrole(tablename, datum, zeit, kennzeichen, tankstelle):
        print("Daten existiert schon.")
        return
    conn = sqlite3.connect('Verbrauch.db')
    cur = conn.cursor()
    sql_command = f'''INSERT INTO {tablename} (datum, zeit, km, kennzeichen, tankstelle, menge, preis_pro_l, gesamte_preis, steuer, inklusiv_steuer, gas, formatted_address, link)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    data = (datum, zeit, km, kennzeichen, tankstelle, menge, preis_pro_l, gesamte_preis, steuer, inklusiv_steuer, gas, formatted_address, link)
    cur.execute(sql_command, data)
    conn.commit()
    conn.close()