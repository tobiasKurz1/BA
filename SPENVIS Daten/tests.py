# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 14:56:08 2022

@author: Tobias Kurz
"""

liste1 = []
liste2 = []

zahl = float(5)

Daten1 = [1, 2, 3, 4, 0, 6],[1,2,3,4,5,5,6,3,9],[1,2,4,5,5,5,5,5,5]

zeile = 0

print(len(Daten1))
print(range(len(Daten1)))
print(Daten1[1])

for zeile in range(len(Daten1)):
    print(Daten1[zeile][4])
    if zeile == 1:
        print("Zeile 1")