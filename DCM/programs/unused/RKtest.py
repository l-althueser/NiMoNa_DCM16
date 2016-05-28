# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 17:49:20 2016

@author: Tobias

Testcode, um die Funktionalität des RK4-Verfajrens zu überprüfen
"""

import numpy as np
import RK4 as RK
import matplotlib.pyplot as plt


z_0=np.array([[1],[2]])    #Anfangswertvektor, bereits in gewünschter Matrixschreibweise

T=2.2
t0=2
dt=0.1              
t = np.arange(t0,T,dt) 

def f(x):       #Gibt die Zeitableitung x_dot wider
	x_dot=x     #So muss x(t)=exp(t) herauskommen
    return x_dot

z=RK.RK4_method(f,z_0,dt,t0,T)

#print(z,t)
plt.figure()
for i in range(len(z_0)):
    plt.plot(t,z[i,:])      #Jede Zeile wird gegen die Zeit geplottet

plt.savefig("test")

