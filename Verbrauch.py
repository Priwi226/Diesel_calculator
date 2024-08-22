# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 18:34:04 2024

@author: priwi
peterpriwitzer@gmail.com
"""

#import
import tkinter as tk
from tkinter import ttk, filedialog
from tkcalendar import Calendar
import subprocess
import os

# import filles / moduls
from extrac_pdf import extract_pdf
import database_read
import mixer 

def importpdf():
    file_path = filedialog.askopenfilename()
    if file_path:
        database_input.delete(0, tk.END)  # texte loschen
        database_input.insert(0, file_path)  # Weg zum fille
        database_adresse = database_input.get()  # Ubersetung zu variable
        print(database_adresse)
        extract_pdf(database_adresse)
        
def update_outputs():
    global Diesel_output, Adblue_output, Benzin_output
    Diesel_output = diesel_fiereck_var.get()
    Adblue_output = adblue_fiereck_var.get()
    Benzin_output = benzin_fiereck_var.get()

def output():
    anfangsdatum = anfang_date_entry.get_date()
    enddatum = endes_date_entry.get_date()
    print(f"Anfangsdatum from Calendar: {anfangsdatum}")
    print(f"Enddatum from Calendar: {enddatum}")
    # database anrufen -- lesen 
    diesel, adblue, benzin = database_read.lese_datenbank(anfangsdatum, enddatum, Diesel_output, Adblue_output, Benzin_output)
    #   notwebding fur weitere ablauf  -- None --ee
    if diesel == None:
        diesel = " "
    if adblue == None:
        adblue = " "
    if benzin == None:
        benzin = " "
    combined_data = mixer.process_fuel_data(diesel, adblue, benzin, 'Verbrauch_daten.csv')   # Daten mixer :D  kokotina picovina ku#va...
    print(diesel)
    print(adblue)
    print(benzin)
    csv_file_path = 'Verbrauch_daten.csv'

    # kontrole ob der fille existiert nicht vieleicht 
    if os.path.isfile(csv_file_path):
        # Ofenn in system vorgestelte program 
        if os.name == 'nt':  # Windows
            os.startfile(csv_file_path)
        elif os.name == 'posix':  # MacOS/Linux
            subprocess.run(['open', csv_file_path])
        else:
            print("Dein OS ist nicht unterschtutz fur diese script")
    else:
        print(f"Fille {csv_file_path} existiert nicht")
    
root = tk.Tk()
root.title("Verbrauch rechner")
root.geometry("800x400")

# Knopfe
run_button = ttk.Button(root, text="Ein CSV machen", padding=10, command=output)
run_button.grid(row=5, column=2, padx=10, pady=(0, 10), sticky="se")

exit_button = ttk.Button(root, text="Beenden", padding=10, command=root.destroy)
exit_button.grid(row=5, column=0, padx=10, pady=(0, 10), sticky="sw")

# Fields
database_input = ttk.Entry(root, width=50)
database_input.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="ew")

# vahlen knopf
file_dialog_button = ttk.Button(root, text="PDF Fille wahlen", command=importpdf)
file_dialog_button.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

# fiereck
diesel_fiereck_var = tk.IntVar()
diesel_fiereck = ttk.Checkbutton(root, text="Diesel", variable=diesel_fiereck_var, command=update_outputs)
diesel_fiereck.grid(row=1, column=1, padx=10, pady=10, sticky="w")

adblue_fiereck_var = tk.IntVar()
adblue_fiereck = ttk.Checkbutton(root, text="Ad blue", variable=adblue_fiereck_var, command=update_outputs)
adblue_fiereck.grid(row=1, column=2, padx=10, pady=10, sticky="w")

benzin_fiereck_var = tk.IntVar()
benzin_fiereck = ttk.Checkbutton(root, text="Benzin", variable=benzin_fiereck_var, command=update_outputs)
benzin_fiereck.grid(row=1, column=3, padx=10, pady=10, sticky="w")

# Kalendar     Tu bude vznikat ten skurveny bug asi 
anfang_date_entry = Calendar(root, date_pattern='dd.mm.yyyy')
anfang_date_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

endes_date_entry = Calendar(root, date_pattern='dd.mm.yyyy')
endes_date_entry.grid(row=2, column=2, padx=10, pady=10, sticky="w")

# wariable output
Diesel_output = 0
Adblue_output = 0
Benzin_output = 0

# fenster einstelungen min/max
root.minsize(width=250, height=250)
root.maxsize(width=1000, height=600)

# Add signature label
signature_label = ttk.Label(root, text="Production by PRIWI peterpriwitzer@gmail.com", font=("Helvetica", 10))
signature_label.grid(row=6, column=0, columnspan=3, pady=(10, 0))

root.mainloop()


