# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 13:49:03 2022

@author: Tobias Kurz

Funktionen

"""
from classes import metadata, dataset
from tabulate import tabulate
import sys
import matplotlib.pyplot as plt
import colorsys
import csv
import pandas as pd

#%% Functions

def output_variables(v):
    outputview = [["e",     v.e,    "pC",            "Elementary Charge"],
                  ["X",     v.X,    "MeV",           "Energy needed to create one electron-hole pair (3.6 eV in Si, 4.8 eV in GaAs)"],
                  ["L_max", v.L_max,"MeV*cm^2*g^-1", "highest LET any stopping ion can deliver"],
                  ["p_max", v.p_max,"g/cm^2",        "largest diameter of the sensitive Volume"],
                  ["Q_c",   v.Q_c,  "pC",            "minimum charge for Upset"],     
                  ["A",     v.A,    "m^2",           "surface area of sensitive volume"]
                 ]

    print(tabulate(outputview, headers=["Variable","Value","Unit","Description"])) 
    print("\n")


def usercheck(v):
    
    L_c = round(v.L_min * ((v.dimensions[0]**2 + v.dimensions[1]**2 + v.dimensions[2]**2)**0.5)/min(v.dimensions),13)
    
    loop = True
    while loop:
        print("\n")
    
        inputview = [["(1)", "w,l,h",            f'{v.dimensions[0]},{v.dimensions[1]},{v.dimensions[2]}', "μm", "Dimensions of the Sensitive Volume"],
                     ["(2)", "L_min",              v.L_min,                            "MeV*cm^2*mg^-1", "Minimum LET for an upset through largest diameter"],
                     ["(3)", "L_c ",              L_c,                               "MeV*cm^2*mg^-1", "Minimum LET for an upset through smallest diameter (critical LET or threshold LET)"],
                     ["(4)", "Transistorcount",      "{:.2e}".format(v.sVol_count),      " - ",           "Number of Sensitive Volumes/Transistors"],
                     ["(5)", "X",                  v.X,                                "eV",            "Energy needed to create one electron-hole pair (Si: 3.6 eV; GaAs: 4.8 eV)"],
                     ["(6)", "ρ",                  v.rho, "g/cm^3", "Density of the material the component is made of. (Only affects intermediate results)"],
                     ["(7)", "σ_pl", v.xsection,                    "cm^2/bit",      "Limiting proton upset cross section of the Device"],
                     ["(8)", "A_t",     v.A_t  ,           "MeV", "Threshold of the proton upset"],
                     ["----"," ","",""],
                     ["(9)", "Steps",              "{:.2e}".format(v.steps),           " - ",           "Number of iteration Steps"],
                     ["(10)", "Axis scale",         v.scale,                            " - ",           "Scale of the Calculation Axis (log/lin)"],
                     ["(11)", "LET calculation", v.switch[0]," - ", "Turn direct LET ionization upset calculation On or Off"],
                     ["(12)", "Proton calculation", v.switch[1]," - ", "Turn proton nuclear reaction upset calculation On or Off"],
                     ["(13)", "Plot graphs?",        v.plot,                             " - ",          "Turn Graph Plotting on or off (use for debugging)"]]
    
        print(tabulate(inputview, headers=["","Variable","Value","Unit","Description"])) 
        
        print("\nChange variables and settings by entering the corresponding number or type exit.\nOr press Enter to Continue",end='\r')
        
        while True:
            
            choice = input()
        
            if ("") == choice: loop = False; break
    
            try: 
                choice = int(choice)
                
                if choice == 1: 
                                v.dimensions = (basicinput(1., "Please enter a new value for w:"),\
                                                basicinput(1., "Please enter a new value for l:"),\
                                                basicinput(1., "Please enter a new value for h:"))
                                L_c = (v.L_min * ((v.dimensions[0]**2 + v.dimensions[1]**2 + v.dimensions[2]**2)**0.5)/min(v.dimensions))
                                break
                if choice == 2: 
                                temp = basicinput(1., "Please enter a new value for L_min:")
                                if (temp < (1.05*(10**5))): v.L_min = temp; L_c = v.L_min * ((v.dimensions[0]**2 + v.dimensions[1]**2 + v.dimensions[2]**2)**0.5)/min(v.dimensions); break
                                else: print("ERROR: Could not Compute! (L_min > L_Max)");break
                
                if choice == 3: 
                                temp2 = basicinput(1., "Please enter a new value for the LET upset threshold:")
                                temp = temp2 * (((v.dimensions[0]**2 + v.dimensions[1]**2 + v.dimensions[2]**2)**0.5)/min(v.dimensions))**-1
                                if (temp < (1.05*(10**5))): v.L_min = temp; L_c = temp2 ; break
                                else: print("ERROR: Could not Compute! (L_min > L_Max)");break
                if choice == 4: v.sVol_count = basicinput(1, "Please enter a new value for the number of sensitive Volumes:") ; break
                if choice == 5: v.X = basicinput(1., "Please enter a new value for X (3.6 eV in Si, 4.8 eV in GaAs):");break
                if choice == 6: v.rho = basicinput(1., "Please enter a new yalue vor ρ:");break
                if choice == 7: v.xsection = basicinput(1., "Please enter a new value for the limiting cross section:");break
                if choice == 8: v.A_t = basicinput(1., "Please enter a new value for the proton upset threshold:");break
                if choice == 9: v.steps = basicinput(1, "Please enter a new value for steps:") ; break
                if choice == 10: 
                                if (v.scale == 'log'): v.scale = "lin"; break
                                else: v.scale = 'log'; break
                if choice == 11: v.switch = (not(v.switch[0]), v.switch[1]);break
                if choice == 12: v.switch = (v.switch[0], not(v.switch[1]));break
                if choice == 13: v.plot = not(v.plot); break
                              
        
                else: print("Incorrect Input. Please try again.")
            
            except: 
                    if (choice =='exit'): sys.exit();
                    print("Incorrect Input. Please try again.")
    
    return(v)


def basicinput(example_of_data, Text):
    
    # Gets a Fault proof input and malkes sure the given Datatype is recieved
    # Returns corrected input
    
    while True:
        temp = input(Text)
        try:
            if type(example_of_data) == type(1):
                temp = int(temp)
                break
            if type(example_of_data) == type("string"):
                temp = str(temp)    
                break
            if type(example_of_data) == type(1.):
                temp = float(temp)    
                break
        except:
            print(f'You need to Enter a {type(example_of_data)}. Please try again.')
    return(temp) 


def usersurvey(metabase, database):
    
    # Takes a database as input and lists all the packages inside
    # User can then choose which one, also gives option to exit program
    # Error and fault proof
    
    print("The following Mission segments were found:\n")
    segment_list = [""]
    for i in range(len(database)):
        if not(segment_list[-1] == database[i].segment):
            segment_list.append(database[i].segment) 
            print(f'({len(segment_list)-1}) {segment_list[-1]}')

    if (len(segment_list))==1:
        print("No mission Segments were found. Make sure to enter the correct file name of the .txt file from SPENVIS.\n\
The default SPENVIS output file is 'spenvis_nlof_srimsi.txt'.")
        out = 2
        (Proton_meta, Proton_data, LET_meta, LET_data) = ([],[],[],[])
        return LET_meta, LET_data, Proton_meta, Proton_data, out
    print("------------------------------------")
    print(f'({len(segment_list)}) Calculate for all of the mission segments above and export results to excel-file')
    print(f'({len(segment_list)+1}) Plot all input data ')
    print(f'({len(segment_list)+2}) Change input file ')
    print(f'({len(segment_list)+3}) HELP')
    print(f'({len(segment_list)+4}) EXIT')
    out = 0
    while True:
        while True:
            chosenDB = (input("Please choose a database or option.\n"))
            try:
                chosenDB = int(chosenDB)
                break
            except:
                if ('exit') in chosenDB:
                    print("Exiting Program...")
                    sys.exit()
                else: print(f'You need to enter a Number between 1 and {len(segment_list)+4}!')
        
        if chosenDB == len(segment_list): #calculate all and export
            out = 1
            (Proton_meta, Proton_data, LET_meta, LET_data) = ([],[],[],[])
            break
        
        elif chosenDB == len(segment_list)+1: #plot all
            for n in range(len(database)):
                plot_this(metabase[n],database[n])
            
            verg_plot(database) #vergleichsplot der gesamtmission      
            
        elif chosenDB == len(segment_list)+2: #change the input file
            out = 2
            (Proton_meta, Proton_data, LET_meta, LET_data) = ([],[],[],[])
            break
        elif chosenDB == len(segment_list)+3: # Help menu
            information_screen(len(segment_list))
        elif chosenDB == len(segment_list)+4: # Exit
            print("Exiting Program...")
            sys.exit()
        elif chosenDB > len(segment_list)+4:
            print("Number too high! Try again or Exit with 'exit'")
        else: 
            for i in range(len(database)):
                if segment_list[chosenDB] == database[i].segment:
                    if ('LET') in database[i].name:
                        LET_meta = metabase[i]
                        LET_data = database[i]
                    elif ('proton') in database[i].name:
                        Proton_meta = metabase[i]
                        Proton_data = database[i]
            try:    
                LET_meta
                try: 
                    Proton_meta; break
                except: 
                    (Proton_meta, Proton_data) = ([],[])
                    print("Warning: No proton data found in selected data! \nTurn proton nuclear reaction calculation off or else you may crash the program (Saturation Crosssection = 0).\nPlease also check your source file.\n "); break
                        
            except: print("Error: No LET Data found in selected Data! Calculation not possible.\n ")
                
                

            
    
    return LET_meta, LET_data, Proton_meta, Proton_data, out

    
def information_screen(segnr):
    print()
    print("**********************************************")
    print("     WELCOME TO THE RAY CALCULATION TOOL!")
    print("**********************************************\n")
    print(f'The RAY (Radiation Single Event Effect Probability) tool was developed as part of a bachelor thesis for the IRS, Uni Stuttgart.\n\
It is used to calculate the upset rates of electonic devices caused by highly energetic particles in space around earth.\n\n\
To get started, any one of the detected mission segments (1 to {segnr-1}) can be drawn for calculation. The program will then give the complete list of calculation variables and settings for the upcoming upset rate calculation.\
 After each result the user has the option to change values and redo the calculations.\nThis can be stopped by typing \'exit\'.\n\
For calculating the upset rates for the entirety of the mission chosse option {segnr}. Here the variables are presented once. After confirming the values, all of the mission segment rates are calculated and the results are stored in \'Upset_rates.xlsx\',\
 which is located in the program folder.\n\
It is recommended to first check the input data for consistency. This can be done by plotting the graphs using option {segnr+1}.\n')
    print("RAY Version 1.0\nOctober 2022 \nTobias Kurz for IRS @ Uni Stuttgart")
    return()     
    
#%% SPENVIS Data handling


def block_starts(ls):
    # Returns 1 if beginning of a new Block is found
    
    if ("'*'") in ls:
        return(1)
    else:
        return(0)


def block_ends(ls):
    # Returns 1 if end of a Block is found
    
    if ("'End of Block'") in ls:
        return(1)
    if ("'End of File'") in ls:
        return(1)
    else:
        return (0)
    

def get_meta(row):
    # Uses first Line of every Block to fill metadata about following data
    
    newMeta = metadata(int(row[1]), int(row[7]), int(row[6]), int(row[8]))
    return newMeta
    

def get_data(meta, block):
    # Fills dataset class with data from current Block
    
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

def to_excel(v,segments,Uprot,Ulet,Utot,upsets):    
    
    print("\nExporting to 'Upset_rates.xlsx'... ")
    
    variables = ["w","l","h","L_min","Steps","SVs","X","rho","sigma_p","A_t"]
    values = [v.dimensions[0],v.dimensions[1],v.dimensions[2],v.L_min,v.steps,v.sVol_count,v.X,v.rho,v.xsection,v.A_t]
    
    dif = len(segments)-len(variables)
    
    if dif < 0:
        for i in range(abs(dif)):
            segments.append("")
            Uprot.append("")
            Ulet.append("")
            upsets.append("")
            Utot.append("")
    if dif > 0:
        for i in range(abs(dif)):
            variables.append("")
            values.append("")
    
    data = pd.DataFrame({"Variables":variables,"Values":values,"":"","Segment":segments,"U_prot":Uprot,"U_LET":Ulet,"U":Utot,"Upsets/year":upsets})
    data.to_excel('Upset_rates.xlsx',sheet_name='Results',index=False)
    
    print("Export successful!")
    
    return()
    
    




def cleanup_text(meta, data):
    # Cleans up text from SPENVIS file for visualisation in Graph
    
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



def import_data(file, delimiter):
    # Imports Data from SPENVIS FILE while using other functions from the source.py file
    
    line = 0                             
    database = []
    metabase = []
    
    
    while True:
    
        try:
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
            break
            
        except:  
            print(f'No file with name \'{file}\' found. Please enter a new file name or type exit.')
            file = basicinput("text", "New file: ")
            if ('exit') in file:
                print("Exiting Program...")
                sys.exit()
                
    metabase.reverse() #allign metabase with plot counting
    database.reverse() #allign database with plot counting
    
    
    
    return metabase, database, file


def plot_this(meta, data):  
    # Plots different types of data from SPENVIS. Data has so be in meta/data structure format.
    # All data form spenvis_nlof_srimsi.txt and spenvis_nlol_srimsi.txt can be plotted
    
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


def verg_plot(data):
    prt = []
    let = []
    
    i = 1
    for n in range(3,len(data)):
        if i == 2: 
            prt.append(data[n])
        if i == 3:
            let.append(data[n])
        i += 1
        
        if i>3: i=1
    
    plt.figure(figsize=(10,8))
    
    for n in range(len(prt)):
        plt.plot(prt[n].xaxis, prt[n].y1axis, label = f'Seg. {prt[n].segment}')
        
    plt.suptitle(f'{prt[0].name}',weight='bold')
    plt.xlabel(f'{prt[0].xlabel} in {prt[0].xunit}')
    plt.ylabel(f'{prt[0].y1label} in {prt[0].y1unit}')
    plt.grid(True)
    plt.legend()

    plt.xscale('log')
    plt.yscale('log')
    plt.show()
    
    
    plt.figure(figsize=(10,8))
    for n in range(len(let)):
        plt.plot(let[n].xaxis, let[n].y1axis, label = f'Seg. {let[n].segment}')
        
    plt.suptitle(f'{let[0].name}',weight='bold')
    plt.xlabel(f'{let[0].xlabel} in {let[0].xunit}')
    plt.ylabel(f'{let[0].y1label} in {let[0].y1unit}')
    plt.grid(True)
    plt.legend()

    plt.xscale('log')
    plt.yscale('log')
    plt.show()