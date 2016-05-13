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

T=10.    #Endzeit
t0=2.    #Anfangszeit
m=100     #Anzahl der Zeitintervalle
dt=(T-t0)/m     #Zeitschrittlaenge
           
t = np.arange(t0,T+dt,dt)      #Zeitarray, T+dt, damit die Endzeit erreicht wird


    
A=np.array([[-1,0.,0.],[0,-0.5,0],[0,0,-1]])        #Matrix A
D=np.array([np.array([[1,0.3,0],[0,0,0],[0,0,0]]),
            np.array([[0,0,0],[0,0,0],[0,0,0]]),
            np.array([[0.1,0,0],[0,0,0],[0,0,0]])])    #Array D hat als Einträge Matrizen B1,B2,...
            
C=np.array([[1,5,2],[0,0,0],[0,0,0]])    #Matrix C

kappa=0.65         #Hemodynamischen Parameter
gamma=0.41
tau=0.98
alpha=0.32
rho=0.34
V0=0.02
k1=7*rho
k2=2
k3=2*rho-0.2
N=3         #Netzwerkgroesse


u=np.zeros((len(D),m))      #Anregung u
u[0,0]=1
u[2,0]=2

x=np.zeros((5*N,m+1))      
#Initialisierung der Gesamtmatrix, wir haben 5 Variablen deshlab 5*N Zeilen und m+1 Spalten(fuer jeden Zeitschritt und Anfangsvektor)
x_0=np.array([1,2,3,4,5,6,1,2,3,4,5,6,2,3,1])   
#Anfangswertvektor (enthält Aktivität und alle hemodynamische Größen hintereinander, Reihenfolge: z, s, f, v, q)
x[:,0]=x_0
#Anfangsvektor wird als erste Spalte in die Gesamtmatrix eingefuegt
#---------------------------------------------------------------------------------------------------------------------

            

    
teta=np.array([A,D,C,kappa,gamma,tau,alpha,rho,N])    #Parameterset fuer DGLs
teta_out=np.array([N,V0,k1,k2,k3])                             #Parameterset fuer output y



def f(x,teta,u):       #Gibt die Zeitableitung x_dot wider
    N=teta[8]           #Groesse unseres Netzwerkes   
    B=0                         
    for i in range(len(teta[1])):
        B=B+teta[1][i]*u[i]                 # Summe B_i * u_i wird berechnet und als B abgespeichert
    
        
    z=np.hsplit(x,(0,N))[1]         #Die zeitabhängigen Variablen werden aus dem Gesamtvektor herausgeschnitten
    s=np.hsplit(x,(N,2*N))[1]
    f=np.hsplit(x,(2*N,3*N))[1]
    v=np.hsplit(x,(3*N,4*N))[1]
    q=np.hsplit(x,(4*N,5*N))[1]
    
    
    z_dot=np.dot(teta[0]+B,z)+np.dot(teta[2],u)      #Die einzelnen Differentialgleichungen, np.dot vermittelt ein Matrixprodukt
    s_dot=z-teta[3]*s-teta[4]*(f-1)
    f_dot=s
    v_dot=1/teta[5]*(f-v**(1/teta[6]))
    q_dot=1/teta[5]*(f*(1-(1-teta[7])**(1/f))/teta[7]-v**(1/teta[6])*q/v)
    
    x_dot=np.hstack((z_dot,s_dot,f_dot,v_dot,q_dot))               #Alles wird wieder zum Gesamtvektor hinzugefügt
    #print(x_dot)
    return x_dot      

def output(x,teta_out):             #Hier wird der experimentell relevante Output y berechnet
    
    v=np.vsplit(x,(3*N,4*N))[1]
    q=np.vsplit(x,(4*N,5*N))[1]
    
    return teta_out[1]*(teta_out[2]*(1-q)+teta_out[3]*(1-q/v)+teta_out[4]*(1-v))
    
        


x=RK.RK4_method(f,teta,u,x,dt,m)    #Aufruf des RK4-Verfahrens
y=output(x,teta_out)    #Aus den hemodyn. Groessen wird y berechnet
#print(x,y)

plt.figure()
for i in range(N):
    plt.xlim((t0,T))
    plt.plot(t,y[i,:])      #Jede Zeile des experimentellen Outputvektors wird gegen die Zeit geplottet

plt.savefig("test")

