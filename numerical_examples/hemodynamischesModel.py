# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 17:49:20 2016

@author: Tobias

Testcode, um die Funktionalität des RK4-Verfahrens zu überprüfen
"""

import numpy as np
import RK4 as RK
import matplotlib.pyplot as plt

#Eingabe systemabhängiger Parameter
x_0=np.array([[1],[2],[3],[4],[5],[6],[1],[2],[3],[4],[5],[6],[0],[0],[0]])    
#Anfangswertvektor (enthält Aktivität und alle hemodynamische Größen hintereinander, Reihenfolge: z, s, f, v, q),
#bereits in gewünschter Matrixschreibweise

T=2.1    #Endzeit
t0=2    #Anfangszeit
dt=0.1              #Zeitschrittlaenge
t = np.arange(t0,T,dt)      #Zeitarray


A=np.matrix("-0.4, 0, 0; 0, 0.1, 0; 0, 0, -0.3")    #Matrix A
D=np.array([np.matrix("-0.4, 0, 0; 0, 0.1, 0; 0, 0, -0.3"),
            np.matrix("-0.4, 0, 0; 0, 0.1, 0; 0, 0, -0.3"),
            np.matrix("-0.4, 0, 0; 0, 0.1, 0; 0, 0, -0.3")])    #Array D hat als Einträge Matrizen B1,B2,...
            
C=np.matrix("-0.4, 0.1, 0; 0, 0.1, 0; 0, 0, -0.3")    #Matrix C
u=np.array([[1],[1],[2]])      #Anregung u
kappa=1         #Hemodynamischen Parameter
gamma=1
tau=1
alpha=1
rho=1
V0=0.02
k=([7*rho,2,2*rho-0.2])
N=3         #Netzwerkgroesse


#---------------------------------------------------------------------------------------------------------------------

const=C*u #C*u ist immer konstant, kann deshalb einfach uebergeben werden
            
for i in range(len(D)):
    B=+D[i]*u[i]
    
teta=list((A,B,const,kappa,gamma,tau,alpha,rho,N))    #Parameterset fuer DGLs
teta_out=list((N,V0,k))                             #Parameterset fuer output y

    

def f(x,teta):       #Gibt die Zeitableitung x_dot wider
    N=teta[8]                             #Groesse unseres Netzwerkes
    
    z=np.vsplit(x,(0,N))[1]         #Die zeitabhängigen Variablen werden aus dem Gesamtvektor herausgeschnitten
    s=np.vsplit(x,(N,2*N))[1]
    f=np.vsplit(x,(2*N,3*N))[1]
    v=np.vsplit(x,(3*N,4*N))[1]
    q=np.vsplit(x,(4*N,5*N))[1]
    
    z_dot=np.squeeze(np.asarray((teta[0]+teta[1])*z+teta[2])).reshape(3,1)      #Die einzelnen Differentialgleichungen
    s_dot=z-teta[3]*s-teta[4]*(f-1)
    f_dot=s
    v_dot=1/teta[5]*(f-v**(1/teta[6]))
    q_dot=1/teta[5]*(f*(1-(1-teta[7])**(1/f))/teta[7]-v**(1/teta[6])*q/v)
    
    x_dot=np.vstack((z_dot,s_dot,f_dot,v_dot,q_dot))               #Alles wird wieder zum Gesamtvektor hinzugefügt
    #print(x_dot)
    return x_dot      

def output(x,teta_out):             #Hier wird der experimentell relevante Output y berechnet
    
    v=np.vsplit(x,(3*N,4*N))[1]
    q=np.vsplit(x,(4*N,5*N))[1]
    
    return teta_out[1]*(teta_out[2][0]*(1-q)+teta_out[2][1]*(1-q/v)+teta_out[2][2]*(1-v))
    
        


x=RK.RK4_method(f,teta,x_0,dt,t0,T)
y=output(x,teta_out)

#print(x,y)

plt.figure()
for i in range(N):
    plt.plot(t,np.squeeze(np.asarray(y[i,:])))      #Jede Zeile des experimentellen Outputvektors wird gegen die Zeit geplottet

plt.savefig("test")

