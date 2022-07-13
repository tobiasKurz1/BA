# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 2022

SPENVIS-Daten LET Auslesen und Darstellen

genutzte Module: tabulate

@author: Tobias Kurz
"""
# Source-Datei einbinden

from source import block_starts, block_ends, get_meta, get_data, plot_this, cleanup_text #import Functions

from tabulate import tabulate
import csv



###### Dateiname ######


file = "spenvis_nlof_srimsi.txt"


#################################################################################
####
####        Programm
####
#################################################################################

line = 0

#CSV-Reader bekommt Datei, mit Anweisung um welche Abstandshalter es sich handelt
with open(file)as werte: # <-- Hier Dateinamen einstellen
    csv_reader_object = csv.reader(werte, delimiter=',') # <-- Hier Abstandshalter einstellen
      
    #Iteration der Zeilen durch den Reader, "row" immer die aktuell eingelesene Zeile
    for row in csv_reader_object:
       
        line += 1
        
        if block_starts(row):
            meta = get_meta(row)
            block = []
            data = []
            
        block.append(row)
        
        if block_ends(row):
            data = get_data(meta, block)
            #print(tabulate(block))
            cleanup_text(meta, data)
            plot_this(meta, data)