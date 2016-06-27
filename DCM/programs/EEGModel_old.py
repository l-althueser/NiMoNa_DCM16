# -*- coding: utf-8 -*-
"""
@author: Tobias
         
Beschreibung:
Implementierung der DGL des EEG Modells nach "Dynamic causal models of steady-state responses",
 hier jedoch in der vereinfachten Version von "A neural mass model for MEG/EEG:
coupling and neuronal dynamics", Friston, 2003. 

Funktionsweise:
Die Zustandgleichungen werden mit dem RK4 oder Eulerverfahren gelöst. Um eine Simulation zu starten, müssen folgende 
Startparameter übergeben werden:
u: Anregungen/Stimulus
thetha: Laterale, Vorwarts und rueckwaerts Kopplung, sowie Stimulusauswirkungsmatrix
Die Parameter x und tstep werden aus dem Runge-Kutta-Verfahren übernommen.

Pythonversion:
3.5.1     
"""

import numpy as np

def stateEquations(x,u,theta,tstep):
    """
    Beschreibung:
    DGL zur Berechnung der Zetableitungen der Zustandsgrößen zu einem Zeitpunkt tstep. 
    Die Ausgabe ist ein Vektor.
    """    
    # Parameter des EEG Modells 
    AL = theta[0]
    AB = theta[1]
    AF = theta[2]
    C = theta[3]
    k_ex = 1./10.
    k_in = 0.05 
    H_ex = 3.25
    H_in = 22.
    gamma1,gamma2,gamma3,gamma4,gamma5=0,0,0,0,0
    N = np.size(x[:,0])/12           #Netzwerkgröße
    
    """
    x steht für ein Potential, v für den Strom, p kennzeichnet Pyramidalzellen, i inhibitorische Interneureonen, s spiny cells
    indizes ex bzw. in stehen für den exzitatorischen bzw. inhibitorischen Teil
    """
    
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

    #Die Teile die in der vereinfachten Version nicht benötigt werden, werden hier auf null gesetzt
    xp_in_dot,vp_in_dot,xp_ges_dot,vi_in_dot,xi_in_dot,xi_ges_dot=np.zeros(3),np.zeros(3),np.zeros(3),np.zeros(3),np.zeros(3),np.zeros(3)

        
    
    # Differentialgleichungen des Modells
    #DGL für Pyramidalneuronen
    xp_ex_dot = vp_ex[:,tstep]
    vp_ex_dot =k_ex*H_ex*sig2(xs[:,tstep]-xi_ex[:,tstep])-2.*k_ex*vp_ex[:,tstep]-k_ex**2.*xp_ex[:,tstep]
    
    #DGL für Spiny Neuronen
    xs_dot = vs[:,tstep]
    vs_dot = k_ex*H_ex*(sig2(xp_ex[:,tstep])+np.dot(C,u[:,tstep]))-2.*k_ex*vs[:,tstep]-k_ex**2.*xs[:,tstep]
    
         #DGL für inhibitorische Interneuronen
    xi_ex_dot = vi_ex[:,tstep]
    vi_ex_dot =k_in*H_in*sig2(xp_ex[:,tstep])-2.*k_in*vi_ex[:,tstep]-k_in**2.*xi_ex[:,tstep]
    
          
    # Zum Gesamtvektor zum Zeitpunkt tstep zusammenfügen  
    x_dot = np.hstack([[xp_ex_dot],[vp_ex_dot],[xp_in_dot],[vp_in_dot],[xp_ges_dot],[xs_dot],[vs_dot],[xi_ex_dot],[vi_ex_dot],[xi_in_dot],[vi_in_dot],[xi_ges_dot]]).T              
    
    return x_dot      



#Die in dem Paper "A neural mass model for MEG/EEG: coupling and neuronal dynamics" angegebene Sigmoidfunktion
def sig2(x): 
    r=0.56
    c1=135.
    v0=6.
    c2=0.8*135.
    e0=5.
    return (c1*e0/(1+np.exp(r*(v0-c2*x))))
#    
        


















