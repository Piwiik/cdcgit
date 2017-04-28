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
from functools import cmp_to_key

index_de = list()
index_ra = list()

### CATALOGUES ###

def liste_index_trie_de(catalogue):
    """
    Renvoie la liste des indices de étoiles triées selon le DE
    """
    l = list()
    copie = [etoile for etoile in catalogue]
    copie.sort(key=cmp_to_key(compare_de))
    for star in copie:
        l.append(catalogue.index(star))
    return l

def liste_index_trie_ra(catalogue):
    """
    Renvoie la liste des indices de étoiles triées selon le DE
    """
    l = list()
    copie = [etoile for etoile in catalogue]
    copie.sort(key=cmp_to_key(compare_ra))
    for star in copie:
        l.append(catalogue.index(star))
    return l

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
    - 'mag'(float): magnitude
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
    liste1, liste2 = liste_index_trie_de(catalog), liste_index_trie_ra(catalog)
    global index_de, index_ra
    for indice in liste1:
        index_de.append(indice)
    for indice in liste2:
        index_ra.append(indice)
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
        - 'mag'(float): magnitude
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
    liste1, liste2 = liste_index_trie_de(catalog), liste_index_trie_ra(catalog)
    global index_de, index_ra
    for indice in liste1:
        index_de.append(indice)
    for indice in liste2:
        index_ra.append(indice)
    print('Bright Star Catalog : lu ',starcount,' étoiles')
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
        - 'mag'(float): magnitude
    CU : nomarchive est une archive gzip contenant un fichier data (extensions .dat.gzip)
    """
    import gzip
    starcount = 0
    catalog = list()
    with gzip.open(nomarchive,'rt') as sitestriste :
        #On peut lire ligne par ligne car leur longueur est peu élevée et a donc peu d'impact sur la mémoire (moins de 50 caractères)
        curseur = sitestriste.readline()
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
            curseur = sitestriste.readline()
    liste1, liste2 = liste_index_trie_de(catalog), liste_index_trie_ra(catalog)
    global index_de, index_ra
    for indice in liste1:
        index_de.append(indice)
    for indice in liste2:
        index_ra.append(indice)
    print('Henri Draper Catalog : lu ',starcount,' étoiles')
    return catalog

def charge_hipparcos(nomarchive):
    """
    Entrée : nomarchive (str) le nom de l'archive gzip d'où lire les données
    Sortie : un catalogue sous forme d'une liste de dictionnaires dont les champs sont:
        - 'nom' (str): nom de l'étoile
        - 'ra_degres' (float): ascension droite en degrés de 0° à 360°
        - 'de_degres' (float): déclinaison en degrés de -90° à +90°
        - 'ra' (float): ascension droite en radians de -pi à +pi
        - 'de' (float): déclinaison en radians de type -pi/2 à +pi/2
        - 'mag'(float): magnitude
    CU : nomarchive est une archive gzip contenant un fichier data (extensions .dat.gzip)
    """
    import gzip
    starcount = 0
    catalog = list()
    with gzip.open(nomarchive,'rt') as sitestriste :
        curseur = sitestriste.read(6)
        while curseur!='' :
            star = dict()
            star['nom'] = 'HR'+curseur
            sitestriste.read(9)
            star['ra'] = float(sitestriste.read(13))
            if star['ra'] > math.pi:
                star['ra'] = star['ra'] - 2.0 * math.pi
            star['ra_degres'] = math.degrees(star['ra'])
            sitestriste.read(1)
            star['de'] = float(sitestriste.read(13))
            sitestriste.read(87)
            star['mag'] = float(sitestriste.read(7))
            catalog.append(star)
            starcount+=1
            sitestriste.readline()
            curseur = sitestriste.read(6)
    liste1, liste2 = liste_index_trie_de(catalog), liste_index_trie_ra(catalog)
    global index_de, index_ra
    for indice in liste1:
        index_de.append(indice)
    for indice in liste2:
        index_ra.append(indice)
    print('Hipparcos Catalog : lu ',starcount,' étoiles')
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
		catalogue (list): un catalogue sous forme d'une liste de dictionnaires dont les champs sont:
	        - 'nom' (str): nom de l'étoile
	        - 'ra_degres' (float): ascension droite en degrés de 0° à 360°
	        - 'de_degres' (float): déclinaison en degrés de -90° à +90°
	        - 'ra' (float): ascension droite en radians de -pi à +pi
	        - 'de' (float): déclinaison en radians de type -pi/2 à +pi/2
	        - 'mag' (float): magnitude de type float
		centre : un couple de flottants (RA0, DE0) des coordonnées en radians du centre de la zone observée
		rayon : un flottant indiquant le rayon de la zone observée
	Sortie : une liste des index des étoiles dans le catalogue donné en paramètre qui sont dans le rayon du cercle
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

###Permet de trouver l'indice dans la liste d'indices triés de l'étoile tout juste supérieure à inf_de ou inf_ra

def trouve_inferieur_liste(catalogue,liste,inf,cle):
	"""
	Paramètres :
		catalogue (list): un catalogue sous forme d'une liste de dictionnaires dont les champs sont:
	        - 'nom' (str): nom de l'étoile
	        - 'ra_degres' (float): ascension droite en degrés de 0° à 360°
	        - 'de_degres' (float): déclinaison en degrés de -90° à +90°
	        - 'ra' (float): ascension droite en radians de -pi à +pi
	        - 'de' (float): déclinaison en radians de type -pi/2 à +pi/2
	        - 'mag' (float): magnitude de type float
        liste (list) : liste des indices des étoiles triées selon DE ou RA
		inf (float) : un nombre
        cle : une clé commune à tous les dictionnaires du catalogue
	Sortie : (int) Renvoie l'indice dans la liste triée d'indices dont la valeur associée à cle est la plus petite étant supérieure ou égale à inf
    CU : catalogue est trié selon les valeurs associées à la clé cle dans les dictionnaires
    """
	l = len(liste)
	a = 0
	b = l-1
	while catalogue[liste[a]][cle] <= inf :
		m = (a+b)//2
		if catalogue[liste[m]][cle] == inf :
			return m
		elif catalogue[liste[m]][cle] > inf :
			b = m
		else :
			a = m+1
	return a

### Nouvelle sélection à tester avec de gros catalogues

def nouveau_parcours_restreint_ha(catalogue,inf_de, sup_de, inf_ra, sup_ra):
    """
    Paramètres :
        catalogue (list): un catalogue sous forme d'une liste de dictionnaires dont les champs sont:
        - 'nom' (str): nom de l'étoile
        - 'ra_degres' (float): ascension droite en degrés de 0° à 360°
        - 'de_degres' (float): déclinaison en degrés de -90° à +90°
        - 'ra' (float): ascension droite en radians de -pi à +pi
        - 'de' (float): déclinaison en radians de type -pi/2 à +pi/2
        - 'mag' (float): magnitude de type float
        inf_de (float) : valeur minimale de déclinaison des étoiles recherchées en radians
        inf_ra (float) : valeur minimale d'ascension verticale des étoiles recherchées en radians
        sup_de (float) : valeur maximale de déclinaison des étoiles recherchées en radians
        sup_ra (float) : valeur maximale d'ascension verticale des étoiles recherchées en radians
    Sortie : (list) une liste des index dans le catalogue des étoiles correspondant aux critères maximaux et minimaux
        de déclinaison et d'ascension verticale donnés en paramètre

    On parcourt les listes index_de et index_ra jusqu'à atteindre les valeurs supérieures, on obtient
    ainsi deux listes des étoiles appartenant aux champs DE et RA, on renvoie ensuite l'intersection
    des deux listes
    """
    et_de=list()
    et_ra=list()
    indice_min_de = trouve_inferieur_liste(catalogue,index_de,inf_de,'de')
    while catalogue[index_de[indice_min_de]]['de']<=sup_de:
        et_de.append(index_de[indice_min_de])
        indice_min_de+=1
    indice_min_ra = trouve_inferieur_liste(catalogue,index_ra,inf_ra,'ra')
    while catalogue[index_ra[indice_min_ra]]['ra']<=sup_ra:
        et_ra.append(index_ra[indice_min_ra])
        indice_min_ra+=1
    return [indice for indice in et_ra if indice in et_de]

def nouveau_parcours_restreint(catalogue,centre,rayon):
    """
    Paramètres :
		catalogue (list): un catalogue sous forme d'une liste de dictionnaires dont les champs sont:
	        - 'nom' (str): nom de l'étoile
	        - 'ra_degres' (float): ascension droite en degrés de 0° à 360°
	        - 'de_degres' (float): déclinaison en degrés de -90° à +90°
	        - 'ra' (float): ascension droite en radians de -pi à +pi
	        - 'de' (float): déclinaison en radians de type -pi/2 à +pi/2
	        - 'mag' (float): magnitude de type float
		centre : un couple de flottants (RA0, DE0) des coordonnées en radians du centre de la zone observée
		rayon : un flottant indiquant le rayon de la zone observée
	Sortie : une liste des index des étoiles dans le catalogue donné en paramètre qui sont dans le rayon du cercle
    """
    #La plupart des catalogues sont triés approximativement selon l'ascension droite, on commence donc par trier selon RA
    sinDE0=math.sin(centre[1])
	#Le pôle nord a une déclinaison de pi/2 radians, l'ascension verticale est donc non nécessaire :
    contientPoleNord = rayon >= math.acos(sinDE0)
	#Le pôle sud a une déclinaison de -pi/2 radians donc :
    contientPoleSud = rayon >= math.acos(-sinDE0)
    if contientPoleNord and contientPoleSud :
    	return selection_champ_parcours_complet(catalogue, centre, rayon)
    elif contientPoleNord :
    	select = nouveau_parcours_restreint_ha(catalogue,min(centre[1]-rayon,centre[1]+rayon),math.pi/2,-math.pi,math.pi)
    elif contientPoleSud :
    	select = nouveau_parcours_restreint_ha(catalogue,-math.pi/2,max(centre[1]-rayon,centre[1]+rayon),-math.pi,math.pi)
    else :
        delta = math.asin(math.sin(rayon)/math.sin(math.pi/2 - centre[1]))
        select = nouveau_parcours_restreint_ha(catalogue,min(centre[1]-rayon,centre[1]+rayon),max(centre[1]-rayon,centre[1]+rayon),min(centre[0]-delta,centre[0]+delta),max(centre[0]-delta,centre[0]+delta))
    sinDE0=math.sin(centre[1])
    cosDE0=math.cos(centre[1])
    sortie=[]
    l = len(catalogue)
    for istar in select :
        if rayon>=math.acos(sinDE0*math.sin(catalogue[istar]['de'])+cosDE0*math.cos(catalogue[istar]['de'])*math.cos(math.fabs(centre[0]-catalogue[istar]['ra']))):
            sortie.append(istar)
    return sortie



def selection_champ_parcours_restreint(catalogue, centre, rayon):
    """
	Paramètres :
		catalogue (list): un catalogue sous forme d'une liste de dictionnaires dont les champs sont:
	        - 'nom' (str): nom de l'étoile
	        - 'ra_degres' (float): ascension droite en degrés de 0° à 360°
	        - 'de_degres' (float): déclinaison en degrés de -90° à +90°
	        - 'ra' (float): ascension droite en radians de -pi à +pi
	        - 'de' (float): déclinaison en radians de type -pi/2 à +pi/2
	        - 'mag' (float): magnitude de type float
		centre : un couple de flottants (RA0, DE0) des coordonnées en radians du centre de la zone observée
		rayon : un flottant indiquant le rayon de la zone observée
	Sortie : une liste des index des étoiles dans le catalogue donné en paramètre qui sont dans le rayon du cercle
    """
	#La plupart des catalogues sont triés approximativement selon l'ascension droite, on commence donc par trier selon RA
    sinDE0=math.sin(centre[1])
	#Le pôle nord a une déclinaison de pi/2 radians, l'ascension verticale est donc non nécessaire :
    contientPoleNord = rayon >= math.acos(sinDE0)
	#Le pôle sud a une déclinaison de -pi/2 radians donc :
    contientPoleSud = rayon >= math.acos(-sinDE0)
    if contientPoleNord and contientPoleSud :
    	return selection_champ_parcours_complet(catalogue, centre, rayon)
    elif contientPoleNord :
    	select = omg(catalogue,min(centre[1]-rayon,centre[1]+rayon),math.pi/2,-math.pi,math.pi)
    elif contientPoleSud :
    	select = omg(catalogue,-math.pi/2,max(centre[1]-rayon,centre[1]+rayon),-math.pi,math.pi)
    else :
        delta = math.asin(math.sin(rayon)/math.sin(math.pi/2 - centre[1]))
        select = omg(catalogue,min(centre[1]-rayon,centre[1]+rayon),max(centre[1]-rayon,centre[1]+rayon),min(centre[0]-delta,centre[0]+delta),max(centre[0]-delta,centre[0]+delta))
    sinDE0=math.sin(centre[1])
    cosDE0=math.cos(centre[1])
    sortie=[]
    l = len(catalogue)
    for istar in select :
        if rayon>=math.acos(sinDE0*math.sin(catalogue[istar]['de'])+cosDE0*math.cos(catalogue[istar]['de'])*math.cos(math.fabs(centre[0]-catalogue[istar]['ra']))):
            sortie.append(istar)
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

def compare_de(x,y):
	"""
    Paramètres :
	x, y : (dict) deux dictionnaires ayant tous les deux un élément de clé 'de'
	Sortie :
	-1 si x['de'] < y['de']
	0 si x['de'] == y['de']
	1 si x['de'] > y['de']
	CU : x et y ont tout les deux un élément de clé 'de'
	"""
	if x['de'] < y['de'] :
		return -1
	elif x['de'] > y['de'] :
		return 1
	else :
           return 0

def compare_ra(x,y)  :
    """
    Paramètres :
	x, y : (dict) deux dictionnaires ayant tous les deux un élément de clé 'ra'
	Sortie :
	-1 si x['ra'] < y['ra']
	0 si x['ra'] == y['ra']
	1 si x['ra'] > y['ra']
	CU : x et y ont tout les deux un élément de clé 'ra'
    """
    if x['ra'] < y['ra']:
        return -1
    elif x['ra']> y['ra']:
        return 1
    else:
        return 0

def compare_index(x,y)  :
    """
    Paramètres :
	x, y : (dict) deux dictionnaires ayant tous les deux un élément de clé 'index'
	Sortie :
	-1 si x['index'] < y['index']
	0 si x['index'] == y['index']
	1 si x['index'] > y['index']
	CU : x et y ont tout les deux un élément de clé 'index'
    """
    if x['index'] < y['index']:
        return -1
    elif x['index']> y['index']:
        return 1
    else:
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
        while k >= 1 and compare(aux, l[k - 1], cle) == -1:
            l[k] = l[k - 1]
            k = k - 1
        l[k] = aux

def trouve_inferieur(catalogue,inf,cle):
	"""
	Paramètres :
		catalogue (list): un catalogue sous forme d'une liste de dictionnaires dont les champs sont:
	        - 'nom' (str): nom de l'étoile
	        - 'ra_degres' (float): ascension droite en degrés de 0° à 360°
	        - 'de_degres' (float): déclinaison en degrés de -90° à +90°
	        - 'ra' (float): ascension droite en radians de -pi à +pi
	        - 'de' (float): déclinaison en radians de type -pi/2 à +pi/2
	        - 'mag' (float): magnitude de type float
		inf (float) : un nombre
        cle : une clé commune à tous les dictionnaires du catalogue
	Sortie : (int) Renvoie l'indice dans la liste triée du dictionnaire dont la valeur associée à cle est la plus petite étant supérieure ou égale à inf
    CU : catalogue est trié selon les valeurs associées à la clé cle dans les dictionnaires
    """
	l = len(catalogue)
	a = 0
	b = l-1
	while catalogue[a][cle] <= inf :
		m = (a+b)//2
		if catalogue[m][cle] == inf :
			return catalogue[m]['index']
		elif catalogue[m][cle] > inf :
			b = m
		else :
			a = m+1
	return a

def reduit_parcours(catalogue,inf_de,sup_de,inf_ra,sup_ra):
    """
    Paramètres :
        catalogue (list): un catalogue sous forme d'une liste de dictionnaires dont les champs sont:
        - 'nom' (str): nom de l'étoile
        - 'ra_degres' (float): ascension droite en degrés de 0° à 360°
        - 'de_degres' (float): déclinaison en degrés de -90° à +90°
        - 'ra' (float): ascension droite en radians de -pi à +pi
        - 'de' (float): déclinaison en radians de type -pi/2 à +pi/2
        - 'mag' (float): magnitude de type float
        inf_de (float) : valeur minimale de déclinaison des étoiles recherchées en radians
        inf_ra (float) : valeur minimale d'ascension verticale des étoiles recherchées en radians
        sup_de (float) : valeur maximale de déclinaison des étoiles recherchées en radians
        sup_ra (float) : valeur maximale d'ascension verticale des étoiles recherchées en radians
    Sortie : (list) une liste des index dans le catalogue des étoiles correspondant aux critères maximaux et minimaux
        de déclinaison et d'ascension verticale donnés en paramètre
    """
    from functools import cmp_to_key
    catalogue.sort(key=cmp_to_key(compare_de))
    #critères selon la déclinaison
    l = len(catalogue)
    select = []
    i_inf = trouve_inferieur(catalogue,inf_de,'de')
    while i_inf < l-1 and catalogue[i_inf]['de'] < sup_de :
        select.append(catalogue[i_inf])
        i_inf+=1
    #critères selon l'ascension verticale
    l = len(select)
    sortie = []
    select.sort(key=cmp_to_key(compare_ra))
    i_inf = trouve_inferieur(select,inf_ra,'ra')
    while i_inf < l-1 and select[i_inf]['ra'] < sup_ra :
        sortie.append(select[i_inf]['index'])
        i_inf+=1
    catalogue.sort(key=cmp_to_key(compare_index))
    return sortie

def omg(catalogue,inf_de,sup_de,inf_ra,sup_ra):
    """
    Paramètres :
        catalogue (list): un catalogue sous forme d'une liste de dictionnaires dont les champs sont:
        - 'nom' (str): nom de l'étoile
        - 'ra_degres' (float): ascension droite en degrés de 0° à 360°
        - 'de_degres' (float): déclinaison en degrés de -90° à +90°
        - 'ra' (float): ascension droite en radians de -pi à +pi
        - 'de' (float): déclinaison en radians de type -pi/2 à +pi/2
        - 'mag' (float): magnitude de type float
        inf_de (float) : valeur minimale de déclinaison des étoiles recherchéesen radians
        inf_ra (float) : valeur minimale d'ascension verticale des étoiles recherchéesen radians
        sup_de (float) : valeur maximale de déclinaison des étoiles recherchéesen radians
        sup_ra (float) : valeur maximale d'ascension verticale des étoiles recherchéesen radians
    Sortie : (list) une liste des index dans le catalogue des étoiles correspondant aux critères maximaux et minimaux
        de déclinaison et d'ascension verticale donnés en paramètre
    """
    sortie = []
    starcount = 0
    for star in catalogue :
        if inf_de<=star['de']<=sup_de and inf_ra<=star['ra']<=sup_ra :
            sortie.append(starcount)
        starcount+=1
    return sortie

def selection_omg(catalogue, centre, rayon):
    """
	Paramètres :
		catalogue (list): un catalogue sous forme d'une liste de dictionnaires dont les champs sont:
	        - 'nom' (str): nom de l'étoile
	        - 'ra_degres' (float): ascension droite en degrés de 0° à 360°
	        - 'de_degres' (float): déclinaison en degrés de -90° à +90°
	        - 'ra' (float): ascension droite en radians de -pi à +pi
	        - 'de' (float): déclinaison en radians de type -pi/2 à +pi/2
	        - 'mag' (float): magnitude de type float
		centre : un couple de flottants (RA0, DE0) des coordonnées en radians du centre de la zone observée
		rayon : un flottant indiquant le rayon de la zone observée
	Sortie : une liste des index des étoiles dans le catalogue donné en paramètre qui sont dans le rayon du cercle
    """
	#La plupart des catalogues sont triés approximativement selon l'ascension droite, on commence donc par trier selon RA
    sinDE0=math.sin(centre[1])
    cosDE0=math.cos(centre[1])
	#Le pôle nord a une déclinaison de pi/2 radians, l'ascension verticale est donc non nécessaire :
    contientPoleNord = rayon >= math.acos(sinDE0)
	#Le pôle sud a une déclinaison de -pi/2 radians donc :
    contientPoleSud = rayon >= math.acos(-sinDE0)
    sortie = []
    starcount = 0
    if contientPoleNord and contientPoleSud :
    	return selection_champ_parcours_complet(catalogue, centre, rayon)
    elif contientPoleNord :
        inf_de, sup_de, inf_ra, sup_ra = min(centre[1]-rayon,centre[1]+rayon), math.pi/2, -math.pi, math.pi
        for star in catalogue :
            if inf_de<=star['de']<=sup_de and inf_ra<=star['ra']<=sup_ra :
                if rayon>=math.acos(sinDE0*math.sin(star['de'])+cosDE0*math.cos(star['de'])*math.cos(math.fabs(centre[0]-star['ra']))):
                    sortie.append(starcount)
            starcount+=1
    elif contientPoleSud :
        inf_de, sup_de, inf_ra, sup_ra = -math.pi/2, max(centre[1]-rayon,centre[1]+rayon), -math.pi, math.pi
        for star in catalogue :
            if inf_de<=star['de']<=sup_de and inf_ra<=star['ra']<=sup_ra :
                if rayon>=math.acos(sinDE0*math.sin(star['de'])+cosDE0*math.cos(star['de'])*math.cos(math.fabs(centre[0]-star['ra']))):
                    sortie.append(starcount)
            starcount+=1
    else :
        delta = math.asin(math.sin(rayon)/math.sin(math.pi/2 - centre[1]))
        inf_de, sup_de, inf_ra, sup_ra = min(centre[1]-rayon,centre[1]+rayon), max(centre[1]-rayon,centre[1]+rayon), min(centre[0]-delta,centre[0]+delta), max(centre[0]-delta,centre[0]+delta)
        for star in catalogue :
            if inf_de<=star['de']<=sup_de and inf_ra<=star['ra']<=sup_ra :
                if rayon>=math.acos(sinDE0*math.sin(star['de'])+cosDE0*math.cos(star['de'])*math.cos(math.fabs(centre[0]-star['ra']))):
                    sortie.append(starcount)
            starcount+=1
    return sortie

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
def imprimer_carte(catalogue, centre, rayon, projection, selection,
						largeur=512, hauteur=512, nomfichier="sortiecdc.svg"):
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
    print("Impression achevée")
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
    #catalogue=charge_bright_star_5("bsc5.dat")
    catalogue=charge_henri_draper("hd.dat.gz")

    # Choix du parcours de la selection d'étoiles
    selection=selection_champ_parcours_complet
    #selection=selection_champ_parcours_restreint

    #choix de la projection
    projection=projection_equirectangulaire
    #projection=projection_aitoff
    #projection=projection_stereographic
    #projection=projection_lambert_equal_area
    if formatsortie=='csv':
        champ=selection(catalogue, centre, rayon)
        champ_vers_csv(catalogue, champ, nomfichier=sortie)
    else:
        imprimer_carte(catalogue, centre, rayon, projection, selection, 1024, 1024, nomfichier=sortie)

if __name__ == '__main__' :
    import doctest
    doctest.testmod(verbose=False)

    main()
