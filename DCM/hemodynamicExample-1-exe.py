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
#from programs import Euler as RK1
from programs import hemodynamicModel as HM
#from programs import bilinearModel as BM

#-----------------------------------------------------------------------------------------------------------------
# Parameter Beispiel 1
T = 100.                     # Endzeit
t0 = 0.                      # Anfangszeit
dt = 0.1                     # Zeitschrittlaenge         
t = np.arange(t0,T+dt,dt)    # Zeitarray
    
A = np.array([[-1.,0.,0. ],
			  [0.3,-1,0.2],
			  [0.6,0.,-1.]]) # Kopplung 

B1 = np.zeros((3,3))         # Induzierte Kopplungänderung durch Stimuli
B2 = np.array([[0  , 0, 0  ],
			   [0  , 0, 0.8],
			   [0.1, 0, 0  ]])
B = np.array([B1, B2])       # Zusammenfassen der ind. Kopplung in ein Array
          
C = np.array([[1, 0],
			  [0, 0],
			  [0, 0]])       # äußerer Einfluss auf Hirnaktivität

D1 = np.zeros((3,3))         # Neuronal induzierte Kopplungsänderung
D2 = np.array([[0  , 0, 0  ],
			   [0  , 0, 0.8],
			   [0.1, 0, 0  ]])
D3 = np.zeros((3,3))
D = np.array([D1, D2])       # Zusammenfassen der neuronalen Kopplungsänderung in ein Array
          
# äußerer Stimulus
u = np.zeros((len(B), len(t)))             
u[0,101:-99:200] = 10.       # Stimulus u1   

u[1,451:550] = 2.            # Stimulus u2 
u[1,251:350] = 5.            # Stimulus u2
u[1, 691:910] = 2.           # Stimulus u2

# Anfangsbedingunden  
x_0 = np.ones(15)
x_0[0:6] = 0.

# Zusammenfassen der Parameter für das "hemodynamicModel"
theta = list([A,B,C,D])

#-----------------------------------------------------------------------------------------------------------------
# Simulation 
#z_0 = np.array([0,0,0])
#z = RK4.RK4(BM.bilinearModel,theta,u,z_0,t0,T,dt)
x = RK4.RK4(HM.stateEquations,theta,u,x_0,t0,T,dt)      # Lösung mithilfe des RK4-Verfahrens
#x = RK1.Euler(HM.stateEquations,theta,u,x_0,t0,T,dt)   # Lösung mithilfe des expl. Euler-Verfahrens
y = HM.BOLDsignal(x)                                    # Berechnung des BOLD-Signals

plt.rcParams['figure.figsize'] = (15.0, 10.0) # Fenstergröße anpassen

#-----------------------------------------------------------------------------------------------------------------
# Plotten Bilineares Modell
#-------------------------- BOLD ------------------------------------
f1 = plt.figure(1) 
f1.suptitle('Bilineares Modell', fontsize = 20)
# Stimulus 
ax1 = plt.subplot(311)
ax1.tick_params(width = 1)
plt.plot(t,u[0,:])
plt.setp(ax1.get_xticklabels(), visible=False)
plt.ylabel('$u_1(t)$', fontsize = 16.)
plt.title('Stimuli')

ax2 = plt.subplot(312,sharex = ax1, sharey =ax1)
ax2.tick_params(width = 1)
plt.plot(t,u[1,:])
ax2.set_ylim([0,np.max(u)+1])
plt.setp(ax2.get_xticklabels(), visible=False)
plt.ylabel('$u_2(t)$', fontsize = 16.)

# Signal Plotten
ax3 = plt.subplot(313,sharex = ax1)
plt.setp(ax3.get_xticklabels(), fontsize = 14.)
plt.xticks(np.arange(10,110,10))
ax3.tick_params(width = 1)

# Region 1:
plt.plot(t,y[0,:],'r',label='Region 1')      #BOLD-Signal
# Region 2:
plt.plot(t,y[1,:],'g',label='Region 2')      #BOLD-Signal
#Region 3:
plt.plot(t,y[2,:],'b',label='Region 3')      #BOLD-Signal

ax3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2),
          fancybox=True, shadow=True, ncol=5)

plt.xlabel('Zeit t', fontsize = 14.)
plt.ylabel('$y(t)$', fontsize = 16.)
plt.title('BOLD-Signal nach Region')

f1.savefig('hemodynamicExample-1_bilinear_BOLD.eps')

#-------------------------- Gehirnaktivität ------------------------------------
f2 = plt.figure(2)
f2.suptitle('Bilineares Modell', fontsize = 20)
# Stimulus plotten
ax4 = plt.subplot(311)
ax4.tick_params(width = 1)
plt.plot(t,u[0,:])
plt.setp(ax4.get_xticklabels(), visible=False)
plt.ylabel('$u_1(t)$', fontsize = 16.)
plt.title('Stimuli')

ax5 = plt.subplot(312,sharex = ax4, sharey =ax4)
ax5.tick_params(width = 1)
plt.plot(t,u[1,:])
ax5.set_ylim([0,np.max(u)+1])
plt.setp(ax5.get_xticklabels(), visible=False)
plt.ylabel('$u_2(t)$', fontsize = 16.)

# Gehirnaktivität plotten
ax6 = plt.subplot(313,sharex = ax4)
plt.setp(ax6.get_xticklabels(), fontsize = 14.)
plt.xticks(np.arange(10,110,10))
ax6.tick_params(width = 1)

