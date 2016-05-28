"""
@author: Lutz
         Timo
         
Beschreibung:
Explizites Eulerverfahrung zur Lösung von gewöhnlichen DGL 1. Ordnung.
Ausgabe der Zeitentwicklung in Matrixform. 

Wichtig:
Die Dimension des Eingabeparameters x_0 muss mit dem verwendetem Modell überinstimmen.


Pythonversion:
3.5.1     
"""
import numpy as np

def Euler(f,theta,u,x_0,t0,T,dt):
    #Input: Funktion, Parameterset, Stimulus, Anfangswert(array), Startpunkt, Endpunkt, Zeitschrittweite 
    
    x = np.zeros((int(len(x_0)), int((T - t0) / dt + 1)))     #Größe der Endmatrix festlegen
    x[:,0] = x_0                                    # Startbedingungen in erster Spalte
	
    for i in range(0,int(np.size(x,1))-1):
        k = f(x,u,theta,i)
        
        x[:,i+1] = x[:,i] + dt * k.T
    
    return x
 