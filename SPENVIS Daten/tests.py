# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 14:56:08 2022

@author: Tobias Kurz
"""
import matplotlib.pyplot as plt
import numpy as np
from numpy import pi, sqrt, arctan, arccos
from scipy.integrate import quad
from source import import_data, plot_this #import Functions

sens_vol = (1, 0.5, 0.1)
(w,l,h) = sens_vol




def ksq(x,y): 
    ksq = x**2+y**2
    return ksq
def tsq(x,z): 
    tsq = x**2+z**2
    return tsq
def t(x,z): 
    t=sqrt(tsq(x,z)) 
    return t
def rsq(x,y,z): 
    rsq = (ksq(x,y)+z*z)
    return rsq
def r(x,y,z): 
    r = sqrt(rsq(x,y,z))
    return r
def v(x,y,z): 
    v = (12*x*y*(z**2))
    return v
def psq(s,z): 
    psq = s**2-z**2
    return psq
def qsq(s,x,z):
    qsq = (s**2 - x**2 -z**2)
    return qsq

steps = 100
lsgx = []
lsgy = []

def G(s,x,y,z):
    G = 0
    
    if (s>=0 and s<z): #EQ A-9
        G=8*(y**2)*z/ksq(x,y)-s*(3*x*y/(r(x,y,z)*t(x,z)))**2
    if (s>=z and s<t(x,z)): #EQ A-10
        G=s*(3*y/sqrt(ksq(x,y)))**2-s*(3*x*y/(t(x,z)*r(x,y,z)))**2
        -x*(sqrt(psq(s,z))/s)*(8+(4*z**2)/(s**2))
        +(v(y,x,z)*np.arctan(y/x)-((y*z**2)/sqrt(ksq(x,y)))**2)/(s**3)
    if (s>=t(x,z) and s<=r(x,y,z)): #EQ A-11
        G=(-s)*(s*x*z/(r(x,y,z)*sqrt(ksq(x,y))))**2
        +(x**2*z**2*(z**2/ksq(x,y)-3)+v(x,y,z)*np.arctan(y/x))/(s**3)   
        +y*z**2*(sqrt(qsq(s,x,z))/s)*(8/tsq(x,z)+4/(s**2))
        -(v(x,y,z)/(s**3))*np.arccos(x/sqrt(psq(s,z)))
    return G
        


for s in np.linspace(0, 1.2, steps, True):
   
    difpld = (G(s,l,w,h)+G(s,w,l,h)+G(s,l,h,w)+G(s,w,h,l)+G(s,h,w,l)+G(s,h,l,w))/(pi*3*(h*w+h*l+l*w))
    lsgy.append(difpld*10)
    lsgx.append(s)

plt.figure(figsize=(10,8))
plt.plot(lsgx,lsgy)
plt.grid(True)
plt.show()










"""
number = 600


for i in range(number):
    pointA = (random.randint(0,100), random.randint(0,100))
    pointB = (random.randint(0,100), random.randint(0,100))
    
    x_values = [pointA[0], pointB[0]]
    y_values = [pointA[1], pointB[1]]
    
    plt.xlim([0,100])
    plt.ylim([0,100])
    plt.plot(x_values,y_values, color='black', alpha = 0.3)







""


















liste1 = []
liste2 = []

l = 0
Daten1 = [1, 2, 3, 4, 5],[6, 7, 8, 9, 10],[11, 12, 13, 14, 15],['a',2,3,4,5]


colorwheel = []
for s in range(len(Daten1)):
    colorwheel.append(colorsys.hsv_to_rgb((1.0/len(Daten1))*s, 1.0, 1.0))
    colorwheel[s] = [round(x) for x in colorwheel[s]]
    colorwheel[s] = '#%02x%02x%02x' % (colorwheel[s][0], colorwheel[s][1], colorwheel[s][2])



"""

#Daten1 = [s.strip("'") for s in Daten1]

# #for s in range(len(Daten1)): Daten1[s] = Daten1[s].replace("'","")
# test = map(lambda each:each.strip("'"), Daten1) 
# print (test)


# while l <= range(len(Daten1))[-1]:
    
#     liste1.append(Daten1[l][0])
#     liste2.append(Daten1[l][1])
#     liste2[2].append(Daten1[l][2])
#     print(f' L1: {liste1}')
#     print(f' L2: {liste2}')
#     l += 1