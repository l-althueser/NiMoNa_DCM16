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
from Euler_1O import Euler_1O

# Explizites Euler-Verfahren 1. Ordnung
print(Euler_1O(lambda x, y: math.cos(x), 0, 1, 1, 1000)) # <- Ausgabe sollte als Matrix erfolgen ..