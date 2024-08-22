# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 22:54:57 2024

@author: priwi
peterpriwitzer@gmail.com
"""

import requests
import Settings
import importlib

# Google maps funktion 
def geocode(adresa):
    importlib.reload(Settings)
    api_key = Settings.Googleapi   # Aus setting   es ist mein privat !!!! nicht weiter geben !!!
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={adresa}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    if data["status"] == "OK" and len(data["results"]) > 0:
        result = data["results"][0]
        formatted_address = result["formatted_address"]
        location = result["geometry"]["location"]
        latitude = location["lat"]
        longitude = location["lng"]
        link = f"https://maps.google.com/?q={latitude},{longitude}&elevation=N/A"
        return formatted_address, link