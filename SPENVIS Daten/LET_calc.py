# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 11:14:33 2022

@author: Tobias Kurz
"""
""" 
    Annahmen:
    
    - RPP model (idealized rectangular parallellopiped)
    - LET of each Ion is constant over the dimensions of the critical volume (CREME)
    
    - Erste Tests : no Shielding
      (Später: Shielding Thickness : 0.2 cm)
    
"""

from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np
from numpy import pi, sqrt, arctan, arccos

from scipy.integrate import quad
from source import import_data, plot_this #import Functions
from calc import difpld, adamsint


#########################################################################
#############   Constants   #############################################
#########################################################################

#%% INPUTS:
    
(w,l,h) = (20, 10, 5) #[μm] dimensions of Sensitive Volume (length, width, thickness)
L_min = 100 #???[MeV*cm^2*g^-1] ANNAHME required minimum LET for an upset with p_max 
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
(wm, lm, hm) = (w *10**-6, l*10**-6, h*10**-6) # convert to [m]


#%% PARAMETERS:
L_max = 1.05*(10**5) # highest LET any stopping ion can deliver [MeV*cm^2*g^-1]
p_max = sqrt(w**2+l**2+h**2) #largest diameter if the sensitive volume [g/cm^2]
Q_c = (e*L_min*p_max)/(X) #minimum charge for Upset [pC]
S_min = Q_c/0.28
A_p = 0.5*(w*h+w*l+h*l) #Average projected Area of sensitive Volume [μm^2]
A = A_p * 4 *10**-12 #[m^2] surface area of sensitive volume
p_Lmin = (X/e)*Q_c/(L_min)

#%%  Differential Path length distribution

steps = 1000000
lbound = 0
rbound = p_Lmin


(difmeta, difdata) = difpld(lbound, rbound, steps, w, l, h)

plot_this(difmeta, difdata)

#%% Function to be integrated

func_y=[]
func_x = []



for L in np.linspace(L_min, L_max, steps, True):

    func = adamsint(L, difdata, LET_data, (X/e), Q_c)

    func_y.append(func)
    func_x.append(L)

plt.figure(figsize=(10,8))
plt.suptitle(f'Function to be Integrated \n Number of Iterations: {steps}; Stepsize: {abs(L_max-L_min)/steps}')
plt.plot(func_x,func_y)
plt.xscale('log')
plt.show()

#%% Integral Calculation

integral = 0.

stepsize = (abs(L_max-L_min)/steps)

for i in range(steps):
    
    integral = (func_y[i])*stepsize + integral


#%% Final Calculation 

U = pi * A * (X/e) * Q_c * integral

print(f'Upset Rate U = {U} [bit^-1 s^-1]')

#%% Probability Calculations



eu =  2.71828182846
err_prob = []

s_to_d = 60*60*24
sVol_count = 10**6

n = sVol_count * s_to_d

mue = n * U

curvex = range(round(mue-(0.002*mue)), round(mue+(0.002*mue)))

sigma = sqrt(n*U*(1-U))

for k in curvex:
    f = ( 1/sqrt((sigma**2)*2*pi))*eu**(-((k-mue)**2)/(2*(sigma)**2))
    err_prob.append(f*100)




# wahrscheinlichkeit integriert
chance = 0

for k in range(len(curvex)):
    chance = chance + err_prob[k]
print(chance)

plt.figure(figsize=(10,8))
plt.plot(curvex, err_prob, color='b')
plt.suptitle(f'Probability Distribution of Errors per Chip ({sVol_count} Transistors) per Day \n μ={round(mue,2)}; σ={round(sigma,2)} \n chance of outcome included in shown distribution: {round(chance,2)}%')
plt.xlabel(f'Number of Errors \n Error Rate per bit per second: {U}')
plt.ylabel('Probability in %')
plt.grid(True)

plt.show()

