"""
@author: Timo

Beschreibung:
Simulation eines Netzwerkes bestehend aus 3 Regionen. 
Grafik folgt.

Pythonversion:
3.5.1     
"""


import numpy as np
import matplotlib.pyplot as plt

from programs import RK4 as RK4
from programs import Euler as RK1
from programs import hemodynamicModel as HM
from programs import bilinearModel as BM



#-----------------------------------------------------------------------------------------------------------------
# Parameter Beispiel 1
T = 20.                         # Endzeit
t0 = 0.                         # Anfangszeit
dt = 0.1                        # Zeitschrittlaenge         
t = np.arange(t0,T+dt,dt)       # Zeitarray

    
A = np.array([[-1.,0.,0.],[0.3,-1,0.2],[0.6,0.,-1.]])        # Kopplung 


B1 = np.zeros((3,3))                                        #Induzierte Kopplung
B2 = np.array([[0, 0, 0],[0, 0, 0.8],[0.1, 0, 0]])
B = np.array([B1, B2])                                      #Zusammenfassen der ind. Kopplung in ein Array
          
C = np.array([[1, 0],[0, 0],[0, 0]])                        # äußerer Einfluss auf Hirnaktivität

# äußerer Stimulus
u = np.zeros((len(B), len(t)))             
u[:,51] = 1.

# Anfangsbedingunden  
x_0 = np.ones(15)
x_0[0:6] = 0.

# Zusammenfassen der Parameter für das "hemodynamicModel"
theta = np.array([A,B,C])

#-----------------------------------------------------------------------------------------------------------------
# Simulation 
#z_0 = np.array([0,0,0])
#z = RK4.RK4(BM.bilinearModel,theta,u,z_0,t0,T,dt)

x = RK4.RK4(HM.stateEquations,theta,u,x_0,t0,T,dt)      # Lösung mithilfe des RK4-Verfahrens
#x = RK1.Euler(HM.stateEquations,theta,u,x_0,t0,T,dt)   # Lösung mithilfe des expl. Euler-Verfahrens

y = HM.BOLDsignal(x)                                    # Berechnung des BOLD-Signals

plt.figure()

# Region 1:
#plt.plot(t,x[0,:],'r',label='Region 1')     #Gehirnaktivität
#plt.plot(t,x[3,:],'r',label='Region 1')     #Vasodilatorisches Signal
#plt.plot(t,x[6,:],'r',label='Region 1')     #Blutfluss 
#plt.plot(t,x[9,:],'r',label='Region 1')     #Blutvolumen
#plt.plot(t,x[12,:],'r',label='Region 1')    #Deoxyhemoglobingehalt
plt.plot(t,y[0,:],'r',label='Region 1')      #BOLD-Signal

# Region 2:
#plt.plot(t,x[1,:],'g',label='Region 2')     #Gehirnaktivität
#plt.plot(t,x[4,:],'g',label='Region 2')     #Vasodilatorisches Signal
#plt.plot(t,x[7,:],'g',label='Region 2')     #Blutfluss
#plt.plot(t,x[10,:],'g',label='Region 2')    #Blutvolumen
#plt.plot(t,x[13,:],'g',label='Region 2')    #Deoxyhemoglobingehalt
plt.plot(t,y[1,:],'g',label='Region 2')      #BOLD-Signal

#R egion 3:
#plt.plot(t,x[2,:],'b',label='Region 3')     #Gehirnaktivität
#plt.plot(t,x[5,:],'b',label='Region 3')     #Vasodilatorisches Signal
#plt.plot(t,x[8,:],'b',label='Region 3')     #Blutfluss 
#plt.plot(t,x[11,:],'b',label='Region 3')    #Blutvolumen
#plt.plot(t,x[14,:],'b',label='Region 3')    #Deoxyhemoglobingehalt
plt.plot(t,y[2,:],'b',label='Region 3')      #BOLD-Signal

plt.title('BOLD-Signal nach Region')
plt.legend()
plt.xlabel('Zeit t')
plt.show

