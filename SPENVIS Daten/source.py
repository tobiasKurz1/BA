# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 13:49:03 2022

@author: Tobias Kurz

Funktionen

"""
import sys
import matplotlib.pyplot as plt
#import numpy as np
import colorsys
import csv

#%% Classes

class metadata:
    def __init__(self, dataStart = [], lines = [], rows = [],  number = []):
        self.dataStart = dataStart
        self.lines = lines
        self.rows = rows
        self.number = number

class dataset:
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

#%% Functions
    


# Takes a database as input and lists all the packages inside
# User can then choose which one, also gives option to exit program
# Error and fault proof
def usersurvey(database):
    print("The following Data was found:\n")
    for i in range(len(database)):
        print(f'({i}) {database[i].name} from {database[i].segment}')

    print(f'({len(database)}) EXIT')
    while True:
        while True:
            chosenDB = (input("Which database do you want to use?\n"))
            try:
                chosenDB = int(chosenDB)
                break
            except:
                if ('exit') in chosenDB:
                    print("Exiting Program...")
                    sys.exit()
                else: print(f'You need to enter a Number between 0 and {len(database)}!\n')
            
        if chosenDB == len(database): 
            print("Exiting Program...")
            sys.exit()
        if chosenDB > len(database):
            print("Number too high! Try again or Exit with 'exit'\n")
        elif not('LET') in database[chosenDB].name:  
            print("No LET Data found. Please choose again!\n ")
        else: break
    return chosenDB

    
# Returns 1 if beginning of a new Block is found
def block_starts(ls):
    if ("'*'") in ls:
        return(1)
    else:
        return(0)

# Returns 1 if end of a Block is found
def block_ends(ls):
    if ("'End of Block'") in ls:
        return(1)
    if ("'End of File'") in ls:
        return(1)
    else:
        return (0)
    
# Uses first Line of every Block to fill metadata about following data
def get_meta(row):
    newMeta = metadata(int(row[1]), int(row[7]), int(row[6]), int(row[8]))
    return newMeta
    
# Fills dataset class with data from current Block
def get_data(meta, block):
    
    labels = meta.rows
    if meta.rows > 3: labels = 3 #Different approaches for different Data Structures
    data = dataset()
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
        
        #Separate While Loop for data Block only (optimization)
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

# Cleans up text from SPENVIS file for visualisation in Graph
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

# Imports Data from SPENVIS FILE while using other functions from the source.py file
def import_data(file, delimiter):
    line = 0                             
    database = []
    metabase = []
    
    with open(file)as werte:
        csv_reader_object = csv.reader(werte, delimiter=delimiter)
          
        for row in csv_reader_object:
           
            line += 1
            
            if block_starts(row): # get metadata about new block
                meta = get_meta(row)
                metabase.append(meta)
                block = []
                data = []
                
            block.append(row) # fill assigned tuple with data
            
            if block_ends(row): #sort and interpret saved data, clean text, plot graphs
                data = get_data(meta, block)
                cleanup_text(meta, data)
                database.append(data)
                
    metabase.reverse() #allign metabase with plot counting
    database.reverse() #allign database with plot counting
    
    return metabase, database


# Plots different types of data from SPENVIS. Data has so be in meta/data structure format.
# All data form spenvis_nlof_srimsi.txt and spenvis_nlol_srimsi.txt can be plotted
def plot_this(meta, data):  
    
    print(f'plotting {data.name} from segment {data.segment}...')
    
    
    if meta.rows ==-1: #special Case Diff. Path length
        plt.figure(figsize=(10,8))
        plt.plot(data.xaxis, data.y1axis, color='b', label = data.name)
        plt.suptitle(f'{data.name}',weight='bold')
        plt.xlabel(f'{data.xlabel} in {data.xunit}')
        plt.ylabel(f'{data.y1label} in {data.y1unit}')
        plt.grid(True)
        
        plt.xlim(meta.number[0],meta.number[1])
        
        plt.xscale('linear')
        plt.yscale('linear')
       
    
    if meta.rows == 2: #simple Graph    
        plt.figure(figsize=(10,8))
        plt.plot(data.xaxis, data.y1axis, color='b', label = data.name)
        plt.suptitle(f'DB:{meta.number} - {data.name} (Segment: {data.segment})',weight='bold')
        plt.xlabel(f'{data.xlabel} in {data.xunit}')
        plt.ylabel(f'{data.y1label} in {data.y1unit}')
        plt.grid(True)

        plt.xscale('log')
        plt.yscale('log')
    
    if meta.rows == 3: #double Graph
        fig, ax1 = plt.subplots(figsize = (10,8))
        ax1.set_xlabel(f'{data.xlabel} in {data.xunit}') 
        ax1.set_ylabel(f'{data.y1label} in {data.y1unit}', color='r')
        ax1.plot(data.xaxis, data.y1axis, color='r')
        ax1.tick_params(axis='y', labelcolor='r')
        plt.yscale('log')
        plt.title(f'DB:{meta.number} - {data.name} (Segment: {data.segment})',weight='bold')
        
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        ax2.set_ylabel(f'{data.y2label} in {data.y2unit}', color='b')  # we already handled the x-label with ax1
        ax2.plot(data.xaxis, data.y2axis, color='b')
        ax2.tick_params(axis='y', labelcolor='b')

        fig.tight_layout()  # otherwise the right y-label is slightly clipped

        plt.grid(True)
        plt.xscale('log')
        plt.yscale('log')
    
    
    if meta.rows > 3: #Layered Graph
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
        plt.title(f'DB:{meta.number} - {data.name} (Segment: {data.segment})',weight='bold')
       
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