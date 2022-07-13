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
from numpy import pi
from scipy.integrate import quad
from source import block_starts, block_ends, get_meta, get_data, plot_this, cleanup_text #import Functions

#########################################################################
#############   Parameters:   ###########################################
#########################################################################

sens_vol = (38.7, 38.7, 2.0) # sensitive Volume (length, width, thickness)[μm]

Q_c = 1.13*(10**-2) # critical Charge [pC] **ANNAHME**

L = data.y1achse[Energy] # ??? LET [MeV*cm^2*g^-1]  **Abhängig von Energie**

p_max = 0 #??? largest diameter if the sensitive volume [g/cm^2]

X = 3.6 # Energy needed to create ine electron-hole pair (3.6 eV in SI; 4.8 eV in GaAs) [eV]
A = 2 * (sens_vol[0]*sens_vol[1]+sens_vol[0]*sens_vol[2]+sens_vol[2]*sens_vol[1]) #surface area of sensitive volume [m^2]
e = 1.602*(10**-19) #elementary charge [C]

L_min = (X/e)*(Q_c/p_max) # required minimum LET for an upset with p_max [MeV*cm^2*g^-1]
L_max = 1.05*(10**5) # highest LET any stopping ion can deliver [MeV*cm^2*g^-1]

def F(L): # Integral LET spectrum [particles*m^-2*s^-1*sr^-1] 
    return 0 # ???

def p(L): # path length over which an ion of LET L will produce a charge Q_c
    return ((X/e) * (Q_c/L))

def D(p): # = D(p(L)) differential path length distribution in the sensitive volume of each memory cell [cm^2*g^-1]
    return 0 # ???


U = 0 # Upset Rate [bit^-1 s^-1]

def U_integral(L):
    return ( (D(p(L))*F(L)) / (L**2) )

U_integral_value = quad(U_integral, L_min, L_max)

U = pi * A * (X/e) * Q_c * U_integral_value


# Direct ionisation upset rates

# Proton induces upset rates