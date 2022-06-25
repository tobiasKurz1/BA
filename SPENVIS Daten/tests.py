# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 14:56:08 2022

@author: Tobias Kurz
"""

liste1 = []
liste2 = []

zahl = float(5)

Daten1 = [1, 2, 3, 4, 5, 6]
Daten2 = [7, 8, 9, 10, 11, 12]
Daten3 = ['a']
Daten4 = ['b']
liste3 = [],[]
'''
liste1.append(Daten1)
liste1.append(Daten2)
liste1[0].extend(Daten3)
liste1[1].append(Daten4)
liste1[0].extend(Daten2)


print(liste1)
print(liste1[0])
print(liste1[1][6])
print(liste3)

liste3[0].extend(Daten3)
liste3[1].extend(Daten4) 
liste3[0].extend([zahl])
print(liste3)

print(zahl)
print("\n\n")
liste3 = [],[]

print(liste1)

liste1[1].pop(1)
print(liste1)'''

liste1 = [float(i) for i in Daten1]
print(liste1)