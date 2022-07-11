# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 14:56:08 2022

@author: Tobias Kurz
"""

liste1 = []
liste2 = []

l = 0
Daten1 = [1, 2, 3, 4, 5],[6, 7, 8, 9, 10],[11, 12, 13, 14, 15],['a',2,3,4,5]


#Daten1 = [s.strip("'") for s in Daten1]

#for s in range(len(Daten1)): Daten1[s] = Daten1[s].replace("'","")
test = map(lambda each:each.strip("'"), Daten1) 
print (test)


# while l <= range(len(Daten1))[-1]:
    
#     liste1.append(Daten1[l][0])
#     liste2.append(Daten1[l][1])
#     liste2[2].append(Daten1[l][2])
#     print(f' L1: {liste1}')
#     print(f' L2: {liste2}')
#     l += 1