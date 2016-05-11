# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 17:49:20 2016

@author: Tobias

Testcode, um die Funktionalität des RK4-Verfahrens zu überprüfen
"""

import numpy as np
import RK4 as RK
import matplotlib.pyplot as plt

#Eingabe systemabhängiger Parameter
z_0=np.array([[1],[2],[3]])    #Anfangswertvektor, bereits in gewünschter Matrixschreibweise

T=10    #Endzeit
t0=2    #Anfangszeit
dt=0.1              #Zeitschrittlaenge
t = np.arange(t0,T,dt)      #Zeitarray


A=np.matrix("-0.4, 0, 0; 0, 0.1, 0; 0, 0, -0.3")    #Matrix A
D=np.array([np.matrix("-0.4, 0, 0; 0, 0.1, 0; 0, 0, -0.3"),
            np.matrix("-0.4, 0, 0; 0, 0.1, 0; 0, 0, -0.3"),
            np.matrix("-0.4, 0, 0; 0, 0.1, 0; 0, 0, -0.3")])    #Array D hat als Einträge Matrizen B1,B2,...
            
C=np.matrix("-0.4, 0, 0; 0, 0.1, 0; 0, 0, -0.3")    #Matrix C
u=np.array([[1],[1],[2]])      #Anregung u


#---------------------------------------------------------------------------------------------------------------------
const=C*u  #C*u ist immer konstant, kann deshalb einfach uebergeben werden


     
for i in range(len(D)):
    B=+D[i]*u[i]

teta=list((A,B,const))  #Parameterset


def f(x,teta):       #Gibt die Zeitableitung x_dot wider
    return (teta[0]+teta[1])*x+teta[2]     
    


z=RK.RK4_method(f,teta,z_0,dt,t0,T)
#print(z[1,:],t)
plt.figure()
for i in range(len(z_0)):
    plt.plot(t,np.squeeze(np.asarray(z[i,:])))      #Jede Zeile wird gegen die Zeit geplottet

plt.savefig("test")

