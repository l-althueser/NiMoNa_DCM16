#!/usr/bin/env python

#==============================================================================
#	RK4.py
#------------------------------------------------------------------------------
# description    :Implementation eines Runge-Kutta-Verfahrens 4. Ordnung (4O).
# author         :t-froh01, l-althueser
#
# usage          :
# python_version :3.5.1
#
# changes/notes  :20160425 :
#==============================================================================

import numpy as np

def RK4_method(f,theta,u,z,dt,m):  
    #Input: Funktion, Parameterset, Anregungsmatrix, Outputmatrix (noch fast ungefuellt), Zeitschrittlaenge, Zeitintervallanzahl
   
    for i in range(0,m,1):
        
        z_aktuell=z[:,i] #Schneidet den aktuellen Output-Vektor aus der Matrix heraus
        u_aktuell=u[:,i]
       # print(z_aktuell)
        
        k_1 = f(z_aktuell, theta, u_aktuell)              #Mit dem aktuellen Outputvektor werden die k's ermittelt
        k_2 = f(z_aktuell + 0.5*dt*k_1, theta, u_aktuell)
        k_3 = f(z_aktuell + 0.5*dt*k_2, theta, u_aktuell)
        k_4 = f(z_aktuell + dt*k_3, theta, u_aktuell)
        
        z[:,i+1] = z[:,i] + (dt/6.)*(k_1 + 2*k_2 + 2*k_3 + k_4)
        
        #Hier wird die der neue Outputvektor aus den k's ermittelt und direkt an die bestehende Matrix angefuegt als neue spalte
    
    return z            