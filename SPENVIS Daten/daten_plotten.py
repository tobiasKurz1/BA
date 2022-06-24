# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 2022

SPENVIS-Daten Darstellen

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
import matplotlib.pyplot as plt


counter = 1

ergebnisse = [] #Hier werden Später die Zeilen abgelegt
x_werte = []
y_werte1 = []
y_werte2 = []
achsen = []

test = []

def daten_sammeln(grenze_u, grenze_o):
    if counter >=grenze_u and counter <=grenze_o:
        x_werte.append(float(row[0]))
        y_werte1.append(float(row[1]))
        y_werte2.append(float(row[2]))
        
def beschiftung_sammeln(grenze_u, grenze_o):
    if counter >=grenze_u and counter <=grenze_o:
        achsen.extend((row[3], row[1]))
        


#CSV-Reader bekommt Datei, mit Anweisung um welche Abstandshalter es sich handelt
with open('block_1.txt')as werte: # <-- Hier Dateinamen einstellen
    csv_reader_object = csv.reader(werte, delimiter=',') # <-- Hier Abstandshalter einstellen
      
        

        
    #Iteration der Zeilen durch den Reader, "row" immer die aktuell eingelesene Zeile
    #Indirekt können hierdurch bestimmte Zeilen ausgegeben werden
    for row in csv_reader_object:
        # Oberste Zeile -> Ueberschriften festlegen
        
        
            ergebnisse.append(row) #befuellen der Ergebnisliste und Aufzaehlen der Zeilen
            daten_sammeln(76, 104)
            beschiftung_sammeln(73,75)
            counter += 1

print (tabulate(ergebnisse))

achsen = [s.replace("'","") for s in achsen]

######### Plot ##########

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel(f'{achsen[0]} [{achsen[1]}]') #Benennung x-Achse
ax1.set_ylabel(f'{achsen[2]} [{achsen[3]}]', color=color)
ax1.plot(x_werte, y_werte1, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel(f'{achsen[4]} [{achsen[5]}]', color=color)  # we already handled the x-label with ax1
ax2.plot(x_werte, y_werte2, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.xscale('log')
plt.show()

