#!/usr/bin/env python

#==============================================================================
#	Euler_1O_test.py
#------------------------------------------------------------------------------
# description    :Implementation eines Euler Verfahrens 1. Ordnung (1O).
#
# usage          :python Euler_1O_test.py
# python_version :3.5.1
#
#==============================================================================

import math
import numpy as np
import matplotlib.pyplot as plt
import Euler_1O

# Explizites Euler-Verfahren 1. Ordnung
# Euler_1O(Funktion, t(0), t(END), y(0), Schritte)
E = Euler_1O.Euler_1O(lambda t, y: math.sin(t), 0, 20, 1, 1000)

plt.figure()
plt.plot(E[0,:], E[1,:])      #Jede Zeile wird gegen die Zeit geplottet
plt.show()