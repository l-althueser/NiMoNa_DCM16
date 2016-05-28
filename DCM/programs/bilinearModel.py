# -*- coding: utf-8 -*-
"""
@author: Tobias
         Timo
Beschreibung:
Implementierung des bilinearen Modells zur Simulation der Hirnaktivität als Reaktion
auf einen äußeren Stimulus 

Funktionsweise:
Die Zustandgleichungen werden mit dem RK4 oder Eulerverfahren gelöst. Um eine Simulation zu starten, müssen folgende Startparameter übergeben werden:
u: Anregungen/Stimulus
thetha: [Eigenkopplung, Induzierte Kopplung(en), Äußerer Einfluss]
Die Parameter x und tstep werden aus dem Runge-Kutta-Verfahren übernommen.

Pythonversion:
3.5.1     
"""
import numpy as np

def bilinearModel(z, u, theta, tstep):       
    #Berechnung der Zeitableitung von z
    D = 0
    for i in range(len(theta[1])):           # Berechnung von sum u_j*B_j
        D = D + np.dot(theta[1][i], u[i,tstep])
    
    
    z_dot = np.dot((theta[0] + D),z[:,tstep]) + np.dot(theta[2],u[:,tstep])
    return np.array([z_dot]).T    
    

