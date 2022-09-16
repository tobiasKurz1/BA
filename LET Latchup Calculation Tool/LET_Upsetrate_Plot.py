"""

Program LET_calc
___________________

This programm comuptes the Upset rate due to direct ionisation fo individual particles.
Each bit on the chip is assumed as a sensitive Volume of dimesions w, l, h in micrometers.
The sensitive Volume (SV) shape is idealized as a rectangular parallellopiped (RPP).
Also assumed is that the LET of each Ion is constant over the dimensions of the critical volume.
The output Upset Rate is translated into a probability distribution using a gaussian standard distribution.


Imputs are:
    dimensions    : w,l,h Dimensions of the sensitive Volume [μm]
    L_min         : Required minimum LET for an Upset with p_max (largest path through the SV) [MeV*cm^2*g^-1]
    X             : Energy needed to create ine electron-hole pair (3.6 eV in SI; 4.8 eV in GaAs) [eV]
    file_name     : Name of the SPENVIS File  which contains the Integral LET spectrum at the specific mission or mission Segment (default file name is "spenvis_nlof_srimsi.txt")
    steps         : Number of steps for the difpld and integration (for accurate results at >100.000 is advised)
    transistorcnt : Number of Transistors per Chip (used for probability calculations)
    axis_scale    : Can either be 'lin' or 'log', log tends to give more precise results more quickly
    Plot_graphs   : Boolean to plot the results step by step

Outputs are:
    Graphic       : differential and integral LET spectra (SPENVIS Data)
    Graphic       : Differental path length distribution (difpld) of the SV
    Graphic       : Probability distribution of Errors per Day per Chip
    U             : Upset Rate in events per bit per second
    
Functions Used:
    import_data   : Importing and Sorting data from SPENVIS standard text output
    plot_this     : Plots data from import_data format
    difpld        : Generates difpld diagramm based on SV and range
    adamsint      : Computes the function, which is later to be integrated for the final calculation
    
"""

from source import import_data



#%% Default Input variables

file_name        = 'spenvis_nlof_srimsi_1cm.txt'
dimensions       = (25000,25000,2000)
X                = 3.6
rho              = 2.33
L_min            = 10
steps            = 100000
transistorcnt    = 1
axis_scale       = 'log'
sat_xsection     = 10**-8
A_t              = 20
plot_graphs      = True
switch           = (False, True)

import matplotlib.pyplot as plt

#%%
(metabase, database)=import_data(file_name,',') # SPENVIS Data
    
for d in range(1,3):
    
   
    
    
    
    plt.figure(figsize=(10,8))
    
    i = d
    
    plt.plot(database[i].xaxis, database[i].y1axis, color='r', alpha=1, label=database[i].segment, zorder=6)
    i= i+3
    plt.plot(database[i].xaxis, database[i].y1axis, color='b', alpha=1, label=database[i].segment, zorder=5)
    i= i+3
    plt.plot(database[i].xaxis, database[i].y1axis, color='b', alpha=0.8, label=database[i].segment, zorder=4)
    i= i+3
    plt.plot(database[i].xaxis, database[i].y1axis, color='b', alpha=0.6, label=database[i].segment, zorder=3)
    i= i+3
    plt.plot(database[i].xaxis, database[i].y1axis, color='b', alpha=0.4, label=database[i].segment, zorder=2)
    i= i+3
    plt.plot(database[i].xaxis, database[i].y1axis, color='b', alpha=0.2, label=database[i].segment, zorder=1)
    
    
    plt.title(f'{database[i].name} for all mission segments')
    plt.xlabel(f'{database[i].xlabel} in {database[1].xunit}') 
    plt.ylabel(f'{database[i].y1label} in {database[1].y1unit}')
    plt.grid(True)
    plt.legend()
    plt.xscale('log')
    plt.yscale('log')
    
    plt.show()
    
    
    i = d
    plt.figure(figsize=(10,8))
    
    plt.plot(database[i].xaxis, database[i].y2axis, color='r', alpha=1, label=database[i].segment, zorder=6)
    i= i+3
    plt.plot(database[i].xaxis, database[i].y2axis, color='b', alpha=1, label=database[i].segment, zorder=5)
    i= i+3
    plt.plot(database[i].xaxis, database[i].y2axis, color='b', alpha=0.8, label=database[i].segment, zorder=4)
    i= i+3
    plt.plot(database[i].xaxis, database[i].y2axis, color='b', alpha=0.6, label=database[i].segment, zorder=3)
    i= i+3
    plt.plot(database[i].xaxis, database[i].y2axis, color='b', alpha=0.4, label=database[i].segment, zorder=2)
    i= i+3
    plt.plot(database[i].xaxis, database[i].y2axis, color='b', alpha=0.2, label=database[i].segment, zorder=1)
    
    
    plt.title(f'{database[i].name} for all mission segments')
    plt.xlabel(f'{database[i].xlabel} in {database[1].xunit}') 
    plt.ylabel(f'{database[i].y2label} in {database[1].y2unit}')
    plt.grid(True)
    plt.legend()
    plt.xscale('log')
    plt.yscale('log')
    
    plt.show()












        
      