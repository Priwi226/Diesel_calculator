# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 22:22:36 2024

@author: priwi
peterpriwitzer@gmail.com
"""

import PyPDF2
import re


import API_Google_maps
import Settings
import database_write

from datetime import datetime

def convert_date(date_str):
    # Parsovanie dátumu zo vstupného reťazca
    date = datetime.strptime(date_str, "%d/%m/%Y")
    # Formátovanie dátumu do požadovaného formátu
    formatted_date = date.strftime("%d.%m.%Y")
    return formatted_date



def extract_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        text = ''
        for page_num in range(reader.numPages):
            text += reader.getPage(page_num).extractText()
            

    
    # Oddelenie údajov do riadkov   # daten teilen
    lines = text.split('\n')
    
    # Inicializácia prázdneho zoznamu pre údaje    # lerere list
    data = []
    
    # Regulárny výraz pre identifikáciu riadkov s potrebnými údajmi   # regularische beteilung 
    regex = r"(\d{2}/\d{2}/\d{4}) (\d{2}:\d{2}) (\d+) ([A-Z0-9]+) (.*?) (\d+\.\d+) (\d+\.\d+) (\d+\.\d+) (\d+%) (\d+\.\d+)"

    for line in lines:
        # Nájdenie údajov pomocou regulárneho výrazu  # duchr regularische zeichner finden die zechnung
        match = re.match(regex, line)
        if match:
            # Rozdelenie riadku na jednotlivé skupiny   ## geteilung zum reie
            datum = match.group(1)
            zeit = match.group(2)
            km = match.group(3)
            kennzeichen = match.group(4)
            tankstelle = match.group(5)
            menge = match.group(6)
            preis_pro_Liter = match.group(7)
            gesamte_preis = match.group(8)
            steuer = match.group(9)
            inklusiv_steuer = match.group(10)
            
            # Vytvorenie slovníka pre tento riadok a pridanie do zoznamu   ## name eingeben
            row = {
                "Datum": datum,
                "Zeit": zeit,
                "KM": km,
                "Kennzeichen": kennzeichen,
                "Tansktelle": tankstelle,
                "Menge": menge,
                "Preis pro Liter": preis_pro_Liter,
                "Gesamte_preis": gesamte_preis,
                "Steuer": steuer,
                "Inklusiv_steuer": inklusiv_steuer
            }
            
            #  extrahovanie paliv 
            tankstelle_parts = tankstelle.split()
            gas = tankstelle_parts[-1]
            tankstelle = ' '.join(tankstelle_parts[:-1])
            if gas == "Blue":
                gas = "AdBlue"
            
            datum = (row["Datum"])      
            datum = convert_date(datum)
            
            zeit = (row["Zeit"])
            km = (row["KM"])
            kennzeichen = (row["Kennzeichen"])
            #tankstelle = (row["Tansktelle"])
            menge = (row["Menge"])
            preis_pro_l = (row["Preis pro Liter"])
            gesamte_preis = (row["Gesamte_preis"])
            steuer = (row["Steuer"])
            inklusiv_steuer = (row["Inklusiv_steuer"])
            print ("\n\n\nDatum: " + datum + "\nZeit: " + zeit + "\nKM: " + km + "\nKenzeichen: " + kennzeichen + "\nTankstelle: " + tankstelle + "\nGas: " + gas + "\nMenge: " + menge + "\nPreis_pro_l: " + preis_pro_l + "\nGesamte_preis: " + gesamte_preis + "\nsteuer: " + steuer + "\nPreis inklusinv steuer : " + inklusiv_steuer)
            
            try:
                if Settings.api == 1:
                    formatted_address, link = API_Google_maps.geocode(tankstelle)
                    # print("\n" + formatted_address + "\n" + link)
                else:
                    formatted_address = " "
                    link = " "
            except:
                formatted_address = " "
                link = " "
                    
             
                tankstelle = (row["Tansktelle"])
                # print(datum + zeit + km + kennzeichen + tankstelle + menge + preis_pro_l + gesamte_preis + steuer + inklusiv_steuer + gas)
            if gas == "Diesel" or gas == "AdBlue" or gas == "Benzin":
                database_write.daten_schreibe(gas, datum, zeit, km, kennzeichen, tankstelle, menge, preis_pro_l, gesamte_preis, steuer, inklusiv_steuer, gas, formatted_address, link)
            

            
    # return datum, zeit, km, kennzeichen, tankstelle, menge, preis_pro_l, gesamte_preis, steuer, inklusiv_steuer, gas
    # if Settings.api == 1: 
    #     return datum, zeit, km, kennzeichen, tankstelle, menge, preis_pro_l, gesamte_preis, steuer, inklusiv_steuer, gas, formatted_address, link 
    # else:
    #     return datum, zeit, km, kennzeichen, tankstelle, menge, preis_pro_l, gesamte_preis, steuer, inklusiv_steuer, gas
# Funkcion anfrufen
#file = ("c:/testovanie/V1,5/tanken.pdf")
#extract_pdf(file)

