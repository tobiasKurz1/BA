# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 16:23:19 2022

Rechnungen

@author: Tobias Kurz
"""

import numpy as np
from numpy import pi, sqrt, arctan, arccos
from source import metadata, dataset
from scipy.integrate import quad

#%% differential path length

def difpld(lbound, rbound, steps, l, w, h):
     
    """ 
        Calculation of the differential path length distribution 
    
        Returns the probability per micrometer over chord length (micrometers)
        
        Also returns the bendel-Integral Cs of the probability when all is uncommented

    """
    
    difpld_y = []
   # Cs_y = []
    difpld_x = []
    
    for s in np.linspace(lbound, rbound, steps, True):
       
        difpld = (G(s,l,w,h)+G(s,w,l,h)+G(s,l,h,w)+G(s,w,h,l)+G(s,h,w,l)+G(s,h,l,w))
      #  difpld = (G(s,l,w,h)[0]+G(s,w,l,h)[0]+G(s,l,h,w)[0]+G(s,w,h,l)[0]+G(s,h,w,l)[0]+G(s,h,l,w)[0])
      #  sumJ = (G(s,l,w,h)[1]+G(s,w,l,h)[1]+G(s,l,h,w)[1]+G(s,w,h,l)[1]+G(s,h,w,l)[1]+G(s,h,l,w)[1])
      #  Cs = sumJ
        #Cs = 1- sumJ/(3*pi*(l*w+l*h+w*h))
        difpld_y.append(difpld)
      #  Cs_y.append(Cs)
        difpld_x.append(s)
     
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
    meta.rows = -1
    meta.number = (lbound, rbound)
     
    return meta, data #, Cs_y
    
def G(s,x,y,z):
    
    """ Bendel-Approach for iterative calculation of the difpld """

    (N1, N2, N3) = (0,0,0)
  #  (I1, I2, I3, J1, J2, J3) = (0, 0, 0, 0, 0, 0)
    r = sqrt(x**2+y**2+z**2) # = p_max
    
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
    
    if ((s>=0)and(s<z)):
        N1 = B1*s+4*z 
      #  I1 = B1*s**2/2 + 4 * z * s
      #  J1 = I1
        
    if ((s>=z) and (s<T)):
        N2 = B2*s+B4/s**3-x*(p/s)*(8+4*z**2/s**2) 
      #  I2 = B2*s**2/2-B4/(2*s**2)
      #  +x*p*(2*z**2/s**2-8) + 6*x*z*arccos(s/s)
      #  J2 = I2 + B6    
        
    if ((s>=T) and (s<=r)):
        N3 = B3*s+B5/s**3+y*(Q/s)*(4+2*T**2/s**2)-(V/s**3)*np.arccos(x/p) 
      #  I3 = B3*s**2/2 - B5/(2*s**2)
      #  +y*Q*(4-T**2/s**2)-6*x*y*(p/s)**2*arccos(x/p)
      #  J3 = I3 + B6 -3*x**2 + 1.5*pi*x*z      
        
   # sumJ = J1 + J2 + J3 
    G_a = ((N1+N2+N3)/norm)
    
    return G_a #,sumJ
    
#%% Interpolation

def interp(x, y, xvalue):
   
    yvalue = 0 

    for i in range(len(y)-1):
      
       if (xvalue > x[i]) and (xvalue < x[i+1]):
           yvalue = y[i] + ((y[i+1]-y[i])/(x[i+1]-x[i])) * (xvalue - x[i])
           
       if xvalue == x[i]:
           yvalue = y[i]
    
    return yvalue


#%% Adams Integral

def adamsint(L, difpl, LET, xe, Qc):
    
    #integral of D[p(L)]*F(L) / L^2 
    
    p = xe*Qc/L
    
    D = interp(difpl.xaxis, difpl.y1axis, p) #value of difpl at position p(L)
    F = interp(LET.xaxis, LET.y1axis, L)    #value of integral LET spectrum at position L
    
    integral = (D*F)/L**2
    
    return integral
    
    
    

