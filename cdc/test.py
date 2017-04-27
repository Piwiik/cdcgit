from cdc import *
from petit_catalogue import PETIT_CATALOGUE
import timeit
import os

oui = charge_henri_draper("hd.dat.gz")
temps1 = timeit.timeit(stmt="selection_champ_parcours_complet(oui,(50,50),20)",number=5,globals=globals())
oui = charge_henri_draper("hd.dat.gz")
temps2 = timeit.timeit(stmt="selection_champ_parcours_restreint(oui,(50,50),20)",number=5,globals=globals())
oui = charge_henri_draper("hd.dat.gz")
temps3 = timeit.timeit(stmt="selection_omg(oui,(50,50),20)",number=5,globals=globals())
print("Parcours complet :",temps1,"secondes\nParcours restreint :",temps2,"secondes\nParcours omg :",temps3,"secondes")

"""
temps1 = timeit.timeit(stmt="reduit_parcours(oui,-1,1,-1,1)",number=5,globals=globals())
oui = charge_henri_draper("hd.dat.gz")
temps2 = timeit.timeit(stmt="omg(oui,-1,1,-1,1)",number=5,globals=globals())
print("reduit_parcours :",temps1,"secondes\nomg :",temps2,"secondes")

ah = reduit_parcours(oui,-1,1,-1,1)
beh = omg(oui,-1,1,-1,1)
ah.sort()
beh.sort()
print(ah[:100])
print(beh[:100])
print(len(ah),len(beh))
print(ah==beh)




temps = timeit.timeit(stmt="os.system('python cdc.py -c 90 20 -r 30 -o svg wow.svg')", globals=globals(), number=5)
print(temps)
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
