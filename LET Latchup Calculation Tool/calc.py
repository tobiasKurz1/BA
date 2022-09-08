# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 16:23:19 2022

Rechnungen

@author: Tobias Kurz
"""
import matplotlib.pyplot as plt
import numpy as np
from source import plot_this #import Functions
from classes import metadata, dataset
import sys
from numpy import pi, sqrt, arctan, arccos



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
    
    data.name = (f'Differential Path Length Distribution of Volume {l} x {w} x {h} g/cm^2')
    data.xaxis = difpld_x
    data.xlabel = ('Chord Length')
    data.xunit = ('g/cm^2')
    data.y1label = ('Pathlength probability per micrometer')
    data.y1unit = ('cm^2/g')
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

def adamsint(L, difpl, LET, p_L):
    # The used values are interpolated from existing Data
    # function which will be integrated in the next step
    # D[p(L)]*F(L) / L^2 
    
    D = interp(difpl.xaxis, difpl.y1axis, p_L) #value of difpl at position p(L)
    F = interp(LET.xaxis, LET.y1axis, L)    #value of integral LET spectrum at position L
    
    integrant = (D*F)/L**2
    
    return integrant
#%% Upsetrate
  
def upsetrate(var, LET_data, LET_meta, Proton_data, Proton_meta):

    lbound = 0
    
    rbound = var.p_max
 
    if var.plot: plot_this(LET_meta,LET_data)
    if var.plot: plot_this(Proton_meta,Proton_data)

    (difmeta, difdata) = difpld(lbound, rbound, var.steps, var.x, var.y, var.z)
    
    if var.plot: plot_this(difmeta, difdata)
    
    #%%  Differential Path length distribution
   
    func_y=[]
    func_x = []
    
    if ('log') in var.scale: scale = np.logspace(np.log10(var.L_min), np.log10(var.L_max), var.steps, True)
    if ('lin') in var.scale: scale = np.linspace(var.L_min, var.L_max, var.steps, True)
    if (not(('lin') in var.scale) and not (('log') in var.scale)): print("ERROR!\nPlease enter scale 'lin' or 'log'.\nExiting Program now..."); sys.exit()
    
    p_Lscale=[]
    
    
    for i in range(var.steps):
        L = scale[i]
       
        p_L = (var.X/var.e)*var.Q_c/L
        p_Lscale.append(p_L)
        func = adamsint(L, difdata, LET_data, p_L)
        func_y.append(func)
        func_x.append(L)
        print(f'\rInterpolating data {round((L-var.L_min)*100/abs(var.L_max-var.L_min))}% ...              ', end = "")
    print("")
   
    
    if var.plot:
        plt.figure(figsize=(10,8))
        plt.suptitle(f'Function to be Integrated \n Number of Iterations: {var.steps}; Stepsize: {abs(var.L_max-var.L_min)/var.steps}')
        plt.plot(func_x,func_y)
        plt.xscale('log')
        plt.show()
   

#%% Integral Calculation

    integral = 0.

    for i in range(1,var.steps):
    
        integral = (func_y[i])*(scale[i]-scale[i-1])+integral
        print(f'\rCalculating integral {round(i*100/(var.steps))}% ...              ', end = "")

    print("") 
    
#%% Nuclear Proton reaction

    U_prot = 0
    
    if not(var.xsection == 0):
        
        protint = 0
        proty = []      
        
        if ('log') in var.scale: protx = np.logspace(0, np.log10(max(Proton_data.xaxis)), var.steps, True)
        if ('lin') in var.scale: protx = np.linspace(0, max(Proton_data.xaxis), var.steps, True)
        
        for i in range(len(protx)):
            if protx[i] > var.A_t:
                proty.append(interp(Proton_data.xaxis,Proton_data.y2axis,protx[i]) * var.xsection)
            else: proty.append(0)
            print(f'\rCalculating proton reaction curve {round(i*100/(var.steps))}% ...              ', end = "")
            
        if var.plot:
            plt.figure(figsize=(10,8))
            plt.suptitle("Nuclear Proton function (to be intregrated)")
            plt.plot(protx,proty)
            plt.xscale('log')
            plt.yscale('log')
            plt.show()
   
        #Integral:
            
        for i in range(1,len(proty)):
            protint = proty[i]*(protx[i]-protx[i-1])+protint
        
        
  #      print(f'\n L_c = {var.L_c}\n protint = {protint}\n')
        
        U_prot = (10**-4)*4*pi*protint
        
#%% Final Calculation 

    U_LET = pi * var.A * (var.X/var.e) * var.Q_c * integral

    U = U_LET + U_prot
    
#%% Probability Calculations


    print(f'\nUpset rate caused by proton nuclear reactions: {U_prot} [bit^-1 s^-1] ({round(U_prot*100/U,2)}%)')
    print(f'Upset rate caused by Cosmic Rays (LET):        {U_LET} [bit^-1 s^-1] ({round(U_LET*100/U,2)}%)')
    print(f'Total Upset Rate (Proton + LET):               {U} [bit^-1 s^-1]')

    eu =  2.71828182846
    err_prob = []
    
    s_to_d = 60*60*24
    d_to_y = 265.2425
    
    
    n = var.sVol_count * s_to_d * d_to_y
    
    mue = n * U # Expected count
    
    sigma = sqrt(n*U*(1-U))
    
    if ((n*U*(1-U))<= 9): 
        
        print("\nProbability U is too low! Gaussian probability distribution will not give a reasonable result.")
        print(f'Most likely outcome μ={mue} [Errors per year].\nTry lowering L_min or increasing transistor count.\n')
        return(0)
    
    curvex = range(round(mue-(mue*(2*sigma/mue))), round(mue+(mue*(2*sigma/mue))))
    
    
    for k in curvex:
        f = ( 1/sqrt((sigma**2)*2*pi))*eu**(-((k-mue)**2)/(2*(sigma)**2))
        err_prob.append(f*100)
    
    
    
    
    # wahrscheinlichkeit integriert
    chance = 0
    
    for k in range(len(curvex)):
        chance = chance + err_prob[k]
    print(f'\nChance of {round(mue)} ± {round(mue-curvex[0])} faulty Transistors per Year: {round(chance,3)}%')
    
    if var.plot:
        plt.figure(figsize=(10,8))
        plt.plot(curvex, err_prob, color='b')
        plt.suptitle(f'Probability Distribution of Errors per Chip ({var.sVol_count} Transistors) per Year \n μ={round(mue,2)}; σ={round(sigma,2)}\nLmin = {var.L_min}')
        plt.xlabel(f'Number of Errors \n\n Error Rate per bit per second: {U}\nChance of {round(mue)} ± {round(mue-curvex[0])} Errors per Chip per Year: {round(chance,3)}%')
        plt.ylabel('Probability in %')
        plt.grid(True)
        
        plt.show()
    
    return U
