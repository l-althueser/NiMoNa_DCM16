#!/usr/bin/env python

#==============================================================================
#	Euler_1O_test.py
#------------------------------------------------------------------------------
# description    :Implementation eines Euler Verfahrens 1. Ordnung (1O).
# author         :l-althueser
#
# usage          :python Euler_1O_test.py
# python_version :3.5.1
#
# changes/notes  :20160425 :
#==============================================================================

import math
import numpy as np
import matplotlib.pyplot as plt
import Euler_1O

#Anfangswertvektor, bereits in gewünschter Matrixschreibweise
t_0 = np.array([[0],[0]])
y_0 = np.array([[0],[1]])

# Explizites Euler-Verfahren 1. Ordnung
y = Euler_1O.Euler_1O(lambda x, y: math.cos(x), t_0, 1, y_0, 1000)

#print(y,t)
plt.figure()
for i in range(len(y)):
    plt.plot(t,y[i,:])      #Jede Zeile wird gegen die Zeit geplottet