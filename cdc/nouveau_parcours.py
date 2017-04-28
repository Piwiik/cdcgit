###Nouveau Parcours
### En gros , au chargement du catalogue, on crée des listes d'indices des étoiles
### Triées selon de et ra, ce sont des variables globales que l'on modifie au chargement du catalogue
### Nouveau catalogue à remplacer dans cdc_gr :
"""
catalogues={'Petit Catalogue': (cdc.charge_petit_catalogue, petit_catalogue.PETIT_CATALOGUE),
            'Bright Star Catalog': (cdc.charge_bright_star_5, 'bsc5.dat'),
            'Henri Draper Catalog': (cdc.charge_henri_draper, 'hd.dat.gz'),
            'Hipparcos Catalog': (cdc.charge_hipparcos, 'hip2.dat.gz')
            }
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
    Renvoie la liste des indices de étoiles triées selon le RA
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

### SELECTION

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
