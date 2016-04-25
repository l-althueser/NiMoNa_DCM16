#!/usr/bin/env python

#==============================================================================
#	Euler_1O.py
#------------------------------------------------------------------------------
# description    :Implementation eines Euler Verfahrens 1. Ordnung (1O).
# author         :l-althueser
#
# usage          :
# python_version :3.5.1
#
# changes/notes  :20160425 :
#==============================================================================

# Explizites Euler-Verfahren 1. Ordnung
def Euler_1O(f,t_0,t_k,y_0,n):
	# f  : gegeben als y' = f(t,y)
	# t_0: Startwert für t (initial value)
	# t_k: Endwert für t (final value)
	# y_0: Startwert für y mit y(t_0) = y_0
	# n  : Anzahl der Schritte auf dem Interval [t_0, t_k]
	# h  : Diskretisierungs-Schrittweite mit h > 0
	# Gibt eine Matrix von angenommenden Werte zurück. (<- Das muss noch getan werden.)

    h = (t_k - t_0) / float(n)
    t = t_0
    y = y_0
    for i in range(n):
        y += h * f(t, y)
        t += h
    return y # <- Hier eine Matrix rausgeben!
