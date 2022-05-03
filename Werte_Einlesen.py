# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 10:19:17 2022

Tests zum Einlesen einer CSV-Datei

genutzte Module: tabulate

@author: Tobias Kurz
"""

import csv

#CSV-Reader bekommt Datei, mit Anweisung um welche Abstandshalter es sich handelt
with open('test.csv')as werte:
    csv_reader_object = csv.reader(werte, delimiter=';')
    
    zeilennummer = 0    #Zaehler für die Gesamtzeilenzahl
    counter = 0         #Zaehler für die Ausgegebenen Zeilen
    
    
    SucheZeile = int(input("Welche Zeile ausgeben? (für komplette Ausgabe 0 eingeben.) \n"))

    ergebnisse = [] #Hier werden Später die Zeilen abgelegt
    
    #Iteration der Zeilen durch den Reader, "row" immer die aktuell eingelesene Zeile
    #Indirekt können hierdurch bestimmte Zeilen ausgegeben werden
    for row in csv_reader_object:
        # Oberste Zeile -> Ueberschriften festlegen
        if zeilennummer == 0:
            beschriftung = ["Eintrag Nr."] + row # Einfügen einer Zaehlspalte in Spalte 1
        else:
            if zeilennummer == SucheZeile or SucheZeile == 0:
                ergebnisse.append([zeilennummer]+row) #befuellen der Ergebnisliste und Aufzaehlen der Zeilen
                counter += 1
        zeilennummer += 1


#  schöne Tabellenform
from tabulate import tabulate
print("\n")
print(tabulate(ergebnisse, headers=beschriftung))

#  Meldung bei zu hoher Zeilenangabe
if SucheZeile > (zeilennummer-1):
    print("\nAusgewählte Zeile nicht vorhanden.")
    
#  Ausgabe verschiedener Infos über die Datenbank
print(f'\nAnzahl ausgegebene Zeilen: {counter}/{zeilennummer-1}')
print(f'Anzahl ausgegebener Einträge: {counter*(len(beschriftung)-1)}/{(zeilennummer-1)*(len(beschriftung)-1)}')
print(f'Anzahl Spalten in der Datenbank: {len(beschriftung)-1}')


