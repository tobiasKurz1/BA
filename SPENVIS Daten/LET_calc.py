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
import matplotlib.pyplot as plt
import numpy as np
from numpy import pi, sqrt, arctan, arccos
from scipy.integrate import quad
from source import import_data, plot_this #import Functions

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
steps = 1000
lsgx =[]
lsgy = []

def F(s,x,y,z):

    r = sqrt(x**2+y**2+z**2) #??? = p_max,  ggf umbennennen
    
    k = sqrt(x**2+y**2)
    T = sqrt(x**2+z**2)
    V = 12*x*y*z**2
    B1 = -(3*x*y/(r*T))**2
    B2 = (3*y/k)**2+B1
    B3 = -(3*x*z/(k*r))**2
    B4 = V*np.arctan(y/x)-(y*z**2/k)**2
    B5 = x**2*z**2*(z**2/k**2-3)+V*np.arctan(y/x)
  #  B6 = 3*y**2*z**2/k**2+6*x*y*np.arctan(y/x)
    norm = 3*pi*(x*y+x*z+y*z)

    p = sqrt(s**2-z**2) if (s>z) else 0
    Q = sqrt((s**2)-(x**2)-(z**2)) if ((s**2)>(x**2+z**2)) else 0
    N1 = B1*s+4*z if ((s>=0)and(s<z)) else 0
    N2 = B2*s+B4/s**3-x*(p/s)*(8+4*z**2/s**2) if ((s>=z) and (s<T)) else 0
    N3 = B3*s+B5/s**3+y*(Q/s)*(4+2*T**2/s**2)-(V/s**3)*np.arccos(x/p) if ((s>=T) and (s<=r)) else 0
    F = ((N1+N2+N3)/norm)
    return F

for s in np.linspace(0, 1.2, steps, True):
    lsgy.append(F(s,l,w,h)+F(s,w,l,h)+F(s,l,h,w)+F(s,w,h,l)+F(s,h,w,l)+F(s,h,l,w))
    lsgx.append(s)
    
    
    
    
lsgy_ex=lsgy[:]
plt.figure(figsize=(10,8))
plt.plot(lsgx,lsgy)
lsgy_ex = [i*10 for i in lsgy_ex]
plt.plot(lsgx,lsgy_ex, '--')
plt.ylim(0,25)
plt.grid(True)

plt.show()

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