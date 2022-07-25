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

import matplotlib.pyplot as plt
import numpy as np
from numpy import pi, sqrt
from source import import_data, plot_this #import Functions
from calc import difpld, adamsint


#%% INPUTS:
    
(w,l,h) = (20, 10, 5) #[μm] dimensions of Sensitive Volume (length, width, thickness)
L_min = 100 #[MeV*cm^2*g^-1] required minimum LET for an upset with p_max 
e = 1.602*(10**-7) #[pC] elementary charge 
X = 3.6 #[eV] Energy needed to create ine electron-hole pair (3.6 eV in SI; 4.8 eV in GaAs) 

# LET-Data

(metabase, database)=import_data('spenvis_nlof_srimsi.txt',',') # SPENVIS Data
#plot_this(metabase[0],database[0])
plot_this(metabase[2],database[2])
#plot_this(metabase[2],database[2])

LET_data = database[2]

#%% CONVERSIONS:

X = X*(10**-6) # convert to [MeV]

#%% PARAMETERS:
L_max = 1.05*(10**5) # highest LET any stopping ion can deliver [MeV*cm^2*g^-1]
p_max = sqrt(w**2+l**2+h**2) #largest diameter of the sensitive volume [g/cm^2]
Q_c = (e*L_min*p_max)/(X) #minimum charge for Upset [pC]
S_min = Q_c/0.28
A_p = 0.5*(w*h+w*l+h*l) #Average projected Area of sensitive Volume [μm^2]
A = A_p * 4 *10**-12 #[m^2] surface area of sensitive volume
p_Lmin = (X/e)*Q_c/(L_min)


stepx = []
Uy = []
stepcnt = 100

while stepcnt < 200000:


    steps = stepcnt
    
    #%%  Differential Path length distribution
    
  #  steps = 5000
    lbound = 0
    rbound = p_Lmin
    
    
    (difmeta, difdata) = difpld(lbound, rbound, steps, w, l, h)
    
   # plot_this(difmeta, difdata)
    
    #%% Function to be integrated
    
    func_y=[]
    func_x = []
    
    Dvec = []
    Fvec = []
    
    for L in np.linspace(L_min, L_max, steps, True):
    
        func = adamsint(L, difdata, LET_data, (X/e), Q_c, Dvec, Fvec)
    
        func_y.append(func)
        func_x.append(L)
    
    # plt.figure(figsize=(10,8))
    # plt.suptitle(f'Function to be Integrated \n Number of Iterations: {steps}; Stepsize: {abs(L_max-L_min)/steps}')
    # plt.plot(func_x,func_y)
    # plt.xscale('log')
    # plt.show()
    
    
    
    # plt.plot(range(len(Dvec)), Dvec)
    # plt.xscale('log')
    # plt.show()
    
    # plt.plot(range(len(Fvec)), Fvec)
    # plt.xscale('log')
    # plt.yscale('log')
    # plt.show()
    
    #%% Integral Calculation
    
    integral = 0.
    
    stepsize = (abs(L_max-L_min)/steps)
    
    for i in range(steps):
        
        integral = (func_y[i])*stepsize + integral
    
    
    #%% Final Calculation 
    
    U = pi * A * (X/e) * Q_c * integral
    
    Uy.append(U)
    stepx.append(stepcnt)

    print(stepcnt)
    print(f'Upset Rate U = {U} [bit^-1 s^-1]')
    stepcnt = round(stepcnt*1.1)
    
plt.figure(figsize=(10,8))
plt.grid(True)    
plt.plot(stepx, Uy, marker='.')
plt.xscale('log')
plt.yscale('linear')
plt.show()

#%% Probability Calculations



# eu =  2.71828182846
# err_prob = []

# s_to_d = 60*60*24
# sVol_count = 10**6

# n = sVol_count * s_to_d

# mue = n * U

# curvex = range(round(mue-(0.002*mue)), round(mue+(0.002*mue)))

# sigma = sqrt(n*U*(1-U))

# for k in curvex:
#     f = ( 1/sqrt((sigma**2)*2*pi))*eu**(-((k-mue)**2)/(2*(sigma)**2))
#     err_prob.append(f*100)




# # wahrscheinlichkeit integriert
# chance = 0

# for k in range(len(curvex)):
#     chance = chance + err_prob[k]
# print(chance)

# plt.figure(figsize=(10,8))
# plt.plot(curvex, err_prob, color='b')
# plt.suptitle(f'Probability Distribution of Errors per Chip ({sVol_count} Transistors) per Day \n μ={round(mue,2)}; σ={round(sigma,2)} \n chance of outcome included in shown distribution: {round(chance,2)}%')
# plt.xlabel(f'Number of Errors \n Error Rate per bit per second: {U}')
# plt.ylabel('Probability in %')
# plt.grid(True)

# plt.show()

