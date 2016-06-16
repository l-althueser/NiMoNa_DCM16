# -*- coding: utf-8 -*-

"""
@author: Timo

Beschreibung:
Simulation eines Netzwerkes bestehend aus 2 Regionen. 
Grafik folgt.

Pythonversion:
3.5.1     
"""

import numpy as np
import matplotlib.pyplot as plt

from programs import RK4 as RK4
#from programs import Euler as RK1
from programs import hemodynamicModel as HM
#from programs import bilinearModel as BM

#-----------------------------------------------------------------------------------------------------------------
# Parameter Beispiel 1
T = 90.                     # Endzeit
t0 = 0.                      # Anfangszeit
dt = 0.1                     # Zeitschrittlaenge         
t = np.arange(t0,T+dt,dt)    # Zeitarray
    
A = np.array([[-1.,0.],
			  [0.5,-1]]) # Kopplung 

B1 = np.zeros((2,2))         # Induzierte Kopplung durch Stimuli
B2 = np.array([[0  , 0],
			   [0.8 , 0]])
B = np.array([B1, B2])       # Zusammenfassen der ind. Kopplung in ein Array
          
C = np.array([[1, 0],
			  [0, 0]])       # äußerer Einfluss auf Hirnaktivität

D1 = np.zeros((3,3))         # Neuronal induzierte Kopplungsänderung
D2 = np.array([[0  , 0, 0  ],
			   [0  , 0, 0.8],
			   [0.1, 0, 0  ]])
D3 = np.zeros((3,3))
D = np.array([D1, D2])       # Zusammenfassen der neuronalen Kopplungsänderung in ein Array
          
# äußerer Stimulus
u = np.zeros((len(B), len(t)))             
u[0,101:-199:200] = 10.       # Stimulus u1   
#u[0,101:200] = 2.       # Stimulus u1

u[1,251:350] = 2.            # Stimulus u2 
u[1,451:550] = 5.            # Stimulus u2
u[1,700:705] = 5.            # Stimulus u2

# Anfangsbedingunden  
x_0 = np.ones(10)
x_0[0:4] = 0.

# Zusammenfassen der Parameter für das "hemodynamicModel"
theta = list([A,B,C,D])


#-----------------------------------------------------------------------------------------------------------------
# Simulation

# ------------- Bilinear 
#z_0 = np.array([0,0,0])
#z = RK4.RK4(BM.bilinearModel,theta,u,z_0,t0,T,dt)
x = RK4.RK4(HM.stateEquations,theta,u,x_0,t0,T,dt)      # Lösung mithilfe des RK4-Verfahrens
#x = RK1.Euler(HM.stateEquations,theta,u,x_0,t0,T,dt)   # Lösung mithilfe des expl. Euler-Verfahrens
y = HM.BOLDsignal(x)                                    # Berechnung des BOLD-Signals

# ------------- Linear 
# Änderung der Anfagsparameter B=0
Blin = np.array([np.zeros((2,2))])
thetalin = list([A,Blin,C])

#Simulation
xlin = RK4.RK4(HM.stateEquations,thetalin,u,x_0,t0,T,dt)      # Lösung mithilfe des RK4-Verfahrens
ylin = HM.BOLDsignal(xlin)                                    # Berechnung des BOLD-Signals


#-----------------------------------------------------------------------------------------------------------------
# Plotten 
plt.rcParams['figure.figsize'] = (15.0, 10.0) # Fenstergröße anpassen
plt.rcParams['axes.linewidth'] = 2

plt.cla() 
f1 =plt.figure(1)
#f1.suptitle('DCM - Simulation', fontsize = 20)
# Stimulus 
ax1 = plt.subplot(411)
ax1.tick_params(width = 2)
plt.xticks(np.arange(10,100,10))
plt.plot(t,u[0,:],'b',linewidth=2)
plt.setp(ax1.get_xticklabels(), visible=False)
plt.ylabel('$u_1(t)$', fontsize = 22.)
plt.title('Stimuli',fontsize = 20.)

ax2 = plt.subplot(412,sharex = ax1, sharey =ax1)
ax2.tick_params(width = 2)
plt.plot(t,u[1,:],'b', linewidth=2)
ax2.set_ylim([0,np.max(u)+1])
plt.setp(ax2.get_xticklabels(), visible=False)
plt.ylabel('$u_2(t)$', fontsize = 22.)

# Gehirnaktivität plotten
ax3 = plt.subplot(413,sharex = ax1)
plt.setp(ax3.get_xticklabels(), fontsize = 14., visible=False)
plt.ylabel('$v(t)$', fontsize = 22.)
ax3.tick_params(width = 1.5)
ax3.set_ylim([0,2])
plt.yticks(np.arange(0,2.5,0.5))

# Region 1:
plt.plot(t,x[0,:],'r',label='Region 1',linewidth=1.5)     #Gehirnaktivität
#plt.plot(t,x[2,:],'r',label='Region 1',linewidth=1.5)     #Vasodilatorisches Signal
#plt.plot(t,x[6,:],'r',label='Region 1',linewidth=1.5)     #Blutvolumen


# Region 2:
plt.plot(t,xlin[1,:],'k',label='Region 2 (lineares Modell)',linewidth=1.5)     #Gehirnaktivität im linearen Modell
plt.plot(t,x[1,:],'g',label='Region 2',linewidth=1.5)     #Gehirnaktivität
#plt.plot(t,x[3,:],'g',label='Region 2',linewidth=1.5)     #Vasodilatorisches Signal
#plt.plot(t,x[7,:],'g',label='Region 2',linewidth=1.5)    #Blutvolumen


plt.title('Gehirnaktivität',fontsize = 18.)

# Signal Plotten
ax4 = plt.subplot(414,sharex = ax1)
plt.setp(ax4.get_xticklabels(), fontsize = 14.)
ax4.tick_params(width = 1.5)
ax4.set_ylim([-0.04,0.06])
plt.yticks(np.arange(-0.04,0.08,0.02))

# Region 1:
plt.plot(t,y[0,:],'r',label='Region 1',linewidth=1.5)      #BOLD-Signal
#plt.plot(t,x[4,:],'r',label='Region 1',linewidth=1.5)     #Blutfluss 
plt.plot(t,x[8,:],'r',label='Region 1',linewidth=1.5)    #Deoxyhemoglobingehalt
# Region 2:
plt.plot(t,ylin[1,:],'k',label='Region 2 (lineares Modell)',linewidth=1.5)     #BOLD-Signal im linearen Modell
plt.plot(t,y[1,:],'g',label='Region 2 (bilineares Modell)',linewidth=1.5)      #BOLD-Signal
#plt.plot(t,x[5,:],'g',label='Region 2',linewidth=1.5)     #Blutfluss
#plt.plot(t,x[9,:],'g',label='Region 2',linewidth=1.5)    #Deoxyhemoglobingehalt

ax4.legend(loc='upper center', bbox_to_anchor=(0.5, -0.27),
          fancybox=True, shadow=True, ncol=5, fontsize=16)

plt.xlabel('Zeit t', fontsize = 18.)
plt.ylabel('$y(t)$', fontsize = 22.)
plt.title('BOLD-Signal',fontsize = 18.)

#f1.savefig('hemodynamicExample-2-volumen-deshb.eps')










