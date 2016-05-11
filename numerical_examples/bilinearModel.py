# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 17:49:20 2016

@author: Tobias

Testcode, um die Funktionalität des RK4-Verfahrens zu überprüfen
"""

import numpy as np
import RK4 as RK
import matplotlib.pyplot as plt


z_0=np.array([[1],[2],[3]])    #Anfangswertvektor, bereits in gewünschter Matrixschreibweise

T=2.2
t0=2
dt=0.1              
t = np.arange(t0,T,dt) 

def f(x):       #Gibt die Zeitableitung x_dot wider
    A=np.matrix("-0.4, 0, 0; 0, 0.1, 0; 0, 0, -0.3")    #Matrix A
    
    x_dot=A*x     #So muss x(t)=exp(t) herauskommen
    #print(x_dot,'hi')
    return x_dot

z=RK.RK4_method(f,z_0,dt,t0,T)
print(z[1,:],t)
plt.figure()
for i in range(len(z_0)):
    plt.plot(t,z[i,:])      #Jede Zeile wird gegen die Zeit geplottet

plt.savefig("test")

