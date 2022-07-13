# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 13:49:03 2022

@author: Tobias Kurz

Funktionen


"""

import matplotlib.pyplot as plt
import numpy as np
import colorsys

####### Klassen #######

class metadata:
    def __init__(self, dataStart, lines, rows,  number):
        self.dataStart = dataStart
        self.lines = lines
        self.rows = rows
        self.number = number

class graph_data:
    def __init__(self, name=[], segment='Total Mission', species = [], xaxis=[], y1axis=[], y2axis=[], xlabel=[], y1label=[], y2label=[], xunit=[], y1unit=[], y2unit=[]):
        self.name = name
        self.segment = segment
        self.species = species
        self.xaxis = xaxis
        self.y1axis = y1axis
        self.y2axis = y2axis
        self.xlabel = xlabel
        self.y1label = y1label
        self.y2label =y2label
        self.xunit = xunit
        self.y1unit = y1unit
        self.y2unit =y2unit
        
class bar_data:
    def __intit__(self, name=[], labels=[], values=[], unit=[]):
        self.name = name
        self.labels = labels
        self.values = values
        self.unit = unit

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
    newMeta = metadata(int(row[1]), int(row[7]), int(row[6]), int(row[8])+1)
    return newMeta
    
# Liest die entsprechenden Daten aus den Bloecken aus und speichert in Klasse Datensatz
def get_data(meta, block):
    
    labels = meta.rows
    if meta.rows > 3: labels = 3
    data = graph_data()
    data.xaxis = []
    data.y1axis = []
    data.y2axis = []
    l = 0
            
    data.xlabel = block[(meta.dataStart-labels)][3]
    data.xunit= block[(meta.dataStart-labels)][1]
    
    data.y1label = block[(meta.dataStart-labels+1)][3]
    data.y1unit= block[(meta.dataStart-labels+1)][1]
    
    if meta.rows > 2:
        data.y2label = block[(meta.dataStart-labels+2)][3]
        data.y2unit= block[(meta.dataStart-labels+2)][1]
        
    if meta.rows > 3:
        for s in range(int((meta.rows-1)/2)):
            data.y1axis.append([])
            data.y2axis.append([])
    
    while l in range(len(block)):
        
        if ("'PLT_HDR'") in block[l][0]: data.name = block[l][2]
        if ("'ORB_HDR'") in block[l][0]: data.segment = block[l][2]
        if ("'SPECIES'") in block[l][0]: 
            data.species = block[l]
            data.species.pop(0)
            data.species.pop(0)
        
        l += 1
        
        #Separate While Schleife für die daten (zur optimierung)
        while (l >= meta.dataStart and l < (meta.dataStart + meta.lines)):
            
            data.xaxis.append(float(block[l][0]))
            
            if meta.rows <= 3:    
                data.y1axis.append(float(block[l][1]))
            if meta.rows == 3:
                data.y2axis.append(float(block[l][2]))
            if meta.rows > 3:
                for t in range(int((meta.rows-1)/2)):
                    data.y1axis[t].append(float(block[l][2*t+1]))
                    data.y2axis[t].append(float(block[l][2*t+2]))
            
            l +=1
            
    return data
    
# Saeubert den Text
def cleanup_text(meta, data):
    data.name = data.name.replace("'","")
    data.segment = data.segment.replace("'","")
    data.xunit = data.xunit.replace("'","")
    data.y1unit = data.y1unit.replace("'","")
    data.xlabel = data.xlabel.replace("'","")
    data.y1label = data.y1label.replace("'","")
    data.y1unit = data.y1unit.replace("!u","^")
    data.y1unit = data.y1unit.replace("!n","") 
    data.xunit = data.xunit.replace("!u","^")
    data.xunit = data.xunit.replace("!n","") 
    
    for i in range(len(data.species)):
        data.species[i] = data.species[i].replace("'","")
        
    if meta.rows >= 3:
        data.y2unit = data.y2unit.replace("'","")
        data.y2label = data.y2label.replace("'","")
        data.y2unit = data.y2unit.replace("!u","^")
        data.y2unit = data.y2unit.replace("!n","") 

def plot_this(meta, data):  
    
    print(f'plotting {data.name} from segment {data.segment}...')
    
    if meta.rows == 2: #Einfacher Graph    
        plt.figure(figsize=(10,8))
        plt.plot(data.xaxis, data.y1axis, color='b', label = data.name)
        plt.suptitle(f'{data.name} (Segment: {data.segment})',weight='bold')
        plt.xlabel(f'{data.xlabel} in {data.xunit}')
        plt.ylabel(f'{data.y1label} in {data.y1unit}')
        plt.grid(True)

        plt.xscale('log')
        plt.yscale('log')
    
    if meta.rows == 3: #Graph mit zwei Y-Achsen
        fig, ax1 = plt.subplots(figsize = (10,8))
        ax1.set_xlabel(f'{data.xlabel} in {data.xunit}') #Benennung x-Achse
        ax1.set_ylabel(f'{data.y1label} in {data.y1unit}', color='r')
        ax1.plot(data.xaxis, data.y1axis, color='r')
        ax1.tick_params(axis='y', labelcolor='r')
        plt.yscale('log')
        plt.title(f'{data.name} (Segment: {data.segment})',weight='bold')
        
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        ax2.set_ylabel(f'{data.y2label} in {data.y2unit}', color='b')  # we already handled the x-label with ax1
        ax2.plot(data.xaxis, data.y2axis, color='b')
        ax2.tick_params(axis='y', labelcolor='b')

        fig.tight_layout()  # otherwise the right y-label is slightly clipped

        plt.grid(True)
        plt.xscale('log')
        plt.yscale('log')
    
    # if meta.rows > 3: #Balkendiagramm
        
    #     r = list(range(len(data.xaxis)))
    #     barWidth = 1
    #     colorwheel = []
        
    #     for s in range(len(data.species)):
    #         colorwheel.append(colorsys.hsv_to_rgb((1.0/len(data.species))*s, 1.0, 1.0))

    #     i = 0
    #     bottombars = [0] * len(data.xaxis)   
        
    #     while i < len(data.species):
    #         plt.bar(r, data.y1axis[i], bottom = bottombars, color = colorwheel[i], width = barWidth)
    #         bottombars = np.add(bottombars, data.y1axis[i]).tolist()
    #         i += 1
            
    #     plt.xticks(r, data.xaxis)
    #     plt.xscale('linear')
    #     plt.yscale('linear')
    #     plt.grid(True)
    #     plt.legend()
    
    if meta.rows > 3: #Schichtdiagramm
        colorwheel = []
        for s in range(len(data.species)):
            colorwheel.append(colorsys.hsv_to_rgb((1.0/len(data.species))*(s*0.8), 1.0, 1.0))
            colorwheel[s] = [round(x*255) for x in colorwheel[s]]
            colorwheel[s] = '#%02x%02x%02x' % (colorwheel[s][0], colorwheel[s][1], colorwheel[s][2])
    
        plt.figure(figsize = (10,8))
        
        data.y1axis.reverse()
        data.y2axis.reverse()
        data.species.reverse()
        
        plt.subplot(211)
        plt.stackplot(data.xaxis, data.y1axis, labels = data.species,colors = colorwheel, alpha = 0.8)
        plt.yscale('log')
        plt.xscale('log')
        plt.grid(True)
        plt.ylabel(f'{data.y1label} in \n{data.y1unit}')
        plt.title(f'{data.name} (Segment: {data.segment})',weight='bold')
       
        
        plt.subplot(212)
        plt.stackplot(data.xaxis, data.y2axis, labels = data.species,colors = colorwheel, alpha = 0.8)
        plt.sharex = True
        plt.yscale('log')
        plt.xscale('log')
        plt.grid(True)
        plt.xlabel(f'{data.xlabel} in {data.xunit}')
        plt.ylabel(f'{data.y2label} in \n{data.y2unit}')
        
        plt.legend(loc='lower center', bbox_to_anchor=(0.5,-1.1), ncol=10)
        
    
    plt.show()
    print(" Done!")