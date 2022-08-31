"""

Program LET_calc
___________________

This programm comuptes the Upset rate due to direct ionisation fo individual particles.
Each bit on the chip is assumed as a sensitive Volume of dimesions w, l, h in micrometers.
The sensitive Volume (SV) shape is idealized as a rectangular parallellopiped (RPP).
Also assumed is that the LET of each Ion is constant over the dimensions of the critical volume.
The output Upset Rate is translated into a probability distribution using a gaussian standard distribution.


Imputs are:
    (w,l,h)     : Dimensions of the sensitive Volume [μm]
    L_min       : Required minimum LET for an Upset with p_max (largest path through the SV) [MeV*cm^2*g^-1]
    - alternatively the code can easily be reprogrammed to use Q_c as a dimensioning factor instead of L_min - 
    X           : Energy needed to create ine electron-hole pair (3.6 eV in SI; 4.8 eV in GaAs) [eV]
    LET_data    : Integral LET spectrum at the specific mission or mission Segment, derived from SPENVIS file "spenvis_nlof_srimsi.txt".
    steps       : Number of steps for the difpld and integration (for accurate results at >100.000 is advised)
    sVol_count  : Number of Transistors per Chip (used for probability calculations)

Outputs are:
    Graphic     : differential and integral LET spectra (SPENVIS Data)
    Graphic     : Differental path length distribution (difpld) of the SV
    Graphic     : Probability distribution of Errors per Day per Chip
    U           : Upset Rate in events per bit per second
    
Functions Used:
    import_data : Importing and Sorting data from SPENVIS standard text output
    plot_this   : Plots data from import_data format
    difpld      : Generates difpld diagramm based on SV and range
    adamsint    : Computes the function, which is later to be integrated for the final calculation
    
"""
from classes import input_var, calc_var
from source import output_variables, usercheck, import_data, usersurvey #import Functions
from calc import upsetrate


#%% Input variables

file_name        = 'spenvis_nlof_srimsi.txt'
dimensions       = (20,10,5)
X                = 3.6
L_min            = 10000
steps            = 1000
transistorcnt    = 10**6
axis_scale       = 'log'
plot_graphs      = False


#%%

    
(metabase, database)=import_data(file_name,',') # SPENVIS Data
chosenDB = usersurvey(database) # Read and present data from Database to choose from
(LET_meta, LET_data) = (metabase[chosenDB], database[chosenDB]) # apply chosen Data

print(f'\nLET Data used: {LET_data.name} in {LET_data.segment}')

inputs = input_var(dimensions, X, L_min, steps, transistorcnt, axis_scale, plot_graphs)      #Default input variables

while True:

    variables = usercheck(inputs) # Function to check variables and change settings

    variables = calc_var(inputs)    # Completes the list of Varibles based on Input

    output_variables(variables)     # Outputs calculated Variables

    U = upsetrate(variables , LET_data, LET_meta) # Calculates Upsetrate

    print("\n##################################################################################################")


