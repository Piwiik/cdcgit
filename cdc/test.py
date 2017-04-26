from cdc import *
from petit_catalogue import PETIT_CATALOGUE
import timeit
import os

ah = charge_petit_catalogue(PETIT_CATALOGUE)

temps = timeit.timeit("os.system('')")
print(temps)
"""
print()
beh = reduit_parcours(ah,-0.5,0.5,1.5,2.5)
print()
print(beh)
"""

"""
w = 0
for i in ah :
    print(w,i,sep="             ")
    w+=1
    """

"""
ah = charge_petit_catalogue(PETIT_CATALOGUE)
for i in beh :
    print(i,ah[i],sep='               ')

g = trouve_inferieur(ah,0,'de',True)

for i in ah :
    print(i)
print()
print(g)
"""
