#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
:mod: cdc

:author: Jean-Luc Levaire

:date: 2017, march

Squelette de programme pour le projet 'Cartes du ciel'.
Permet de charger un catalogue, sélectionner les étoiles dans une zone du ciel
déterminée par son centre et son rayon, projeter les étoiles d'une zone dans le plan,
sauvegarder les étoiles projetées dans un fichier csv.
"""
import math

### CATALOGUES ###
def charge_petit_catalogue(c):
    """ renvoie un catalogue à partir d'une liste d'étoiles c.
	Chaque étoile de la liste c est un dictionnaire dont les champs sont:
 	- 'nom' (str): nom de l'étoile
 	- 'ra' (float): ascension droite en degrés de 0° à 360°
 	- 'de' (float): déclinaison en degrés de -90° à +90°
 	- 'Vmag' (float): magnitude apparente
	Valeur renvoyée: un catalogue sous forme d'une liste de dictionnaires
	dont les champs sont:
 	- 'nom' (str): nom de l'étoile
 	- 'ra_degres' (float): ascension droite en degrés de 0° à 360°
 	- 'de_degres' (float): déclinaison en degrés de -90° à +90°
 	- 'ra' (float): ascension droite en radians de -pi à +pi
 	- 'de' (float): déclinaison en radians de type -pi/2 à +pi/2
 	- 'mag': magnitude de type float
 	CU: aucune
 	"""
    starcount=0
    catalog=[]
    for cstar in c:
        star=dict()
        star['nom']=cstar['nom']
        star['mag']=cstar['Vmag']
        star['ra_degres']=cstar['ra']
        star['de_degres']=cstar['de']
        star['ra'] = math.radians(star['ra_degres'])
        # pour que (0,0) soit au centre de la carte, il faut décaler les points
        # de l'intervalle ]+pi, +2*pi] vers l'intervalle ]-pi, 0.0]
        if star['ra'] > math.pi:
            star['ra'] = star['ra'] - 2.0 * math.pi
        star['de'] = math.radians(star['de_degres'])
        catalog.append(star)
        starcount+=1
    print("Petit catalogue: lu "+str(starcount)+" étoiles")
    return catalog

def charge_bright_star_5(nomfichier):
    """
    Entrée : (str) le nom du fichier d'où lire les données
    Sortie : un catalogue sous forme d'une liste de dictionnaires dont les champs sont:
        - 'nom' (str): nom de l'étoile
        - 'ra_degres' (float): ascension droite en degrés de 0° à 360°
        - 'de_degres' (float): déclinaison en degrés de -90° à +90°
        - 'ra' (float): ascension droite en radians de -pi à +pi
        - 'de' (float): déclinaison en radians de type -pi/2 à +pi/2
        - 'mag': magnitude de type float
    CU : nomfichier est sous le format du Bright Star Catalogue : http://cdsarc.u-strasbg.fr/viz-bin/Cat?V/50
    """
    starcount=0
    catalog=list()
    with open(nomfichier,'r') as entree :
        curseur=entree.read(4)
        while curseur!='':
            star=dict()
            star['nom']='HR'+curseur
            entree.read(71)
            RAh=entree.read(2)
            if RAh!='  ':
                RAh=float(RAh)
                RAm=float(entree.read(2))
                RAs=float(entree.read(4))
                star['ra_degres']=15.0*RAh+((15.0*(60.0*RAm+RAs))/3600)
                star['ra']=math.radians(star['ra_degres'])
                if star['ra'] > math.pi:
                    star['ra'] = star['ra'] - 2.0 * math.pi
                DEsgn=float(entree.read(1)+'1')
                DEd=float(entree.read(2))
                DEm=float(entree.read(2))
                DEs=float(entree.read(2))
                star['de_degres']=DEsgn*(DEd+((15.0*(60.0*DEm+DEs))/3600))
                star['de'] = math.radians(star['de_degres'])
                entree.read(12)
                star['mag']=float(entree.read(5))
                catalog.append(star)
                starcount+=1
            entree.readline()
            curseur=entree.read(4)
    print('Catalogue : lu ',starcount,' étoiles')
    return catalog

def charge_henri_draper(nomarchive) :
	"""
	Entrée : nomarchive (str) le nom de l'archive gzip d'où lire les données
    Sortie : un catalogue sous forme d'une liste de dictionnaires dont les champs sont:
        - 'nom' (str): nom de l'étoile
        - 'ra_degres' (float): ascension droite en degrés de 0° à 360°
        - 'de_degres' (float): déclinaison en degrés de -90° à +90°
        - 'ra' (float): ascension droite en radians de -pi à +pi
        - 'de' (float): déclinaison en radians de type -pi/2 à +pi/2
        - 'mag': magnitude de type float
    CU : nomarchive est une archive gzip contenant un fichier data (extensions .dat.gzip)
	"""
	import gzip
	starcount = 0
	catalog = list()
	with gzip.open(nomarchive,'rt') as entree :
		#On peut lire ligne par ligne car leur longueur est peu élevée et a donc peu d'impact sur la mémoire (moins de 50 caractères)
		curseur = entree.readline()
		while curseur != '' :
			if curseur[29:34] != '     ' or curseur[36:41] != '     ' :
				star = dict()
				star['nom'] = 'HR' + curseur[:6].split()[0]
				star['ra_degres'] = 15*float(curseur[18:20]) + float(curseur[20:23])/40
				star['ra'] = math.radians(star['ra_degres'])
				if star['ra'] > math.pi :
					star['ra'] = star['ra'] - 2.0 * math.pi
				star['de_degres'] = float(curseur[23]+'1') * (float(curseur[24:26]) + float(curseur[26:28])/60)
				star['de'] = math.radians(star['de_degres'])
				try :
					star['mag'] = float(curseur[29:34])
				except ValueError :
					star['mag'] = float(curseur[36:41])
				catalog.append(star)
				starcount += 1
			curseur = entree.readline()
	print('Catalogue : lu ',starcount,' étoiles')
	return catalog


### CALCUL DU CHAMP ###
def calcul_centre_zone_observee(lat,long,temps,az,alt):
	'''
	/!\ pas encore implémenté
	Paramètres :
		lat : (float) la latitude de l'observateur
		long : (float) la longitude de l'observateur
		temps : (tuple) l'heure UTC à laquelle l'observation est fait sous forme d'un triplet d'entiers (int) (heures,minutes,secondes)
		az : (float) l'azimut en degrés, le sud étant à 0°, l'ouest à 90°
		alt : (float) l'altitude (l'angle d'élévation) en degrés
	Sortie : (tuple) un couple (RA0, DE0) de coordonnées équatoriales du point désigné par les paramètres
	CU :
		lat est compris entre -90 et 90
		long est compris entre -180 et 179
		heures est compris entre 0 et 23, minutes est compris entre 0 et 59, secondes est compris entre 0 et 59
		az est compris entre 0 et 359
		alt est compris entre -90 et 90
	'''
	long=(long-(temps[0]+temps[1]/60+temps[2]/3600)*15)%360-180
	print("Cette fonction n'est pas encore fonctionnelle")

def selection_champ_parcours_complet(catalogue, centre, rayon):
	"""
	Paramètres :
		catalogue : un catalogue sous forme d'une liste de dictionnaires dont les champs sont:
	        - 'nom' (str): nom de l'étoile
	        - 'ra_degres' (float): ascension droite en degrés de 0° à 360°
	        - 'de_degres' (float): déclinaison en degrés de -90° à +90°
	        - 'ra' (float): ascension droite en radians de -pi à +pi
	        - 'de' (float): déclinaison en radians de type -pi/2 à +pi/2
	        - 'mag' (float): magnitude de type float
		centre : un couple de flottants (RA0, DE0) des coordonnées en radians du centre de la zone observée
		rayon : un flottant indiquant le rayon de la zone observée
	Sortie : un catalogue de même forme comportant les étoiles du catalogue en paramètre qui son dans le rayon du cercle
	"""
	sinDE0=math.sin(centre[1])
	cosDE0=math.cos(centre[1])
	sortie=[]
	istar = 0
	l = len(catalogue)
	while istar < l :
		if rayon>=math.acos(sinDE0*math.sin(catalogue[istar]['de'])+cosDE0*math.cos(catalogue[istar]['de'])*math.cos(math.fabs(centre[0]-catalogue[istar]['ra']))):
			sortie.append(istar)
		istar += 1
	return sortie

def compare(x,y,cle):
	"""
	Paramètres :
	x, y : (dict) deux dictionnaires ayant tous les deux un élément de clé cle
	cle : une clé contenue dans les deux dictionnaires
	Sortie :
	-1 si x[cle] < y[cle]
	0 si x[cle] == y[cle]
	1 si x[cle] > y[cle]
	CU : cle est une clé contenue dans les x et y et x[cle] et y[cle] sont comparables par les opérateurs >, >= et ==
	"""
	if x[cle] < y[cle] :
		return -1
	elif x[cle] > y[cle] :
		return 1
	else :
		return 0

def tri_insert(l, cle):
    """
    paramètre l : (list) une liste à trier
	paramètre cle : clé selon laquelle les dictionnaires seront triés
    valeur renvoyée : (NoneType) aucune
    effet de bord : modifie la liste l en triant ses dictionnaires selon la valeur associée à la clé cle
    CU : l liste de dictionnaires comportant tous la clé cle
    """
    n = len(l)
    for i in range(1, n):
        aux = l[i]
        k = i
        while k >= 1 and comp(aux, l[k - 1], cle) == -1:
            l[k] = l[k - 1]
            k = k - 1
        l[k] = aux

def selection_champ_parcours_restreint(catalogue, centre, rayon):
    """
	Paramètres :
		catalogue : un catalogue sous forme d'une liste de dictionnaires dont les champs sont:
	        - 'nom' (str): nom de l'étoile
	        - 'ra_degres' (float): ascension droite en degrés de 0° à 360°
	        - 'de_degres' (float): déclinaison en degrés de -90° à +90°
	        - 'ra' (float): ascension droite en radians de -pi à +pi
	        - 'de' (float): déclinaison en radians de type -pi/2 à +pi/2
	        - 'mag' (float): magnitude de type float
		centre : un couple de flottants (RA0, DE0) des coordonnées en radians du centre de la zone observée
		rayon : un flottant indiquant le rayon de la zone observée
	Sortie : un catalogue de même forme comportant les étoiles du catalogue en paramètre qui son dans le rayon du cercle
    """
    print("Fonction non implémentée")

### CHANGEMENT DE REPERE SUR LA SPHERE ###
def changement_de_repere(point, origine):
    """
	renvoie les coordonnées du point de coordonnées sphériques point
	dans le repère dont l'origine est le point de coordonnées sphériques origine.
	CU: les coordonnées sont en radian
    """
    ra, de = point
    ra0, de0 = origine
    dra = ra - ra0
    alpha=(math.pi / 2.0) - de0
    beta = 0.0
    de_origine=math.asin((math.sin(alpha)*math.sin(de)) - (math.cos(alpha)*math.cos(de)*math.cos(dra)))
    ra_origine=beta+math.atan2(math.cos(de)*math.sin(dra),
                              (math.cos(alpha)*math.sin(de)) + (math.sin(alpha)*math.cos(de)*math.cos(dra)))
    return (ra_origine, de_origine)

### PROJECTIONS ###
def projection_equirectangulaire(point):
    """
	renvoie les coordonnées (x,y) dans le plan du point de coordonnées sphériques point
	pour la projection equirectangulaire.
 	- point (float, float): couple (ra, de) des coordonnées sphériques du point à projeter
 	- valeur renvoyée (float, float): couple (x,y) des coordonnées du point projeté dans le plan
 	CU: aucune
    """
    ra, de = point
    x = ra
    y = de
    return (x, y)

def projection_aitoff(point):
    """
	renvoie les coordonnées (x,y) dans le plan du point de coordonnées sphériques point
	pour la projection aitoff.
 	- point (float, float): couple (ra, de) des coordonnées sphériques du point à projeter
 	- valeur renvoyée (float, float): couple (x,y) des coordonnées du point projeté dans le plan
 	CU: aucune
    """
    ra, de = point
    alpha=math.acos(math.cos(de)*math.cos(ra/2.0))
    if alpha!=0.0:
        sincalpha=math.sin(alpha)/alpha
    else:
        sincalpha=1.0
    x=2.0 * math.cos(de) * math.sin(ra/2.0) / sincalpha
    y=math.sin(de)/sincalpha
    return (x, y)

def projection_stereographic(point):
	"""
	renvoie les coordonnées (x,y) dans le plan du point de coordonnées sphériques point
	pour la projection stéréographique.
 	- point (float, float): couple (ra, de) des coordonnées sphériques du point à projeter
 	- valeur renvoyée (float, float): couple (x,y) des coordonnées du point projeté dans le plan
 	CU: aucune
 	"""
	RA,DE = point
	x1 = math.cos(DE) * math.sin(RA)
	y1 = math.sin(DE)
	k = 2 / (1.0 + math.cos(DE) * math.cos(RA))
	x = k * x1
	y = k * y1
	return (x,y)

def projection_lambert_equal_area(point):
	"""
	renvoie les coordonnées (x,y) dans le plan du point de coordonnées sphériques point
	pour la projection azimutale équivalent de Lambert.
 	- point (float, float): couple (ra, de) des coordonnées sphériques du point à projeter
 	- valeur renvoyée (float, float): couple (x,y) des coordonnées du point projeté dans le plan
 	CU: aucune
    """
	RA,DE=point
	x1 = math.cos(DE) * math.sin(RA)
	y1 = math.sin(DE)
	k = math.sqrt(abs(2 / (1.0 + math.cos(DE) * math.cos(RA))))
	x = k * x1
	y = k * y1
	return (x,y)

### ECHELLE ###
def echelle_projection(projection, rayon, largeur, hauteur):
    """
	renvoie l'échelle à utiliser pour effectuer le dessin d'une zone de rayon rayon
	en utilisant la projection projection dans une fenêtre de taille largeurxhauteur
 	- projection (function): fonction de projection
 	- rayon (float): rayon de la zone à projeter en radians
 	- largeur, hauteur (int): taille de la fenêtre où l'on projette en pixels
	Valeur renvoyée (float): échelle en pixels par radian
	CU: rayon positif non nul
    """
    assert rayon > 0, 'echelle_projection: le rayon doit être strictement positif'
    if projection==projection_equirectangulaire or projection==projection_aitoff:
        rayon_image=rayon
    else:
        rayon_image=rayon
    echelle_x = largeur / (2.0 * rayon_image)
    if projection==projection_equirectangulaire or projection==projection_aitoff:
        echelle_y = hauteur / ((2.0 * rayon_image) if (rayon_image < math.pi/2) else math.pi)
    else:
        echelle_y = hauteur / ((2.0 * rayon_image))
    echelle = min(echelle_x, echelle_y)
    return echelle

### SORTIE CSV ###
def champ_vers_csv(catalogue, champ, nomfichier='sortiecdc.csv'):
    """
	crée un fichier csv contenant les étoiles du champ d'étoiles champ provenant du catalogue catalogue.
 	- catalogue (list): catalogue d'étoiles
 	- champ (list): liste des index dans catalogue des étoiles du champ sélectionné
 	- nomfichier (str): nom du fichier csv à créer (ou écraser)
 	- valeur renvoyée: aucune
 	CU: aucune
    """
    if type(nomfichier) == str:
        f=open(nomfichier, mode='w')
    else:
        f=nomfichier
    if len(catalogue) > 0:
        #première ligne: ecriture de l'entête des colonnes
        entetes=catalogue[0].keys()
        for k in entetes:
            f.write(k+';')
        f.write('\n')
        for index in champ:
            etoile=catalogue[index]
            for k in entetes:
                f.write(str(etoile[k])+';')
            f.write('\n')
    f.close()

### IMPRESSION DE LA CARTE ###
def imprimer_carte(catalogue, centre, rayon, projection, selection, largeur=512, hauteur=512, nomfichier="sortiecdc.svg"):
    if type(nomfichier) == str:
        f=open(nomfichier, mode='w')
    else:
        f=nomfichier
    f.write('<svg width="'+str(largeur)+'" height="'+str(hauteur)+'" style="background-color: white;" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">\n')
    select = selection(catalogue, centre, rayon)
    echelle = echelle_projection(projection, rayon, largeur, hauteur)
    maxmag = 0
    l_coordonnees = []
    for istar in select :
        mag = catalogue[istar]['mag']
        coordonnees = projection(changement_de_repere((catalogue[istar]["ra"] , catalogue[istar]["de"]) , centre))
        coordonnees = (-coordonnees[0]*echelle+largeur//2 , -coordonnees[1]*echelle+hauteur//2 , mag)
        maxmag = max(maxmag , mag)
        l_coordonnees.append(coordonnees)
    separateur = [maxmag*0.50,maxmag*0.75,maxmag*0.87,maxmag*0.95,maxmag]
    for coordonnees in l_coordonnees :
        r = 0.5
        isep = 0
        while isep < 5 and coordonnees[2] >= separateur[isep] :
            r += 0.5
            isep += 1
        f.write('<circle cx="'+str(coordonnees[0])+'" cy="'+str(coordonnees[1])+'" r="'+str(r)+'" />\n')
    f.write('</svg>')
    f.close()


### PROGRAMME PRINCIPAL EN MODE TEXTE ###
def usage():
    print('Usage : cdc.py [OPTION] [<nom fichier>]')
    print('    <nom fichier> = nom du fichier (csv ou svg) à produire. Si absent : stdout')
    print('    OPTION =')
    print('             -h  : cette aide')
    print('             -c  : centre de la zone sous la forme ra de avec 0<=ra<=360 et -90<=de<= 90')
    print('                   exemple: -c 84.05 -1.2')
    print('             -r  : rayon de la zone en degrés')
    print('                   exemple: -r 10.0')
    print('             -o  : csv ou svg')
    print('    Pas d\'option équivaut à -c 84.05 -1.2 -r 10.0 -o csv')
    exit(1)

def main():
    import sys
    centre_degres=(84.05, -1.2)
    rayon_degres=10.0
    formatsortie='csv'
    sortie=sys.stdout
    iarg=1
    while iarg <= len(sys.argv) - 1:
        arg=sys.argv[iarg]
        if arg == '-h':
            usage()
        elif arg == '-c':
            try:
                ra0=float(sys.argv[iarg+1])
                de0=float(sys.argv[iarg+2])
            except:
                usage()
            centre_degres=(ra0, de0)
            iarg+=3
        elif arg == '-r':
            try:
                rayon_degres=float(sys.argv[iarg+1])
            except:
                usage()
            iarg+=2
        elif arg == '-o':
            formatsortie=sys.argv[iarg+1]
            if formatsortie != 'csv' and formatsortie!='svg':
                usage()
            iarg+=2
        else:
            if iarg == len(sys.argv) - 1 and sys.argv[iarg][0]!='-':
                sortie=sys.argv[iarg]
                iarg+=1
            else:
                usage()
    # conversion en radians
    centre=(math.radians(centre_degres[0]), math.radians(centre_degres[1]))
    rayon=math.radians(rayon_degres)

    # choix catalogue
    import petit_catalogue
    #catalogue=charge_petit_catalogue(petit_catalogue.PETIT_CATALOGUE)
    catalogue=charge_bright_star_5("bsc5.dat")

    # Choix du parcours de la selection d'étoiles
    selection=selection_champ_parcours_complet
    #selection=selection_champ_parcours_restreint

    #choix de la projection
    projection=projection_equirectangulaire
    #projection=projection_aitoff
    if formatsortie=='csv':
        champ=selection(catalogue, centre, rayon)
        champ_vers_csv(catalogue, champ, nomfichier=sortie)
    else:
        imprimer_carte(catalogue, centre, rayon, projection, selection, 1024, 1024, nomfichier=sortie)

if __name__ == '__main__' :
    import doctest
    doctest.testmod(verbose=False)

    main()
