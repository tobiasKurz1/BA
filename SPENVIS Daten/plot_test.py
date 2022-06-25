# -*- coding: utf-8 -*-
"""
TEST
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
        x_werte.append(float(row[0]))
        y_werte1.append(float(row[1]))
        y_werte2.append(float(row[2]))

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
    


#################################################################################
####
####        Programm
####
#################################################################################


from tabulate import tabulate
import csv
import matplotlib.pyplot as plt

##  Anfangsposition der Daten Blöcke 1-12 (Achsenbeschriftungen in den drei Zeilen davor)
daten = [76, 181, 287, 392, 498, 603, 709, 814, 920, 1025, 1085, 1144, 28, 61]
##  Anzahl Zeilen der Datenblöcke
datenlaenge = [29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 5, 5]
counter = 1
blocknr = 12
ergebnisse = [] #Hier werden Später die Zeilen abgelegt
x_werte = []
y_werte1 = []
y_werte2 = []
achsen = []
satz = []

#CSV-Reader bekommt Datei, mit Anweisung um welche Abstandshalter es sich handelt
with open('block_13_14.txt')as werte: # <-- Hier Dateinamen einstellen
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
              
                satz.append(y_werte1[:])
                y_werte1.clear()
                y_werte2.clear()
           
              
            
        if anfang_block(row)==1:
            anfang = counter
                        
        if ende_block(row)==1:
            print(f'\n* * * * * *  {blocknr}. Block: Von Zeile {anfang} bis {counter}, Länge: {counter-anfang+1} Zeilen * * * * * *\n')
            print (tabulate(ergebnisse))
            ergebnisse.clear()

            
            
        counter += 1







