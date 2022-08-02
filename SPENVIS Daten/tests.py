# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 14:56:08 2022

@author: Tobias Kurz
"""
import matplotlib.pyplot as plt
import numpy as np
from numpy import pi, sqrt, arctan, arccos
from tabulate import tabulate
import numpy as np
from numpy import pi, sqrt, arctan, arccos
import random as random
import scipy.special as sp


class testclass:
    def __init__(self, zahl, zahlmal2):
        self.zahl = zahl
        self.zahlmal2 = zahlmal2

nummer = (1,2)


test = testclass(nummer[0],nummer[1])





"""
start = 1.4
stop = 67



test = np.logspace(np.log10(start),np.log10(stop), 50, True)

plt.figure(figsize=(30,2))
plt.plot(test,[1]*len(test), marker="o")
plt.xscale('log')
plt.show()
"""
"""
xvalue = 3.3
x = [1,2,3,4,5,6,7]
y = [0,2,2**2,2**3,2**4,2**5,2**6]


for i in range(len(y)-1):
    
    if (xvalue > x[i]) and (xvalue < x[i+1]):
        yvalue = y[i] + ((y[i+1]-y[i])/(x[i+1]-x[i])) * (xvalue - x[i])
        
    if xvalue == x[i]:
        yvalue = y[i]


print(x)
print(y)
print("\n")
print (yvalue)



"""












"""
sens_vol = (1, 0.5, 0.1)
(w,l,h) = sens_vol

lim = 1.2
steps = 100
lsgx = []
lsgy = []





def G(s,x,y,z):
    G1 = 0
    G2 = 0
    G3 = 0
    ksq = x**2.+y**2.
    tsq = x**2.+z**2.
    t=sqrt(tsq) 
    rsq = ksq+z*z
    r = sqrt(rsq)
    v = 12.*x*y*z**2
    psq = s**2.-z**2.
    qsq = s**2.-x**2-z**2
    
    if ((s>=0) and (s<z)): #EQ A-9
        G1=8*(y**2)*z/ksq-s*(3*x*y/(r*t))**2
        print(1)
    if ((s>=z) and (s<t)): #EQ A-10
        G2=s*(3*y/sqrt(ksq))**2-s*(3*x*y/(t*r))**2
        -x*(sqrt(psq)/s)*(8+4*z**2/(s**2))
        +(v*arctan(y/x)-(y*z**2/sqrt(ksq))**2)/(s**3)
        print(2)
    if ((s>=t) and (s<=r)): #EQ A-11
        G3=(-s)*(3*x*z/(r*sqrt(ksq)))**2
        +((x**2)*(z**2)*(z**2/ksq-3)+v*arctan(y/x))/(s**3)   
        +y*z**2*(sqrt(qsq)/s)*(8/tsq+4/(s**2))
        -(v/(s**3))*arccos(x/sqrt(psq))
        print(3)
    
    G = (G1+G2+G3)/(pi*3*(x*y+y*z+x*z))
    #print(f'S={round(s,3)}, G1={round(G1,3)}, G2={round(G2,3)}, G3={round(G3,3)}')

    return G
        


for s in np.linspace(0, lim, steps, True):
   
    lsgy.append((G(s,l,w,h)+G(s,w,l,h)+G(s,l,h,w)+G(s,w,h,l)+G(s,h,w,l)+G(s,h,l,w)))
    lsgx.append(s)

lsgy_ex=lsgy[:]
plt.figure(figsize=(10,8))
plt.plot(lsgx,lsgy)
lsgy_ex = [i*10 for i in lsgy_ex]
plt.plot(lsgx,lsgy_ex, '--')
plt.ylim(0,20)
plt.grid(True)
plt.show()
"""

"""








number = 20000


for i in range(number):
    pointA = (random.randint(0,100), random.randint(0,100))
    pointB = (random.randint(0,100), random.randint(0,100))
    
    x_values = [pointA[0], pointB[0]]
    y_values = [pointA[1], pointB[1]]
    print(f'{round(i/number,2)} geladen')
    plt.xlim([0,100])
    plt.ylim([0,100])
    plt.plot(x_values,y_values, alpha = 1)


























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