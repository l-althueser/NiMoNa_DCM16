#!/usr/bin/env python

#==============================================================================
#	RK4.py
#------------------------------------------------------------------------------
# description    :Implementation eines Runge-Kutta-Verfahrens 4. Ordnung (4O).
# author         :t-froh01
#
# usage          :
# python_version :3.5.1
#
# changes/notes  :20160425 :
#==============================================================================

import numpy as np
def RK4_method(f,z_0,dt,t0,T):  
    #Input: Funktion, Anfangswert(arrany), Zeitschrittweite, Endzeit
   
    z=z_0
    #print(z[1,0])
    #Lege Liste an, entspricht nachher Trajektorie
   # t=np.arange(0,T,dt)
   
        
    for i in range(0,int((T-t0)/dt-1),1):
        # define all k
        z_aktuell=np.hsplit(z,(i,i+1))[1] #Schneidet den aktuellen Output-Vektor aus der Matrix heraus
        
        
        k_1 = f(z_aktuell)                  #Mit dem aktuellen Outputvektor werden die k's ermittelt
        k_2 = f(z_aktuell+ 0.5*dt*k_1)
        k_3 = f(z_aktuell + 0.5*dt*k_2)
        k_4 = f(z_aktuell + dt*k_3)
        
        z=np.column_stack((z,np.hsplit(z,(i,i+1))[1] + (dt/6.)*(k_1 + 2*k_2 + 2*k_3 + k_4))) 
        #Hier wird die der neue Outputvektor aus den k's ermittelt und direkt an die bestehende Matrix angefuegt als neue spalte
    
        
    
    return z            
      
      


