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
from classes import input_var, calc_var
from source import output_variables, usercheck, import_data, usersurvey, basicinput #import Functions
from calc import upsetrate
import sys

#%% Default Input variables

file_name        = 'spenvis_nlof_srimsi_1cm.txt'
dimensions       = (10000,10000,2000)
X                = 3.6
rho              = 2.33
L_min            = 2.3460824318873357
steps            = 10000
transistorcnt    = 1
axis_scale       = 'log'
sat_xsection     = 1*10**-8
A_t              = 20
plot_graphs      = False
switch           = (False, True) #LET, Proton


#%%
out = 2 #Internal Option Output Variable 

while out==2: 
    
    (metabase, database)=import_data(file_name,',') # SPENVIS Data
    
    print(f'\nChosen file: "{file_name}"\n')
    (LET_meta, LET_data, Proton_meta, Proton_data, out) = usersurvey(metabase, database) # Read and present data from Database to choose from
    if out == 2 : file_name = basicinput("text", "Please enter the name of the new file: ")
    
inputs = input_var(dimensions, X, rho, L_min, steps, transistorcnt, axis_scale, plot_graphs, sat_xsection, A_t, switch)      #Default input variables



if out ==1: # Iterator for the proton and LET datasets, if "calculate for all" is selected
    protdata = 1
    letdata = 2
        

while True:
    
    if out==1: (LET_meta, LET_data, Proton_meta, Proton_data) = (metabase[letdata], database[letdata], metabase[protdata], database[protdata])
 
    print(f'\n\n#################### {LET_data.segment} ####################')    

    inputs = usercheck(inputs)      # Function to check variables and change settings

    variables = calc_var(inputs)    # Completes the list of Varibles based on Input

    output_variables(variables)     # Outputs calculated Variables

    U = upsetrate(variables , LET_data, LET_meta, Proton_data, Proton_meta) # Calculates Upsetrate
    
    if out==1: 
        protdata = protdata+3; letdata = letdata+3
        if letdata>len(database): sys.exit()
   
   

   
      