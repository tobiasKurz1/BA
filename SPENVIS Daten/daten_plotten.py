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

# Sammelt Daten aus den Bereichen in Arrays
def daten_sammeln(grenze_u, grenze_o):
    if counter >=grenze_u and counter <=grenze_o:
        
        y_werte[0].extend([float(row[1])])
        y_werte[1].extend([float(row[2])])
        x_werte.append(float(row[0]))

def gesdaten_sammeln(anf_daten):
    if counter >= anf_daten and counter <= (anf_daten+4):
        n = counter - anf_daten
        gesy_werte.append(row[:])
        gesy_werte[n].pop(0)
        gesy_werte[n].pop(0)
        gesy_werte[n] = [float(i) for i in gesy_werte[n]]
    
    if counter == (anf_daten-15):
        gesx_werte.append(row[:])
        gesx_werte[0].pop(0)
        gesx_werte[0].pop(0)
        gesx_werte[0].pop(-1)
        gesx_werte[0] = [float(i) for i in gesx_werte[0]]
      
        
#def gesbeschriftung_sammeln(anf_daten):

def plot_gesdaten():
    plt.plot(gesx_werte[0], gesy_werte[0], color='r', label='Phase 1')
    plt.plot(gesx_werte[0], gesy_werte[1], color='r', label='Phase 2')
    plt.plot(gesx_werte[0], gesy_werte[2], color='r', label='Phase 3')
    plt.plot(gesx_werte[0], gesy_werte[3], color='r', label='Phase 4')
    plt.plot(gesx_werte[0], gesy_werte[4], color='r', label='Phase 5')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel(f'Block {blocknr}') #Benennung x-Achse
    
    plt.show()
    
# Sammelt Achsenbeschriftungen aus dem Bereich über dem Datenblock in Arrays        
def beschiftung_sammeln(anf_daten):
    if counter >=(anf_daten-3) and counter <= (anf_daten-1):
        achsen.extend((row[3], row[1]))
        
# Plottet aktuelle Achsen und Daten
def plot_daten():  
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel(f'Block {blocknr}: {achsen[0]} [{achsen[1]}]') #Benennung x-Achse
    ax1.set_ylabel(f'{achsen[2]} [{achsen[3]}]', color=color)
    ax1.plot(x_werte, y_werte[0], color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel(f'{achsen[4]} [{achsen[5]}]', color=color)  # we already handled the x-label with ax1
    ax2.plot(x_werte, y_werte[1], color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.xscale('log')
    plt.show()
    


#################################################################################
####
####        Programm
####
#################################################################################


from tabulate import tabulate
import csv
import matplotlib.pyplot as plt

##  Anfangsposition der Daten Blöcke 1-12 (Achsenbeschriftungen in den drei Zeilen davor)
daten = [76, 181, 287, 392, 498, 603, 709, 814, 920, 1025, 1085, 1144, 1202, 1235, 1268, 1301, 1334, 1367]
##  Anzahl Zeilen der Datenblöcke
datenlaenge = [29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 5, 5, 5, 5, 5, 5]
counter = 1
blocknr = 0
ergebnisse = [] #Hier werden Später die Zeilen abgelegt
x_werte = []
y_werte = [],[]
gesy_werte = []
gesx_werte = []
achsen = []


#CSV-Reader bekommt Datei, mit Anweisung um welche Abstandshalter es sich handelt
with open('Average_proton_and_electron_fluxes.txt')as werte: # <-- Hier Dateinamen einstellen
    csv_reader_object = csv.reader(werte, delimiter=',') # <-- Hier Abstandshalter einstellen
      
    #Iteration der Zeilen durch den Reader, "row" immer die aktuell eingelesene Zeile
    for row in csv_reader_object:
        # Oberste Zeile -> Ueberschriften festlegen
        
        
        blocknr = blocknr + anfang_block(row)
        
        ergebnisse.append(row) #befuellen der Ergebnisliste und Aufzaehlen der Zeilen
        
        if blocknr < 13:    # ZU TESTZWECKEN
            
            daten_sammeln(daten[blocknr-1], daten[blocknr-1]+datenlaenge[blocknr-1]-1)
            beschiftung_sammeln(daten[blocknr-1])
                            
            if ende_block(row)==1:
                achsen = [s.replace("'","") for s in achsen]
                plot_daten()
                achsen.clear()
                x_werte.clear()
                y_werte = [],[]
        
        if blocknr >= 13:
            gesdaten_sammeln(daten[blocknr-1])
            
            if ende_block(row)==1:
                
                plot_gesdaten()
                gesx_werte = []
                gesy_werte = []
                n = 0
        
            
        if anfang_block(row)==1:
            anfang = counter
                        
        if ende_block(row)==1:
            print(f'\n* * * * * *  {blocknr}. Block: Von Zeile {anfang} bis {counter}, Länge: {counter-anfang+1} Zeilen * * * * * *\n')
            print (tabulate(ergebnisse))
            ergebnisse.clear()       
            
        counter += 1







