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

from scipy.integrate import quad
from source import import_data, plot_this #import Functions
from calc import difpld

(database, metabase)=import_data('spenvis_nlof_srimsi.txt',',')

#########################################################################
#############   Parameters:   ###########################################
#########################################################################





"""
# Pickel, Blandford - Rechnung:
    
L_min = 100 #??? ANNAHME required minimum LET for an upset with p_max [MeV*cm^2*g^-1]
    
e = 1.602*(10**-7) #elementary charge [pC]
X = 3.6 # Energy needed to create ine electron-hole pair (3.6 eV in SI; 4.8 eV in GaAs) [eV]
X = X*(10**-6) # convert to [MeV]

sens_vol = (38.7, 38.7, 2.0) # dimensions of Sensitive Volume (length, width, thickness)[μm]
sens_vol = [s * (10**-6) for s in sens_vol] # convert to [m]

S_max = sqrt(sens_vol[0]**2+sens_vol[1]**2+sens_vol[2]**2) #largest diameter if the sensitive volume [g/cm^2]

Q_c = (e*L_min*S_max)/X #minimum charge for Upset [pC]

S_min = Q_c/0.28

A_p = 0.5*(sens_vol[0]*sens_vol[1]+sens_vol[0]*sens_vol[2]+sens_vol[2]*sens_vol[1]) #Average projected Area of sensitive Volume [m^2]

E_R = 0 # Error Rate for sensitive Volume (events/day)

def E_R_integral(S):
    return (  )

E_R_integral_value = quad(E_R_integral, S_min, S_max)

E_R = A_p * 

"""









#SPENVIS - Rechnung:

sens_vol = (1, 0.5, 0.1)
#sens_vol = (38.7, 38.7, 2.0) # dimensions of Sensitive Volume (length, width, thickness)[μm]
#sens_vol = [s * (10**-6) for s in sens_vol] # convert to [m]
(w,l,h) = sens_vol
steps = 10000
lbound = 0
rbound = 1.2
X1 =[]
Y1 = []
Y2 = []



(X1, Y1, Y2) = difpld(lbound, rbound, steps, w, l, h)


plt.figure(figsize=(10,8))
plt.plot(X1,Y1)
plt.plot(X1,Y2)

#plt.plot(lsgx,lsgy_ex, '--')
plt.ylim(0,20)
plt.grid(True)

plt.show()

"""
L_min = 100 #??? ANNAHME required minimum LET for an upset with p_max [MeV*cm^2*g^-1]
L_max = 1.05*(10**5) # highest LET any stopping ion can deliver [MeV*cm^2*g^-1]

p_max = sqrt(x**2+y**2+z**2) #largest diameter if the sensitive volume [g/cm^2]


X = 3.6 # Energy needed to create ine electron-hole pair (3.6 eV in SI; 4.8 eV in GaAs) [eV]
X = X*(10**-6) # convert to [MeV]
A = 2 * (x*y+x*z+y*z) #surface area of sensitive volume [m^2]
e = 1.602*(10**-7) #elementary charge [pC]


# Q_c = (e*L_min*p_max)/X #minimum charge for Upset [pC]
"""
#%% Differential Path length distribution



    
    
    

## Rechnung:


                                                                       



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