#!/usr/bin/env python

#==============================================================================
#	RK_4O.py
#------------------------------------------------------------------------------
# description    :Implementation eines Runge-Kutta-Verfahrens 4. Ordnung (4O).
# author         :l-althueser
#
# usage          :
# python_version :3.5.1
#
# changes/notes  :20160425 :
#==============================================================================

# import of needed libaries
import numpy as np

# the following code is written for a specific function and needs to be adapted as seen in Euler_1O.py

# define constant values and parameters
L = 2.*np.pi # interval length
N = 128      # steps in the interval
             # n = 2^p - an integer power of 2
dx = L/N     # step size
c = 0.3      # velocity of the advection equation
h = 0.01     # time step in the Runge-Kutta-Method (RK)
T = 10     # end time of the system t \in [0,T]

# define x- and k-axis
x = np.arange(0,L,dx)                    # x-array
k = np.fft.fftfreq(int(N),L/(2*np.pi*N)) # k-array

# definition of the given initial condition
# L instead of (np.pi/2) could also be used
u_0_x = np.exp(-2*np.pi*(x-(np.pi/2))**2) 
u_0_k = np.fft.fft(u_0_x)

# evaluation of f = du_k/dt of the ordinary differential equation (ODE) system
# in Fourier space
def f(u,k,c):
    return -1j*u*k*c

# define u_k as start point
u_k = u_0_k
    
# evaluate the solution with the RK4 (Fourier)
for i in range(0,T+1,1):
    # define all k
    k_1 = f(u_k,k,c)
    k_2 = f(u_k + 0.5*h*k_1,k,c)
    k_3 = f(u_k + 0.5*h*k_2,k,c)
    k_4 = f(u_k + h*k_3,k,c)
    u_k = u_k + (h/6)*(k_1 + 2*k_2 + 2*k_3 + k_4)

    u = np.fft.ifft(u_k)