# Region 1:
plt.plot(t,x[0,:],'r',label='Region 1')     #Gehirnaktivität
#plt.plot(t,x[3,:],'r',label='Region 1')     #Vasodilatorisches Signal
#plt.plot(t,x[6,:],'r',label='Region 1')     #Blutfluss 
#plt.plot(t,x[9,:],'r',label='Region 1')     #Blutvolumen
#plt.plot(t,x[12,:],'r',label='Region 1')    #Deoxyhemoglobingehalt

# Region 2:
plt.plot(t,x[1,:],'g',label='Region 2')     #Gehirnaktivität
#plt.plot(t,x[4,:],'g',label='Region 2')     #Vasodilatorisches Signal
#plt.plot(t,x[7,:],'g',label='Region 2')     #Blutfluss
#plt.plot(t,x[10,:],'g',label='Region 2')    #Blutvolumen
#plt.plot(t,x[13,:],'g',label='Region 2')    #Deoxyhemoglobingehalt

# Region 3:
plt.plot(t,x[2,:],'b',label='Region 3')     #Gehirnaktivität
#plt.plot(t,x[5,:],'b',label='Region 3')     #Vasodilatorisches Signal
#plt.plot(t,x[8,:],'b',label='Region 3')     #Blutfluss 
#plt.plot(t,x[11,:],'b',label='Region 3')    #Blutvolumen
#plt.plot(t,x[14,:],'b',label='Region 3')    #Deoxyhemoglobingehalt

ax6.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2),
          fancybox=True, shadow=True, ncol=5)
plt.xlabel('Zeit t', fontsize = 14.)
plt.ylabel('$z(t)$', fontsize = 16.)
plt.title('Gehirnaktivitaet nach Region')
#plt.show()

f2.savefig('hemodynamicExample-1_bilinear_Aktivitaet.eps')

#--------------------------------------------------------------------- Lineares Modell zum Vergleich -----------------------------------------------
# Änderung der Anfagsparameter B=0 und D=0
Blin = np.array([np.zeros((3,3))])
Dlin = np.array([np.zeros((3,3))])
thetalin = list([A,Blin,C,Dlin])

#Simulation
xlin = RK4.RK4(HM.stateEquations,thetalin,u,x_0,t0,T,dt)      # Lösung mithilfe des RK4-Verfahrens
ylin = HM.BOLDsignal(xlin)                                    # Berechnung des BOLD-Signals

# Plotten
#-------------------------- BOLD ------------------------------------
f3 = plt.figure(3) 
f3.suptitle('Lineares Modell', fontsize = 20)
# Stimulus 
ax1lin = plt.subplot(311)
ax1lin.tick_params(width = 1)
plt.plot(t,u[0,:])
plt.setp(ax1lin.get_xticklabels(), visible=False)
plt.ylabel('$u_1(t)$', fontsize = 16.)
plt.title('Stimuli')

ax2lin = plt.subplot(312,sharex = ax1lin, sharey =ax1lin)
ax2lin.tick_params(width = 1)
plt.plot(t,u[1,:])
ax2lin.set_ylim([0,np.max(u)+1])
plt.setp(ax2lin.get_xticklabels(), visible=False)
plt.ylabel('$u_2(t)$', fontsize = 16.)

# Signal Plotten
ax3lin = plt.subplot(313,sharex = ax1lin)
plt.setp(ax3lin.get_xticklabels(), fontsize = 14.)
plt.xticks(np.arange(10,110,10))
ax3lin.tick_params(width = 1)

# Region 1:
plt.plot(t,ylin[0,:],'r',label='Region 1')      #BOLD-Signal
# Region 2:
plt.plot(t,ylin[1,:],'g',label='Region 2')      #BOLD-Signal
#Region 3:
plt.plot(t,ylin[2,:],'b',label='Region 3')      #BOLD-Signal

ax3lin.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2),
          fancybox=True, shadow=True, ncol=5)
plt.xlabel('Zeit t', fontsize = 14.)
plt.ylabel('$y(t)$', fontsize = 16.)
plt.title('BOLD-Signal nach Region')

f3.savefig('hemodynamicExample-1_linear_BOLD.eps')

#-------------------------- Gehirnaktivität ------------------------------------
f4 = plt.figure(4)
f4.suptitle('Lineares Modell', fontsize = 20)
# Stimulus plotten
ax4lin = plt.subplot(311)
ax4lin.tick_params(width = 1)
plt.plot(t,u[0,:])
plt.setp(ax4lin.get_xticklabels(), visible=False)
plt.ylabel('$u_1(t)$', fontsize = 16.)
plt.title('Stimuli')

ax5lin = plt.subplot(312,sharex = ax4lin, sharey =ax4lin)
ax5lin.tick_params(width = 1)
plt.plot(t,u[1,:])
ax5lin.set_ylim([0,np.max(u)+1])
plt.setp(ax5lin.get_xticklabels(), visible=False)
plt.ylabel('$u_2(t)$', fontsize = 16.)

# Gehirnaktivität plotten
ax6lin = plt.subplot(313,sharex = ax4lin)
plt.setp(ax6lin.get_xticklabels(), fontsize = 14.)
plt.xticks(np.arange(10,110,10))
ax6lin.tick_params(width = 1)

# Region 1:
plt.plot(t,xlin[0,:],'r',label='Region 1')     #Gehirnaktivität
# Region 2:
plt.plot(t,xlin[1,:],'g',label='Region 2')     #Gehirnaktivität
# Region 3:
plt.plot(t,xlin[2,:],'b',label='Region 3')     #Gehirnaktivität

ax6lin.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2),
          fancybox=True, shadow=True, ncol=5)
plt.xlabel('Zeit t', fontsize = 14.)
plt.ylabel('$z(t)$', fontsize = 16.)
plt.title('Gehirnaktivitaet nach Region')

f4.savefig('hemodynamicExample-1_linear_Aktivitaet.eps')

plt.show()









