# -*- coding: utf-8 -*-
"""
@author: Tobias
         Timo
         
Beschreibung:
Runge-Kutta-Verfahren vierter Ordnung zur Lösung von gewöhnlichen DGL 1. Ordnung.
Ausgabe der Zeitentwicklung in Matrixform. 

Wichtig:
Die Dimension des Eingabeparameters x_0 muss mit dem verwendetem Modell überinstimmen.

Pythonversion:
3.5.1     
"""

import numpy as np



def RK4(f,theta,u,x_0,t0,T,dt):  
    #Input: Funktion, Parameterset, Stimulus, Anfangswert(array), Startpunkt, Endpunkt, Zeitschrittweite 
    t = np.arange(t0,T,dt)    # Zeitarray
 #   x = np.zeros((int(len(x_0)), int((T - t0) / dt + 1)))     #Größe der Endmatrix festlegen
    x = np.zeros((int(len(x_0)), len(t)))    
    x[:,0] = x_0                                    # Startbedingungen in erster Spalte
       
    for i in range(0,int(np.size(x,1))-1):
        k_1 = f(x,u,theta,i)              
        k_2 = f(x + 0.5*dt*k_1,u,theta,i)
        k_3 = f(x + 0.5*dt*k_2,u,theta,i)
        k_4 = f(x + dt*k_3,u,theta,i)
        
        x[:,i+1] = x[:,i] + (dt/6.)*(k_1.T + 2*k_2.T + 2*k_3.T + k_4.T)
    
    return x