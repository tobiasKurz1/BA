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
from calc import difpld


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
plot_this(metabase[0],database[0])
plot_this(metabase[1],database[1])
plot_this(metabase[2],database[2])

#%% CONVERSIONS:

X = X*(10**-6) # convert to [MeV]
(wm, lm, hm) = (w *10**-6, l*10**-6, h*10**-6) # convert to [m]


#%% PARAMETERS:
L_max = 1.05*(10**5) # highest LET any stopping ion can deliver [MeV*cm^2*g^-1]
p_max = sqrt(wm**2+lm**2+hm**2) #largest diameter if the sensitive volume [g/cm^2]
Q_c = (e*L_min*p_max)/X #minimum charge for Upset [pC]
S_min = Q_c/0.28
A_p = 0.5*(wm*hm+wm*lm+hm*lm) #Average projected Area of sensitive Volume [m^2]
A = A_p * 4 #[m^2] surface area of sensitive volume

#%%  Differential Path length distribution


steps = 1000
lbound = 0
rbound = 25
X1 =[]
Y1 = []


(difmeta, difdata) = difpld(lbound, rbound, steps, w, l, h)

plot_this(difmeta, difdata)




"""




E_R = 0 # Error Rate for sensitive Volume (events/day)

def E_R_integral(S):
    return (  )

E_R_integral_value = quad(E_R_integral, S_min, S_max)

#E_R = A_p * 

    
    

## Rechnung:


       """                                                                



"""


#%% Iterating Data:
db_data = 17    

i = 0 # Iterator
    
L = database[db_data].xaxis[i] # LET [MeV*cm^2*g^-1]  **Abhängig von Integral Flux**
F = database[db_data].y1axis[i] # Integral LET spectrum [particles*m^-2*s^-1*sr^-1] 
    
def p(L): # path length over which an ion of LET L will produce a charge Q_c
    return ((X/e) * (Q_c/L))

def D(p): # = D(p(L)) differential path length distribution in the sensitive volume of each memory cell [cm^2*g^-1]
    return 0 # ???


U = 0 # Upset Rate [bit^-1 s^-1]

def U_integral(L):
    return ( (D(p(L))*F) / (L**2) )

U_integral_value = quad(U_integral, L_min, L_max)

U = pi * A * (X/e) * Q_c * U_integral_value


# Direct ionisation upset rates

# Proton induces upset rates



#plot_this(metabase[0], database[0])
"""