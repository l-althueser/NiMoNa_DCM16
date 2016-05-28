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
    kappa = 0.65         
    gamma = 0.41
    tau = 0.98
    alpha = 0.32
    rho = 0.34    
    N = np.size(theta[0],0)           #Netzwerkgröße
    
    # Berechnung von sum u_j*B_j    
    D = 0                         
    for i in range(len(theta[1])):
        D = D + np.dot(theta[1][i],u[i,tstep])                 
    
        
    # Die zeitabhängigen Variablen werden aus dem Gesamtvektor herausgeschnitten 
    z = np.vsplit(x,(0,N))[1]         
    s = np.vsplit(x,(N,2*N))[1]
    f = np.vsplit(x,(2*N,3*N))[1]
    v = np.vsplit(x,(3*N,4*N))[1]
    q = np.vsplit(x,(4*N,5*N))[1]
    
    # Differentialgleichungen des Modells
    z_dot = np.dot((theta[0] + D),z[:,tstep]) + np.dot(theta[2],u[:,tstep])      
    s_dot = z[:,tstep] - kappa * s[:,tstep] - gamma * ( f[:,tstep] - 1 )
    f_dot = s[:,tstep]
    v_dot = 1/tau * ( f[:,tstep] - v[:,tstep]**(1/alpha) )
    q_dot = 1/tau * ( f[:,tstep] * (1-(1-rho)**(1/f[:,tstep])) / rho - v[:,tstep]**(1/alpha) * q[:,tstep]/v[:,tstep])
    
    # Zum Gesamtvektor zum Zeitpunkt tstep zusammenfügen  
    x_dot = np.hstack([[z_dot],[s_dot],[f_dot],[v_dot],[q_dot]]).T               
    
    return x_dot      





def BOLDsignal(x): 
    """
    Beschreibung:
    Funktion zur Berechnung des BOLD Signals aus dem zeitabhängigen Blutvolumen und des Deoxyhomoglobingehalts des Blutes. 
    Der Eingabeparamter x muss mit den Funktionen stateEquations und RK4/Euler gelöst werden. 
    Ausgeben wird eine N-zeilige Matrix (N: Netzwerkgröße). Über die Zeilen sind die verschiedene Bereiche abgetragen,
    wohingegen sich die zeitliche Entwicklung über die Spalten erstreckt.
    """            
    # Parameter des Modells
    rho = 0.34    
    V0 = 0.02
    k1 = 7*rho
    k2 = 2
    k3 = 2*rho-0.2 
    
    #Netzwerkgröße ; Faktor 5 aufgrund der 5 gekoppelten DGL des hämodynamischen Systems
    N = int(np.size(x,0) / 5. )         
    
    # Abhängige Variablen (Blutvolumen v und Deoxyhemoglobingehalt q) aus der Gesamtmatrix herausschneiden
    v=np.vsplit(x,(3*N,4*N))[1]
    q=np.vsplit(x,(4*N,5*N))[1]
    
    # Berechnung des Signals
    signal = V0 * (k1 * (1-q) + k2 * (1-q/v) + k3 * (1-v))
    
    return signal


    
        


















