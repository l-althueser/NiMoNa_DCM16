#!/usr/bin/env python

#==============================================================================
#	Euler_1O.py
#------------------------------------------------------------------------------
# description    :Implementation eines Euler Verfahrens 1. Ordnung (1O).
#
# usage          :
# python_version :3.5.1
#
#==============================================================================

import numpy as np

def Euler_1O(f,t_0,t_k,y_0,n):
	# f  : gegeben als y' = f(t,y)
	# t_0: Startwert für t (initial value)
	# t_k: Endwert für t (final value)
	# y_0: Startwert für y mit y(t_0) = y_0
	# n  : Anzahl der Schritte auf dem Interval [t_0, t_k]
	# h  : Diskretisierungs-Schrittweite mit h > 0
	# Gibt eine Matrix von angenommenden Werte zurück.

	# Erstelle Matrix der Größe n
	E = np.hstack((np.vstack((t_0,y_0)),np.zeros((2,n))))
	h = (t_k - t_0) / float(n)
	
	for i in range(n):			
		E[1,i+1] = E[1,i] + h * f(E[0,i], E[1,i])	#y
		E[0,i+1] = E[0,i] + h						#t
		
	return E