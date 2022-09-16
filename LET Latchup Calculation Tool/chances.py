# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 14:50:06 2022

@author: Tobias Kurz
"""
import matplotlib.pyplot as plt
import numpy as np
from source import plot_this #import Functions
from classes import metadata, dataset
import sys
from numpy import pi, sqrt, arctan, arccos

U = 1.0835 * 10 **-11

eu =  2.71828182846
err_prob = []

s_to_d = 60*60*24
d_to_y = 365.2425


n = s_to_d * d_to_y

mue = n * U # Expected count

sigma = sqrt(n*U*(1-U))

if ((n*U*(1-U))<= 9): 
    
    print("\nProbability U is too low! Gaussian probability distribution will not give a reasonable result.")
    print(f'Most likely outcome μ={mue} [Errors per year].\nTry lowering L_min or increasing transistor count.\n')
    
    #Poisson Distribution for 1 or more events in 10 years:
   
    print(f'Chance of one or more SEEs in 10 years: {round(100*(1 - eu**(-mue*10)),2)}% \nIn 1000 years: {round(100*(1 - eu**(-mue*1000)),2)}%')
    print(U)
    sys.exit()

curvex = range(round(mue-(mue*(2*sigma/mue))), round(mue+(mue*(2*sigma/mue))))


for k in curvex:
    f = ( 1/sqrt((sigma**2)*2*pi))*eu**(-((k-mue)**2)/(2*(sigma)**2))
    err_prob.append(f*100)




# wahrscheinlichkeit integriert
chance = 0

for k in range(len(curvex)):
    chance = chance + err_prob[k]
print(f'\nChance of {round(mue)} ± {round(mue-curvex[0])} faulty Transistors per Year: {round(chance,3)}%')


  
print(U)