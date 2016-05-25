# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 17:49:20 2016

@author: Tobias

Testcode, um die Funktionalität des RK4-Verfahrens zu überprüfen
"""

import numpy as np
import RK4 as RK
import matplotlib.pyplot as plt


#Eingabe Parameter
T=1200                      #Endzeit - als float eingeben
t0=0                        #Anfangszeit - als float eingeben 
n=256                       #Zeitschrittanzahl
dt=(float(T)-float(t0))/n   #Zeitschrittlaenge - beruecksichtigt, dass dt float sein kann
t = np.arange(t0,T,dt)      #Zeitarray 

#Eingabe hemodynamische Parameter
kappa=1         
gamma=1
tau=1
alpha=1
rho=1
V0=0.02
k=([7*rho,2,2*rho-0.2])
N=3                     #Netzwerkgroesse    

A=np.matrix("-0.4, 0, 0; 0, -0.1, 0; 0, 0, -0.3")               #Matrix A (3x3) negative Eintraege auf der Hauptdiagonalen
B=np.array([np.matrix("-0.4, 0, 0; 0, -0.1, 0; 0, 0, -0.3"),
            np.matrix("-0.4, 0, 0; 0, -0.1, 0; 0, 0, -0.3"),
            np.matrix("-0.4, 0, 0; 0, -0.1, 0; 0, 0, -0.3")])   #Array D hat als Eintraege Matrizen B1,B2,...
            
C=np.matrix("-0.4, 0.1, 0; 0, -0.1, 0; 0, 0, -0.3")             #Matrix C  


x=np.zeros((5*N,n))                             #spaltenweiser Eintrag von z,s,f,v,q nach jeder Zeitschrittlaenge dt
x_0=np.array([1,1,1,2,2,2,3,3,3,4,4,4,5,5,5])   #x als z,s,f,v,q je N Zeilen im Spaltenvektor für die Anfangsbedingungen
x_0=np.transpose(x_0)                           #transponiert x_0 zu Spaltenvektor (Notwendigkeit pruefen)
x[:,0]=x_0                                      #traegt x_0 als erste Spalte in x ein

u=np.zeros((N,N))       #Anregung u - Matrix braucht die Groesse von C
u_0=np.array([1,1,1])   #definiert u_0 
u_0=np.transpose(u_0)   #transponiert u_0 zu Spaltenvektor (Notwendigkeit pruefen)
u[:,0]=u_0              #trägt u_0 als erste Spalte in u ein

#---------------------------------------------------------------------------------------------------------------------

const=C*u               #C*u soll zeitabhaenigig aber vorgegeben sein
            
for i in range(len(B)): #len(B) gibt die Anzahl der B_j 
    D=+B[i]*u[i]
    
teta=list((A,D,const,kappa,gamma,tau,alpha,rho,N))    #Parameterset fuer DGLs
teta_out=list((N,V0,k))                             #Parameterset fuer output y

    

def f(x,teta):       #Ab hier tritt ein Fehler auf in dieser Version - Gibt die Zeitableitung x_dot wieder - abhier tritt ein Fehler im Zusammenhang mit dem RK4 auf
    N=teta[8]                             #Groesse unseres Netzwerkes
    
    #x=x[:,1] # dies war die Üeberlegung beim Treffen heute, umgekehrt sollte die Matrix auch wieder spaltenweise beschrieben werden koennen - das Problem liegt aber in der 1 in Zeile 65, sie müsste irgendwie durchlaufen 
    #z=x[0:N,0]
    #z=x[N:2*N,0] 
    #z=x[2*N:3*N,0] 
    #z=x[3*N:4*N,0] 
    #z=x[4*N:5*N,0]     
    
    z=np.hsplit(x,(0,N))[1]         #Die zeitabhaengigen Variablen werden aus dem Gesamtvektor herausgeschnitten - kann das nicht ueber z=x[0:3,0] realisiert werden?
    s=np.hsplit(x,(N,2*N))[1]
    f=np.hsplit(x,(2*N,3*N))[1]
    v=np.hsplit(x,(3*N,4*N))[1]
    q=np.hsplit(x,(4*N,5*N))[1]
    
    z_dot=(teta[0]+teta[1])*z+teta[2]      #Die einzelnen Differentialgleichungen
    s_dot=z-teta[3]*s-teta[4]*(f-1)
    f_dot=s
    v_dot=1/teta[5]*(f-v**(1/teta[6]))
    q_dot=1/teta[5]*(f*(1-(1-teta[7])**(1/f))/teta[7]-v**(1/teta[6])*q/v)
    
    x_dot=np.vstack((z_dot,s_dot,f_dot,v_dot,q_dot))               #Alles wird wieder zum Gesamtvektor hinzugefügt
    #print(x_dot)
    return x_dot      

def output(x,teta_out):             #Hier wird der experimentell relevante Output y berechnet
    
    v=x[3*N:4*N,0]
    q=x[4*N:5*N,0]
    
    return teta_out[1]*(teta_out[2][0]*(1-q)+teta_out[2][1]*(1-q/v)+teta_out[2][2]*(1-v))
    
        


x=RK.RK4_method(f,teta,x_0,dt,n)
y=output(x,teta_out)

#print(x,y)

plt.figure()
for i in range(N):
    plt.plot(t,np.squeeze(np.asarray(y[i,:])))      #Jede Zeile des experimentellen Outputvektors wird gegen die Zeit geplottet

plt.savefig("test")

