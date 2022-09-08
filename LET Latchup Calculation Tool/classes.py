# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 15:06:20 2022

@author: Tobias Kurz
"""
from numpy import sqrt

#%% Calculaition Classes

class calc_var:
    def __init__(self, input_vars):
        self.w = input_vars.dimensions[0] * 0.0001 # convert to cm 
        self.l = input_vars.dimensions[1] * 0.0001 # convert to cm 
        self.h = input_vars.dimensions[2] * 0.0001 # convert to cm 
        self.L_min = input_vars.L_min *1000 # convert to [Mev*cm^2*g^-1]
        self.steps = input_vars.steps
        self.sVol_count = input_vars.sVol_count
        self.e = 1.602*(10**-7) #[pC] elementary charge 
        self.X = input_vars.X * (10**-6) # convert to [MeV]
        self.L_max = 1.05*(10**5) # highest LET any stopping ion can deliver [MeV*cm^2*g^-1]
        self.A = (2*self.w*self.l+2*self.l*self.h+2*self.h*self.w) *0.0001 #[m^2] surface area of sensitive volume        
        self.x = input_vars.rho * self.w # in g/cm^2
        self.y = input_vars.rho * self.l # in g/cm^2
        self.z = input_vars.rho * self.h # in g/cm^2
        self.p_max = sqrt(self.x**2+self.y**2+self.z**2) #largest diameter of the sensitive volume [g/cm^2]
        self.Q_c = (self.e*self.L_min*self.p_max)/(self.X) #minimum charge for Upset [pC]
        self.scale = input_vars.scale
        self.plot = input_vars.plot
        self.xsection = input_vars.xsection
        self.A_t = input_vars.A_t


#%% Classes

class input_var:
    def __init__(self, dimensions, X, rho, L_min, steps, sVol_count, scale, plot, xsection, A_t):
        self.dimensions = dimensions
        self.X = X
        self.rho = rho
        self.L_min = L_min
        self.steps = steps
        self.sVol_count = sVol_count
        self.scale = scale
        self.plot = plot
        self.xsection = xsection
        self.A_t = A_t

class metadata:
    def __init__(self, dataStart = [], lines = [], rows = [],  number = []):
        self.dataStart = dataStart
        self.lines = lines
        self.rows = rows
        self.number = number

class dataset:
    def __init__(self, name=[], segment='Total Mission', species = [], xaxis=[], y1axis=[], y2axis=[], xlabel=[], y1label=[], y2label=[], xunit=[], y1unit=[], y2unit=[]):
        self.name = name
        self.segment = segment
        self.species = species
        self.xaxis = xaxis
        self.y1axis = y1axis
        self.y2axis = y2axis
        self.xlabel = xlabel
        self.y1label = y1label
        self.y2label =y2label
        self.xunit = xunit
        self.y1unit = y1unit
        self.y2unit =y2unit
