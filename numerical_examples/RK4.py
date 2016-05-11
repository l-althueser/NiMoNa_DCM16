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
import math
def RK4_method(f,A,B,const,z_0,dt,t0,T):  
    #Input: Funktion, Matrizen A,B und C*u, Anfangswert(array), Zeitschrittweite,Anfangszeit, Endzeit
   
    z=z_0
   
        
    for i in range(0,int(math.ceil((T-t0)/dt-1)),1):
        
        z_aktuell=np.hsplit(z,(i,i+1))[1] #Schneidet den aktuellen Output-Vektor aus der Matrix heraus
        
        
        k_1 = f(z_aktuell,A,B,const)                  #Mit dem aktuellen Outputvektor werden die k's ermittelt
        k_2 = f(z_aktuell+ 0.5*dt*k_1,A,B,const)
        k_3 = f(z_aktuell + 0.5*dt*k_2,A,B,const)
        k_4 = f(z_aktuell + dt*k_3,A,B,const)
        
        z=np.column_stack((z,np.hsplit(z,(i,i+1))[1] + (dt/6.)*(k_1 + 2*k_2 + 2*k_3 + k_4))) 
        #Hier wird die der neue Outputvektor aus den k's ermittelt und direkt an die bestehende Matrix angefuegt als neue spalte
    
        
    
    return z            
      
      


