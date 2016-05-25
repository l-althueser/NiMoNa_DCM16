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
# changes/notes  :20160523 : Schrittweite gegen Intervallzahl
#==============================================================================

import numpy as np



def RK4_method(f,teta,x_0,dt,n):  
    #Input: Funktion, Parameterset, Anfangswert(array), Zeitschrittweite, Zeitschrittanzahl
   
    x=x_0
 
        
    for i in range(0,n,1):
        
        x_aktuell = x #Hier tritt ein Fehler auf, weil wir es veraendert haben - Schneidet den aktuellen Output-Vektor aus der x Matrix heraus
        
        
        k_1 = f(x_aktuell,teta)                  #Mit dem aktuellen Outputvektor werden die k's ermittelt
        k_2 = f(x_aktuell+ 0.5*dt*k_1,teta)
        k_3 = f(x_aktuell + 0.5*dt*k_2,teta)
        k_4 = f(x_aktuell + dt*k_3,teta)
        
        x=x + (dt/6.)*(k_1 + 2*k_2 + 2*k_3 + k_4)
        
        x[:,i+1]=x          #Hier tritt ein Fehler auf, weil wir es veraendert haben - Fuegt den neuen Vetor x der x Matrix zu
        
        #np.column_stack((x,np.hsplit(x,(i,i+1))[1] + (dt/6.)*(k_1 + 2*k_2 + 2*k_3 + k_4))) 
        #Hier wird die der neue Outputvektor aus den k's ermittelt und direkt an die bestehende Matrix angefuegt als neue spalte
        
        #ggf hier zur alten Version uebergehen
    
        
    
    return x            
      
      


