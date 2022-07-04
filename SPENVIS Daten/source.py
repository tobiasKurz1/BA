# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 13:49:03 2022

@author: Tobias Kurz

Funktionen


"""

import matplotlib.pyplot as plt

####### Klassen #######

class metadata:
    def __init__(self, dataStart, length, number):
        self.dataStart = dataStart
        self.length = length
        self.number = number

class dataset:
    def __init__(self, name=[], xaxis=[], yaxis=[], xlabel=[], ylabel=[], xunit=[], yunit=[]):
        self.name = name
        self.xaxis = xaxis
        self.yaxis = yaxis
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.xunit = xunit
        self.yunit = yunit
        


####### FUnktionen ########
        
# Gibt eine 1 zurück, wenn der Anfang eines Blocks gefunden wurde
def block_starts(ls):
    if ("'*'") in ls:
        return(1)
    else:
        return(0)

# Gibt eine 1 zurück, wenn das Ende eines Blocks gefunden wurde
def block_ends(ls):
    if ("'End of Block'") in ls:
        return(1)
    if ("'End of File'") in ls:
        return(1)
    else:
        return (0)
    
# Fuellt Metadata-Klasse mit Informationen aus der ersten Zeile  
def get_meta(row):
    newMeta = metadata(int(row[1]), int(row[7]), int(row[8])+1)
    return newMeta
    
# Liest die entsprechenden Daten aus den Bloecken aus und speichert in Klasse Datensatz
def get_data(meta, block):
    data = dataset()
    data.xaxis = []
    data.yaxis = []
    l = 0
    
    while l in range(len(block)):
        
        if ("'PLT_HDR'") in block[l]:    
            data.name = block[l][2]
        if ("'Energy'") in block[l]:     
            data.xlabel = block[l][3]
            data.xunit = block[l][1]
        if ("'LET'") in block[l]:     
            data.ylabel = block[l][3]
            data.yunit = block[l][1]
        
        l += 1
        
        #Separate While Schleife für die daten (zur optimierung)
        while (l >= meta.dataStart and l < (meta.dataStart + meta.length)):
            data.xaxis.append(float(block[l][0]))
            data.yaxis.append(float(block[l][1]))
            l +=1
            
    return data
def cleanup_text(data):
    data.name = data.name.replace("'","")
    data.xunit = data.xunit.replace("'","")
    data.yunit = data.yunit.replace("'","")
    data.xlabel = data.xlabel.replace("'","")
    data.ylabel = data.ylabel.replace("'","")
    
    data.yunit = data.yunit.replace("!u","^")
    data.yunit = data.yunit.replace("!n","")    
    
    


def plot_this(data):
    plt.plot(data.xaxis, data.yaxis, color='b', label = data.name)
    plt.suptitle(data.name)
    plt.xlabel(f'{data.xlabel} in {data.xunit}')
    plt.ylabel(f'{data.ylabel} in {data.yunit}')
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True)
    
    plt.show()