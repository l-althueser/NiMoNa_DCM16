"""
@author: Timo

Beschreibung:
Simulation eines Netzwerkes bestehend aus 4 Regionen. 
Grafik folgt.
samt nicht-linearer Erweiterung

Beachte: u_2 hat via dem Bilinearen Term keinen Einfluss

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
t = np.arange(t0,T,dt)    # Zeitarray
    
A = np.array([[-1.0, 0.0, 0.0, 0.0],
              [ 0.4,-1.0, 0.0, 0.0],
              [ 0.0, 0.3,-1.0, 0.0],
              [ 0.5, 0.0, 0.0,-1.0]]) # Kopplung 

B1 = np.zeros((4,4))         # Induzierte Kopplungänderung durch Stimuli
B2 = np.array([[0.0, 0.0, 0.0, 0.0],
               [0.0, 0.0, 0.0, 0.0],
               [0.0, 0.0, 0.0, 0.0],
			[0.0, 0.0, 0.0, 0.0]])
B = np.array([B1, B2])       # Zusammenfassen der ind. Kopplung in ein Array
          
C = np.array([[0.5, 0.0],
              [0.0, 0.0],
              [0.0, 0.0],
        	    [0.0, 0.0]])       # äußerer Einfluss auf Hirnaktivität

D2 = np.zeros((4,4))         # Neuronal induzierte Kopplungsänderung
D3 = np.array([[ 0.0, 0.0, 0.0, 0.0],
               [-0.5, 0.0, 0.0, 0.0],
               [ 0.0, 0.0, 0.0, 0.0],
			[ 0.0, 0.0, 0.0, 0.0]])
D1 = np.zeros((4,4))
D4 = np.zeros((4,4))
D = np.array([D1, D2, D3, D4])       # Zusammenfassen der neuronalen Kopplungsänderung in ein Array
          
# äußerer Stimulus
u = np.zeros((len(B), len(t)))             
u[1,101:-99:200] = 10.       # Stimulus u1 
 
u[0,250:350] = 5.            # Stimulus u2
u[0,451:550] = 3.            # Stimulus u2
u[0,691:910] = 3.            # Stimulus u2

# Anfangsbedingunden  
x_0 = np.ones(20)
x_0[0:8] = 0.

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
f1.suptitle('Nichtlineares Modell', fontsize = 20)
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
#Region 4:
plt.plot(t,y[3,:],'c',label='Region 4')      #BOLD-Signal

ax3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2),
          fancybox=True, shadow=True, ncol=5)

plt.xlabel('Zeit t', fontsize = 14.)
plt.ylabel('$y(t)$', fontsize = 16.)
plt.title('BOLD-Signal nach Region')


f1.savefig('hemodynamicExample-4R-BOLD.eps')

#-------------------------- Gehirnaktivität ------------------------------------
f2 = plt.figure(2)
f2.suptitle('Nichtlineares Modell', fontsize = 20)
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
#plt.plot(t,x[4,:],'r',label='Region 1')     #Vasodilatorisches Signal
#plt.plot(t,x[8,:],'r',label='Region 1')     #Blutfluss 
#plt.plot(t,x[12,:],'r',label='Region 1')     #Blutvolumen
#plt.plot(t,x[16,:],'r',label='Region 1')    #Deoxyhemoglobingehalt

# Region 2:
plt.plot(t,x[1,:],'g',label='Region 2')     #Gehirnaktivität
#plt.plot(t,x[5,:],'g',label='Region 2')     #Vasodilatorisches Signal
#plt.plot(t,x[9,:],'g',label='Region 2')     #Blutfluss
#plt.plot(t,x[13,:],'g',label='Region 2')    #Blutvolumen
#plt.plot(t,x[17,:],'g',label='Region 2')    #Deoxyhemoglobingehalt

# Region 3:
plt.plot(t,x[2,:],'b',label='Region 3')     #Gehirnaktivität
#plt.plot(t,x[6,:],'b',label='Region 3')     #Vasodilatorisches Signal
#plt.plot(t,x[10,:],'b',label='Region 3')     #Blutfluss 
#plt.plot(t,x[14,:],'b',label='Region 3')    #Blutvolumen
#plt.plot(t,x[18,:],'b',label='Region 3')    #Deoxyhemoglobingehalt

# Region 4:
plt.plot(t,x[3,:],'c',label='Region 4')     #Gehirnaktivität
#plt.plot(t,x[7,:],'c',label='Region 4')     #Vasodilatorisches Signal
#plt.plot(t,x[11,:],'c',label='Region 4')     #Blutfluss 
#plt.plot(t,x[15,:],'c',label='Region 4')    #Blutvolumen
#plt.plot(t,x[19,:],'c',label='Region 4')    #Deoxyhemoglobingehalt

ax6.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2),
          fancybox=True, shadow=True, ncol=5)
plt.xlabel('Zeit t', fontsize = 14.)
plt.ylabel('$z(t)$', fontsize = 16.)
plt.title('Gehirnaktivitaet nach Region')
#plt.show()

f2.savefig('hemodynamicExample-4R-Aktivitaet.eps')










