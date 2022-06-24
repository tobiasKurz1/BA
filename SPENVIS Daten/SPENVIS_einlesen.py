# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 2022

Einlesen einer CSV-Datei aus SPENVIS und Ausgabe bestimmter Daten

genutzte Module: tabulate

@author: Tobias Kurz
"""
####### FUnktionen ########


# Einen String in der Zeile suchen und anzahl Zeile ausgeben
def suche_string(x, ls):
    if x in ls:
        print(f'Treffer in Zeile {counter}' )
        
# Gibt eine 1 zurück, wenn der Anfang eines neuen Blocks gefunden wurde
def anfang_block(ls):
    if ("'*'") in ls:
        return(1)
    else:
        return(0)

# Gibt eine 1 zurück, wenn das Ende eines neuen Blocks gefunden wurde
def ende_block(ls):
    if ("'End of Block'") in ls:
        return(1)
    if ("'End of File'") in ls:
        return(1)
    else:
        return (0)


#################################################################################
####
####        Programm
####
#################################################################################


from tabulate import tabulate
import csv

#CSV-Reader bekommt Datei, mit Anweisung um welche Abstandshalter es sich handelt
with open('Average_proton_and_electron_fluxes.txt')as werte: # <-- Hier Dateinamen einstellen
    csv_reader_object = csv.reader(werte, delimiter=',') # <-- Hier Abstandshalter einstellen
    
    
    blockzahl = 0
    counter = 1         #Zaehler für die Ausgegebenen Zeilen
    treffer = 0 
    anfang = 0

        
        
    ergebnisse = [] #Hier werden Später die Zeilen abgelegt
        
    #Iteration der Zeilen durch den Reader, "row" immer die aktuell eingelesene Zeile
    #Indirekt können hierdurch bestimmte Zeilen ausgegeben werden
    for row in csv_reader_object:
        # Oberste Zeile -> Ueberschriften festlegen
        
            ergebnisse.append(row) #befuellen der Ergebnisliste und Aufzaehlen der Zeilen
            blockzahl = blockzahl + ende_block(row) 
            
            if anfang_block(row)==1:
                anfang = counter
                            
            if ende_block(row)==1:
                print(f'\n* * * * * *  {blockzahl}. Block: Von Zeile {anfang} bis {counter}  * * * * * *\n')
                print (tabulate(ergebnisse))
                ergebnisse.clear()
                
            
            counter += 1



###### Ausgaben ######

   
print("\n")

print(f'\nAnzahl Blöcke: {blockzahl}')      
#  Ausgabe verschiedener Infos über die Datenbank
print(f'\nAnzahl Zeilen: {counter-1}')



