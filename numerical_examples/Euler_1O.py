#!/usr/bin/env python

#==============================================================================
#	Euler_1O.py
#------------------------------------------------------------------------------
# description    :Implementation eines Euler Verfahrens 1. Ordnung (1O).
# author         :	l-althueser
#				t-wiedemann
#
# usage          :
# python_version :3.5.1
#
# changes/notes  :20160425 :
#==============================================================================

# Explizites Euler-Verfahren 1. Ordnung
# Merke Euler-Verfahren = RK1
# y' = f0(t,y)
# y(t_n+1) = y_n+1 = y_n + h * f(t_n,y_n)


def Euler_1O(f,t,t_k,y,n):
	# f  : gegeben als y' = f(t,y)
	# t_0: Startwert für t (initial value)
	# t_k: Endwert für t (final value)
	# y_0: Startwert für y mit y(t_0) = y_0
	# n  : Anzahl der Schritte auf dem Interval [t_0, t_k]
	# h  : Diskretisierungs-Schrittweite mit h > 0
	# Gibt eine Matrix von angenommenden Werte zurück.

    h = (t_k - t[:,0]) / float(n)

    for i in range(n):			
        y[:,i+1] = y[:,i] + h * f(t[:,i], y[:,i])
        t[:,i+1] = t[:,i] + h
		
    return y 