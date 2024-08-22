# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 08:48:50 2024

@author: priwi
peterpriwitzer@gmail.com
"""


import csv
from collections import defaultdict
from datetime import datetime

def Verbrauch_berechnung(data):
    # logische nachfolge : kennzeichen /datum zeit
    data = sorted(data, key=lambda x: (x[4], datetime.strptime(x[1] + ' ' + x[2], '%d.%m.%Y %H:%M')))  # Seřadit podle SPZ, datumu a času
    result = []  # lerere list 
    for i in range(len(data)):
        current_record = data[i]
        if i == 0 or current_record[3] == 0:
            verbrauch = 0  # Wenn verbrauch =0 stellt man  0
            abgelaufene_km = 0  # gleiche
        else:
            prev_record = data[i-1] # data vor !!! wichtig
            if prev_record[4] == current_record[4]:  # gleiche kenzeichen
                abgelaufene_km = current_record[3] - prev_record[3]    # abgelaufene Km berechniug
                menge = current_record[6]   # Verbrauch
                if abgelaufene_km != 0:
                    verbrauch = round((menge / abgelaufene_km) * 100, 2)   # 100 Km/l berechnug
                else:
                    verbrauch = 0
            else:
                verbrauch = 0  # erste reie in daten muss = 0 
                abgelaufene_km = 0  # erste reie in daten muss = 0
        # beendigung
        current_record = list(current_record)
        current_record.insert(4, round(abgelaufene_km, 2))  # Přidat sloupec ubehnute_km hned za stav_pocitadla_Km
        current_record.insert(8, round(verbrauch, 2))  # Přidat sloupec spotřeby hned za sloupec menge
        result.append(tuple(current_record))
        
    return result

def calculate_totals(records):
    # Berechnuge in grupen
        # Zusamen km 
    total_abgelaufene_km = sum(float(record[4]) for record in records)
        #komplete diesel/adblue/benzin
    total_menge = sum(float(record[7]) for record in records)
        # komplet preis PHM
    total_gesamte_preis = sum(float(record[10]) for record in records)
        # steur zusamen        
    total_steuer_preis = sum(float(record[12]) for record in records)
    
    return round(total_abgelaufene_km, 2), round(total_menge, 2), round(total_gesamte_preis, 2), round(total_steuer_preis, 2)
 
def Durchnit_Verbrauch(records):
    consumptions = [float(record[8]) for record in records if float(record[8]) > 0]
    # Pokud jsou celkové ujeté kilometry nenulové, vypočítá průměrnou spotřebu
    if consumptions:
        average_consumption = sum(consumptions) / len(consumptions)
    else:
        # 0 = wen komplette abgelaufene km sim 0
        average_consumption = 0
    return round(average_consumption, 2)

def process_fuel_data(diesel_data, adblue_data, benzin_data, filename):
    # definicia stlpcov 
    columns = [
        "ID", "Datum", "Zeit", "Der aktuelle Status des Km", "Laufene Km", "Kennzeichen", "Tankstelle", "Menge", 
        "Verbrauch", "Preis pro liter", "Gesamte preis", "Steuer", "Steuer preis", 
        "Gas", "alternativ adresse", "Google link"
    ]
    
    # jede kennzeiche extra
    vehicles = defaultdict(lambda: {'diesel': [], 'adblue': [], 'benzin': []})
    
    # Komby / zusamenpasung kennzeichen/Gas
    for record in diesel_data:
        vehicles[record[4]]['diesel'].append(record)
    for record in adblue_data:
        vehicles[record[4]]['adblue'].append(record)
    for record in benzin_data:
        vehicles[record[4]]['benzin'].append(record)
    
    # daten zum logischen denkung einpassen 
    sorted_combined_data = []
    for spz, records in vehicles.items():
        if sorted_combined_data:
            sorted_combined_data.extend([('',) * len(columns), ('',) * len(columns)])  # 2 frei raine zwischen kennzaiche
        if records['diesel']:
            diesel_records = Verbrauch_berechnung(records['diesel'])
            sorted_combined_data.extend(diesel_records)
            total_ubehnute_km, total_menge, total_gesamte_preis, total_steuer_preis = calculate_totals(diesel_records)
            average_consumption = Durchnit_Verbrauch(diesel_records)
            sorted_combined_data.append(('', '', '', '', total_ubehnute_km, '', '', total_menge, average_consumption, '', total_gesamte_preis, '', total_steuer_preis, '', '', ''))  # Souhrnné hodnoty pro Diesel
        if records['adblue']:
            sorted_combined_data.append(('',) * len(columns))  # ! freie raje zwische
            adblue_records = Verbrauch_berechnung(records['adblue'])
            sorted_combined_data.extend(adblue_records)
            total_ubehnute_km, total_menge, total_gesamte_preis, total_steuer_preis = calculate_totals(adblue_records)
            average_consumption = Durchnit_Verbrauch(adblue_records)
            sorted_combined_data.append(('', '', '', '', total_ubehnute_km, '', '', total_menge, average_consumption, '', total_gesamte_preis, '', total_steuer_preis, '', '', ''))  # Souhrnné hodnoty pro AdBlue
        if records['benzin']:
            sorted_combined_data.append(('',) * len(columns))  # 
            benzin_records = Verbrauch_berechnung(records['benzin'])
            sorted_combined_data.extend(benzin_records)
            total_ubehnute_km, total_menge, total_gesamte_preis, total_steuer_preis = calculate_totals(benzin_records)
            average_consumption = Durchnit_Verbrauch(benzin_records)
            sorted_combined_data.append(('', '', '', '', total_ubehnute_km, '', '', total_menge, average_consumption, '', total_gesamte_preis, '', total_steuer_preis, '', '', ''))  # Souhrnné hodnoty pro Benzin
    
    # HURAAAAAAAAAAAAAAAAAAA CSV WRITE   --- A ze to nepojde kua kua
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(columns)  # Zapsat názvy sloupců
        writer.writerows(sorted_combined_data)  # Zapsat data
    
    
    return sorted_combined_data
