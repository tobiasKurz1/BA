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
from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np
from numpy import pi, sqrt
from source import import_data, plot_this, usersurvey #import Functions
from calc import difpld, adamsint
import sys

#%% INPUTS:
    
(w,l,h) = (20, 10, 50) #[μm] dimensions of Sensitive Volume (length, width, thickness)
L_min = 5 #[MeV*cm^2*mg^-1] required minimum LET for an upset with p_max 
e = 1.602*(10**-7) #[pC] elementary charge 
X = 3.6 #[eV] Energy needed to create one electron-hole pair (3.6 eV in SI; 4.8 eV in GaAs) 


(metabase, database)=import_data('spenvis_nlof_srimsi.txt',',') # SPENVIS Data

chosenDB = usersurvey(database) # Read and present data from Database to choose from

LET_data = database[chosenDB] # apply chosen Data




#%% CONVERSIONS:
L_min = L_min * 10**3 # convert to [Mev*cm^2*g^-1]
X = X*(10**-6) # convert to [MeV]

#%% PARAMETERS:
    
L_max = 1.05*(10**5) # highest LET any stopping ion can deliver [MeV*cm^2*g^-1]
p_max = sqrt(w**2+l**2+h**2) #largest diameter of the sensitive volume [g/cm^2]
Q_c = (e*L_min*p_max)/(X) #minimum charge for Upset [pC]
S_min = Q_c/0.28
A_p = 0.5*(w*h+w*l+h*l) #Average projected Area of sensitive Volume [μm^2]
A = A_p * 4 *10**-12 #[m^2] surface area of sensitive volume
p_Lmin = (X/e)*Q_c/(L_min)

steps = 50
lbound = 0
rbound = p_Lmin
sVol_count = 100

if (L_min > L_max): print("ERROR: Could not Compute! (L_min > L_Max)\nExiting Program..."); sys.exit()

#%%
print("\nCheck before calculating:\n")

inputview = [["(1)","w,l,h", f'{w}, {l}, {h}' ,"μm"],
             ["(2)","L_min", L_min, "MeV*cm^2*g^-1"],
             ["(3)","File", f'{database[chosenDB].name} in {database[chosenDB].segment}', " - "],
             ["(4)","Steps", "{:.2e}".format(steps), " - "],
             ["(5)","Predicted Stepsize", abs(L_max-L_min)/steps, "-" ],
             ["(6)","Number of Transistors", "{:.2e}".format(sVol_count), " - "]]

print(tabulate(inputview, headers=["","Name","Value","Unit"]))

choice = (input("Proceed or change settings? (J/N) "))
if (choice == 'n') or (choice == 'N'): print("Exiting Program..."); sys.exit()
#if choice


plot_this(metabase[chosenDB],database[chosenDB]) # plot chosen Data

  
 #%%  Differential Path length distribution
 

(difmeta, difdata) = difpld(lbound, rbound, steps, w, l, h)
 
#plot_this(difmeta, difdata)
 
#%% Function to be integrated
 
func_y=[]
func_x = []
logscale = np.logspace(np.log10(L_min), np.log10(L_max), steps, True)
linscale = np.linspace(L_min, L_max, steps, True)
p_Lscale=[]

for i in range(steps):
    L = logscale[i]
    
    p_L = (X/e)*Q_c/L
    p_Lscale.append(p_L)
    func = adamsint(L, difdata, LET_data, p_L)
    func_y.append(func)
    func_x.append(L)
    print(f'\rInterpolating data {round((L-L_min)*100/abs(L_max-L_min))}% ...              ', end = "")
print("") 

plt.figure(figsize=(10,8))
plt.suptitle(f'Function to be Integrated \n Number of Iterations: {steps}; Stepsize: {abs(L_max-L_min)/steps}')
plt.plot(func_x,func_y)
plt.xscale('log')
plt.show()

 
#%% Integral Calculation

integral = 0.

stepsize = (abs(L_max-L_min)/steps)

for i in range(1,steps):
    
    integral = (func_y[i])*(logscale[i]-logscale[i-1])+integral
    print(f'\rCalculating integral {round(i*100/(steps))}% ...              ', end = "")

print("")    
#%% Final Calculation 

U = pi * A * (X/e) * Q_c * integral

print(f'\nUpset Rate U = {U} [bit^-1 s^-1]')

#%% Probability Calculations

eu =  2.71828182846
err_prob = []

s_to_d = 60*60*24*365


n = sVol_count * s_to_d

mue = n * U # Expected count

sigma = sqrt(n*U*(1-U))

if ((n*U*(1-U))<= 9): 
    print("\nProbability U is too low! Gaussian probability distribution will not give a reasonable result.")
    print(f'Most likely outcome μ={mue} [Errors per day].\nTry lowering L_min or increasing transistor count.\n\nThe program will exit now.'); sys.exit()
    print(f'Most likely outcome μ={mue*365} [Errors per year].')
curvex = range(round(mue-(mue*(2*sigma/mue))), round(mue+(mue*(2*sigma/mue))))


for k in curvex:
    f = ( 1/sqrt((sigma**2)*2*pi))*eu**(-((k-mue)**2)/(2*(sigma)**2))
    err_prob.append(f*100)




# wahrscheinlichkeit integriert
chance = 0

for k in range(len(curvex)):
    chance = chance + err_prob[k]
print(f'Chance of {round(mue)} ± {round(mue-curvex[0])} Errors per Chip per Year: {round(chance,3)}%')

plt.figure(figsize=(10,8))
plt.plot(curvex, err_prob, color='b')
plt.suptitle(f'Probability Distribution of Errors per Chip ({sVol_count} Transistors) per Year \n μ={round(mue,2)}; σ={round(sigma,2)}\nLmin = {L_min}')
plt.xlabel(f'Number of Errors \n\n Error Rate per bit per second: {U}\nChance of {round(mue)} ± {round(mue-curvex[0])} Errors per Chip per Year: {round(chance,3)}%')
plt.ylabel('Probability in %')
plt.grid(True)

plt.show()

