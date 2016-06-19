# -*- coding: utf-8 -*-
"""
@author: Tobias
         Timo
Beschreibung:
Implementierung der Funktionen die zur Simulation des hämodynamischen Modells benötigt werden. 

Funktionsweise:
Die Zustandgleichungen werden mit dem RK4 oder Eulerverfahren gelöst. Um eine Simulation zu starten, müssen folgende Startparameter übergeben werden:
u: Anregungen/Stimulus
thetha: [Eigenkopplung, Induzierte Kopplung(en), Äußerer Einfluss]
Die Parameter x und tstep werden aus dem Runge-Kutta-Verfahren übernommen.

Anmerkung:
Enthält bilineares Modell

Pythonversion:
3.5.1     
"""

import numpy as np

def stateEquations(x,u,theta,tstep):
    """
    Beschreibung:
    Funktion zur Berechnung der hämodynamischen Zustandsgleichungen zu einem Zeitpunkt tstep. 
    Die Ausgabe ist ein Vektor.
    Die Reihenfolge der Zustandsgleichungen, welche sich über die Zeilen erstrecken lautet:
    Gehinraktivität z
    Vasodilatorisches Signal s
    Blutfluss (inflow) f 
    Blutvolumen v
    Deoxyhemoglobingehalt q
    """    
    # Parameter des hemodynamischen Modells 
    AL = theta[0]
    AB = theta[1]
    AF = theta[2]
    C = theta[3]
    k_ex = 4
    k_in = 16 
    H_ex = 8
    H_in = 32
    gamma1 = 128
    gamma2 = 128
    gamma3 = 64
    gamma4 = 64 
    gamma5 = 5
    N = np.size(x[:,0])/12           #Netzwerkgröße
    

    # Die zeitabhängigen Variablen werden aus dem Gesamtvektor herausgeschnitten 
    xp_ex = np.vsplit(x,(0,N))[1]  
    vp_ex = np.vsplit(x,(N,2*N))[1]         
    xp_in = np.vsplit(x,(2*N,3*N))[1]
    vp_in = np.vsplit(x,(3*N,4*N))[1]       
    xp_ges = np.vsplit(x,(4*N,5*N))[1]
    
    xs = np.vsplit(x,(5*N,6*N))[1]
    vs = np.vsplit(x,(6*N,7*N))[1]
    
    xi_ex = np.vsplit(x,(7*N,8*N))[1]  
    vi_ex = np.vsplit(x,(8*N,9*N))[1]         
    xi_in = np.vsplit(x,(9*N,10*N))[1]
    vi_in = np.vsplit(x,(10*N,11*N))[1]       
    xi_ges = np.vsplit(x,(11*N,12*N))[1]

    

        
    
    # Differentialgleichungen des Modells
    #DGL für Pyramidalneuronen
    xp_ex_dot = vp_ex[:,tstep]
    vp_ex_dot = k_ex*H_ex*(np.dot((AB+AL),sig(xp_ges[:,tstep]))+gamma2*sig(xs[:,tstep]))-2*k_ex*vp_ex[:,tstep]-k_ex**2*xp_ex[:,tstep]
    xp_in_dot = vp_in[:,tstep]
    vp_in_dot = k_in*H_in*gamma4*sig(xi_ges[:,tstep])-2*k_in*vp_in[:,tstep]-k_in**2*xp_in[:,tstep]
    xp_ges_dot = xp_ex[:,tstep]-xp_in[:,tstep]
    
    #DGL für Siny Neuronen
    xs_dot = vs[:,tstep]
    vs_dot = k_ex*H_ex*(np.dot((AF+AL+gamma1*np.eye(3)),sig(xp_ges[:,tstep]))+np.dot(C,u[:,tstep]))-2*k_ex*vs[:,tstep]-k_ex**2*xs[:,tstep]
         
         #DGL für inhibitorische Interneuronen
    xi_ex_dot = vi_ex[:,tstep]
    vi_ex_dot = k_ex*H_ex*np.dot((AB+AL+gamma3*np.eye(3)),sig(xp_ges[:,tstep]))-2*k_ex*vi_ex[:,tstep]-k_ex**2*xi_ex[:,tstep]
    xi_in_dot = vi_in[:,tstep]
    vi_in_dot = k_in*H_in*gamma5*sig(xi_ges[:,tstep])-2*k_in*vi_in[:,tstep]-k_in**2*xi_in[:,tstep]
    xi_ges_dot = xi_ex[:,tstep]-xi_in[:,tstep]
    print(tstep,vp_ex_dot[0],vp_ex[0],(k_ex*H_ex*(np.dot((AB+AL),sig(xp_ges[:,tstep]))+gamma2*sig(xs[:,tstep])))[0],2*k_ex*vp_ex[0,tstep]-k_ex**2*xp_ex[0,tstep])
          
    # Zum Gesamtvektor zum Zeitpunkt tstep zusammenfügen  
    x_dot = np.hstack([[xp_ex_dot],[vp_ex_dot],[xp_in_dot],[vp_in_dot],[xp_ges_dot],[xs_dot],[vs_dot],[xi_ex_dot],[vi_ex_dot],[xi_in_dot],[vi_in_dot],[xi_ges_dot]]).T              
    
    return x_dot      





def sig(x): 
    r=0.56
    return (1/(1+np.exp(-r*x))-1/2.)


    
        


















