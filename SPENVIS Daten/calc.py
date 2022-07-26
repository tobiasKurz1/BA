# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 16:23:19 2022

Rechnungen

@author: Tobias Kurz
"""

import numpy as np
from numpy import pi, sqrt, arctan, arccos
from source import metadata, dataset


#%% differential path length

def difpld(lbound, rbound, steps, l, w, h):
     
    """ 
        Calculation of the differential path length distribution 
        Returns the probability per micrometer over chord length (micrometers)
        Uses the function G for calculating Bendels formular using the Pickel and Blandford approach
    """
    
    difpld_y = []
    difpld_x = []
    
    for s in np.linspace(lbound, rbound, steps, True):
       
        difpld = (G(s,l,w,h)+G(s,w,l,h)+G(s,l,h,w)+G(s,w,h,l)+G(s,h,w,l)+G(s,h,l,w))
        difpld_y.append(difpld)
        difpld_x.append(s)
        
        print(f'\rCalculating difpld {round(s*100/(rbound-lbound))}% ...              ', end = "")

    print("")   
    # Dataformat:
    data = dataset()
    meta = metadata()
    
    data.name = (f'Differential Path Length Distribution of Volume {l} x {w} x {h} micrometers')
    data.xaxis = difpld_x
    data.xlabel = ('Chord Length')
    data.xunit = ('μm')
    data.y1label = ('Pathlength probability per micrometer')
    data.y1unit = ('1/μm')
    data.y1axis = difpld_y
    
    meta.lines = steps
    meta.rows = -1 # Special row number as imput for plot_this function
    meta.number = (lbound, rbound)
     
    return meta, data
    
def G(s,x,y,z):
    
    """ Iterative calculation of the difpld """

    (N1, N2, N3) = (0,0,0)
    r = sqrt(x**2+y**2+z**2) # = p_max
    
    k = sqrt(x**2+y**2)
    T = sqrt(x**2+z**2)
    V = 12*x*y*z**2
    B1 = -(3*x*y/(r*T))**2
    B2 = (3*y/k)**2+B1
    B3 = -(3*x*z/(k*r))**2
    B4 = V*np.arctan(y/x)-(y*z**2/k)**2
    B5 = x**2*z**2*(z**2/k**2-3)+V*arctan(y/x)
    norm = 3*pi*(x*y+x*z+y*z)

    p = sqrt(s**2-z**2) if (s>z) else 0
    Q = sqrt((s**2)-(x**2)-(z**2)) if ((s**2)>(x**2+z**2)) else 0
    
    N1 = (B1*s+4*z) if ((s>=0)and(s<z)) else 0
    N2 = (B2*s+B4/s**3-x*(p/s)*(8+4*z**2/s**2)) if ((s>=z) and (s<T)) else 0
    N3 = (B3*s+B5/s**3+y*(Q/s)*(4+2*T**2/s**2)-(V/s**3)*arccos(x/p)) if ((s>=T) and (s<=r)) else 0  

    G_a = ((N1+N2+N3)/norm)
    
    return G_a
    
#%% Interpolation

def interp(x, y, xvalue):
    # Because of the numeric nature of the data, all values are linearly interpolated between existing ones
    yvalue = 0 

    for i in range(len(y)-1):
      
       if (xvalue > x[i]) and (xvalue < x[i+1]):
           yvalue = y[i] + ((y[i+1]-y[i])/(x[i+1]-x[i])) * (xvalue - x[i])
           break
           
       if xvalue == x[i]:
           yvalue = y[i]
           break
    
    return yvalue


#%% Adams Integral

def adamsint(L, difpl, LET, xe, Qc):
    # The used values are interpolated from existing Data
    # function which will be integrated in the next step
    # D[p(L)]*F(L) / L^2 
    
    p = xe*Qc/L
    
    D = interp(difpl.xaxis, difpl.y1axis, p) #value of difpl at position p(L)
    F = interp(LET.xaxis, LET.y1axis, L)    #value of integral LET spectrum at position L
    
    integrant = (D*F)/L**2
    
    return integrant
    
    
    

