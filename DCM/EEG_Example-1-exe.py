# -*- coding: utf-8 -*-

"""
@author: Tobias

Beschreibung:
Simulation eines Netzwerkes bestehend aus 3 Regionen nach dem 
EEG Modell nach "Dynamic causal models of steady-state responses", Friston 2009. 


Pythonversion:
3.5.1     
"""

import numpy as np
import matplotlib.pyplot as plt

from programs import RK4 as RK4
from programs import EEGModel as EEG

#-----------------------------------------------------------------------------------------------------------------
# Parameter Beispiel 1
T =200.                      # Endzeit
t0 = 0.                      # Anfangszeit
dt = 0.1                     # Zeitschrittlaenge         
t = np.arange(t0,T,dt)    # Zeitarray
AL = 4.*np.array([[0.,0.,0. ],
			  [0.,0.,0.],
			  [0.,0.,0.]]) # Laterale Kopplung 


         # Induzierte Kopplungänderung durch Stimuli
AB = 16.*np.array([[0.  , 0, 0  ],
			   [0  , 0., 0.],
			   [0., 0, 0.]])      # Backward connection

AF = 32.*np.array([[0.  , 0, 0  ],
			   [0.  , 0., 0.],
			   [0., 0, 0.  ]])   #Forward connection 
      
C = np.array([[1., 0],
			  [0, 0],
			  [0, 0]])       # Stimuluseinkopplung


# äußerer Stimulus
u = np.zeros((2, len(t)))             
u[0,0:2] = 2.      # Stimulus u1   

# Anfangsbedingunden
N=3             #Netzwerkanzahl
x_0=np.zeros(12*N)  #Varibalen pro Netzwerk: 5 (pyrmaidenneuronen)+ 5 (inhibitorische Interneuronen) + 2 (Spiny zellen)
#x_0[1]=1

# Zusammenfassen der Parameter für das "EEGModel"
theta = list([AL,AB,AF,C])

#-----------------------------------------------------------------------------------------------------------------
# Simulation
x = RK4.RK4(EEG.stateEquations,theta,u,x_0,t0,T,dt)      # Lösung mithilfe des RK4-Verfahrens

y = np.vsplit(x,(4*N,5*N))[1]               #EEG-Messstrom, xp_ges in unserer Notation (siehe EEGModel.py)


plt.rcParams['figure.figsize'] = (15.0, 10.0) # Fenstergröße anpassen

#-----------------------------------------------------
#def res(x):
#    k=4.
#    return 0.032*t*k*np.exp(-k*t)
#plt.figure(2)
##x=np.arange(-10,10)
#plt.plot(t,res(t))
#plt.show()
#------------------------------------------------------------
# Plotten EEG Modell

f1 = plt.figure(1) 
f1.suptitle('EEG Modell', fontsize = 20)
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
plt.plot(t,y[0,:],'r',label='Region 1')   
# Region 2:
plt.plot(t,y[1,:],'g',label='Region 2')      
#Region 3:
plt.plot(t,y[2,:],'b',label='Region 3')      

ax3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2),
          fancybox=True, shadow=True, ncol=5)

plt.xlabel('Zeit t', fontsize = 14.)
plt.ylabel('$y(t)$', fontsize = 16.)
plt.title('Messsignal nach Region')

f1.savefig('EEGExample-1-Messstrom.pdf')







