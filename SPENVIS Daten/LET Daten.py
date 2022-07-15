# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 2022

SPENVIS-Daten LET Auslesen und Darstellen

genutzte Module: tabulate

@author: Tobias Kurz
"""

#%% Imports

from source import block_starts, block_ends, get_meta, get_data, plot_this, cleanup_text #import Functions
#from tabulate import tabulate
import csv

#%% Declarations

file = "spenvis_nlof_srimsi.txt"     # File name
delimiter = ","                      # delimiter of datapoints
line = 0                             # line starter
database = []
metabase = []


#%% function for returning database


#%% Import Data

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
            #print(tabulate(block))
            cleanup_text(meta, data)
            database.append(data)
            plot_this(meta, data)

metabase.reverse() #allign metabase with plot counting
database.reverse() #allign database with plot counting
