# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 10:19:17 2022

Tests zum Einlesen einer CSV-Datei

@author: Tobias Kurz
"""



import csv

#CSV-Reader bekommt Datei, mit Anweisung um welche Abstandshalter es sich handelt
with open('test.csv')as werte:
    csv_reader_object = csv.reader(werte, delimiter=';')
    
    zeilennummer = 0
    
    
    SucheZeile = int(input("Welche Zeile ausgeben? (für komplette Ausgabe 0 eingeben.) "))

    
    #Iteration der Zeilen durch den Reader
    #Indirekt können hierdurch bestimmte Zeilen ausgegeben werden
    
    for row in csv_reader_object:
        # Oberste Zeile
        if zeilennummer == 0:
            print(f'Spaltennamen sind: {", ".join(row)}')
        else:
            if zeilennummer == SucheZeile or SucheZeile == 0:
                print(row)
        zeilennummer += 1

print(f'Anzahl Zeilen: {zeilennummer-1}')

if SucheZeile > (zeilennummer-1):
    print("Ausgewählte Zeile nicht vorhanden.")
