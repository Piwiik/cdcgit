#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 17:29:37 2017

@author: Lucky
"""

#Comment trier avec la méthode sort
#Je commence par reprendre ta fonction de comparaison mais j'en crée deux
#indépendantes du paramètre "key" :
    
def compare_de(x,y):
	"""
	"""
	if x['de'] < y['de'] :
		return -1
	elif x['de'] > y['de'] :
		return 1
	else :
           return 0
        
def compare_ra(x,y)  :
    """
    """
    if x['ra'] < y['ra']:
        return -1
    elif x['ra']> y['ra']:
        return 1
    else:
        return 0
        
#Pour trier avec .sort() :
    
"""
>>> from functools import cmp_to_key
>>> from petit_catalogue import *
>>> PETIT_CATALOGUE.sort(key=cmp_to_key(compare_de))
>>> PETIT_CATALOGUE
[{'Vmag': 1.67,
  'de': -69.71716,
  'nom': 'Miaplacidus',
  'ra': 138.29969583333335},
 {'Vmag': 1.91, 'de': -69.02773, 'nom': 'Atria', 'ra': 252.16625},
 {'Vmag': 0.77, 'de': -63.099093333333336, 'nom': 'Acrux', 'ra': 186.6495375},
 {'Vmag': -0.01,
  'de': -60.83376333333333,
  'nom': 'Rigil Kentaurus, Toliman',
  'ra': 219.89872916666667},
 {'Vmag': 0.61,
  'de': -60.373055,
  'nom': 'Hadar, Agena',
  'ra': 210.95580833333332},
 {'Vmag': 1.25, 'de': -59.68877, 'nom': 'Mimosa', 'ra': 191.93021666666667},
 {'Vmag': 1.86, 'de': -59.50949333333333, 'nom': 'Avior', 'ra': 125.6285},
 {'Vmag': 2.72,
  'de': -58.748888889,
  'nom': 'Delta Crucis',
  'ra': 183.783333333},
 {'Vmag': 0.45,
  'de': -57.236776666666664,
  'nom': 'Achernar',
  'ra': 24.428595833333333},
 {'Vmag': 1.59,
  'de': -57.113328333333335,
  'nom': 'Gacrux',
  'ra': 187.79151666666667},
 {'Vmag': 1.94,
  'de': -56.735128333333336,
  'nom': 'Peacock',
  'ra': 306.41191249999997},
 {'Vmag': 1.93,
  'de': -54.70886333333333,
  'nom': 'Delta Vel',
  'ra': 131.1759625},
 {'Vmag': -0.62, 'de': -52.69565, 'nom': 'Canopus', 'ra': 95.987975},
 {'Vmag': 1.75,
  'de': -47.33658333333333,
  'nom': 'Gamma Vel',
  'ra': 122.38312083333334},
 {'Vmag': 1.73, 'de': -46.96104, 'nom': 'Alnair', 'ra': 332.0583541666667},
 {'Vmag': 1.86, 'de': -42.997825, 'nom': 'Sargas', 'ra': 264.32970416666666},
 {'Vmag': 1.62, 'de': -37.103835, 'nom': 'Schaula', 'ra': 263.4021625},
 {'Vmag': 1.79,
  'de': -34.38467166666667,
  'nom': 'Kaus Australis',
  'ra': 276.04297083333336},
 {'Vmag': 1.17,
  'de': -29.622308333333333,
  'nom': 'Fomalhaut',
  'ra': 344.41285833333336},
 {'Vmag': 1.5,
  'de': -28.972083333333334,
  'nom': 'Adhara',
  'ra': 104.65644999999999},
 {'Vmag': 1.06,
  'de': -26.432011666666668,
  'nom': 'Antarès',
  'ra': 247.3519125},
 {'Vmag': 1.83, 'de': -26.393198333333334, 'nom': 'Wezen', 'ra': 107.09785},
 {'Vmag': 1.98, 'de': -17.955916666666667, 'nom': 'Mirzam', 'ra': 95.6749375},
 {'Vmag': -1.44, 'de': -16.716656666666665, 'nom': 'Sirius', 'ra': 101.2869},
 {'Vmag': 0.98, 'de': -11.161335, 'nom': 'Spica', 'ra': 201.298225},
 {'Vmag': 2.06, 'de': -9.669444444, 'nom': 'Saiph', 'ra': 86.9375},
 {'Vmag': 1.99, 'de': -8.658588333333334, 'nom': 'Alphard', 'ra': 141.8968375},
 {'Vmag': 0.18, 'de': -8.20164, 'nom': 'Rigel', 'ra': 78.63446666666667},
 {'Vmag': 1.74, 'de': -1.94257, 'nom': 'Alnitak', 'ra': 85.18969583333333},
 {'Vmag': 1.69, 'de': -1.2019199999999999, 'nom': 'Alnilam', 'ra': 84.0533875},
 {'Vmag': 2.23, 'de': -0.29888888889, 'nom': 'Mintaka', 'ra': 83.0},
 {'Vmag': 0.4, 'de': 5.224535, 'nom': 'Procyon', 'ra': 114.825175},
 {'Vmag': 1.64, 'de': 6.349695, 'nom': 'Bellatrix', 'ra': 81.28275833333333},
 {'Vmag': 0.45, 'de': 7.407066666666666, 'nom': 'Bételgeuse', 'ra': 88.79295},
 {'Vmag': 0.76,
  'de': 8.868491666666667,
  'nom': 'Altair',
  'ra': 297.69606666666664},
 {'Vmag': 1.36, 'de': 11.967208333333334, 'nom': 'Régulus', 'ra': 152.09285},
 {'Vmag': 1.93,
  'de': 16.399221666666666,
  'nom': 'Alhena',
  'ra': 99.42791666666666},
 {'Vmag': 0.87,
  'de': 16.509218333333333,
  'nom': 'Aldébaran',
  'ra': 68.9801875},
 {'Vmag': -0.05,
  'de': 19.181528333333333,
  'nom': 'Arcturus',
  'ra': 213.9147875},
 {'Vmag': 1.16, 'de': 28.02618, 'nom': 'Pollux', 'ra': 116.32864583333333},
 {'Vmag': 1.65,
  'de': 28.607371666666666,
  'nom': 'El Nath',
  'ra': 81.57298333333334},
 {'Vmag': 1.58, 'de': 31.88817, 'nom': 'Castor', 'ra': 113.64934166666667},
 {'Vmag': 0.03,
  'de': 38.783818333333336,
  'nom': 'Véga',
  'ra': 279.23484583333334},
 {'Vmag': 1.9,
  'de': 44.94743166666667,
  'nom': 'Menkalinan',
  'ra': 89.88214166666667},
 {'Vmag': 1.25,
  'de': 45.28033833333333,
  'nom': 'Deneb',
  'ra': 310.35797916666667},
 {'Vmag': 0.08, 'de': 45.99780166666667, 'nom': 'Capella', 'ra': 79.172375},
 {'Vmag': 1.85, 'de': 49.31325833333333, 'nom': 'Alkaid', 'ra': 206.885075},
 {'Vmag': 1.79, 'de': 49.86116833333333, 'nom': 'Mirfak', 'ra': 51.080725},
 {'Vmag': 2.4, 'de': 53.694722222, 'nom': 'Phecda', 'ra': 178.454166667},
 {'Vmag': 2.22, 'de': 54.925277778, 'nom': 'Mizar', 'ra': 200.979166667},
 {'Vmag': 1.76, 'de': 55.95981666666667, 'nom': 'Alioth', 'ra': 193.507375},
 {'Vmag': 2.35, 'de': 56.382222222, 'nom': 'Merak', 'ra': 165.458333333},
 {'Vmag': 3.3, 'de': 57.0325, 'nom': 'Megrez', 'ra': 183.854166667},
 {'Vmag': 1.81, 'de': 61.751018333333334, 'nom': 'Dubhe', 'ra': 165.9318},
 {'Vmag': 1.97, 'de': 89.264105, 'nom': 'Polaris', 'ra': 37.95605}]
 """
 
 #Voilà ! La méthode .sort est normalement plus efficace que le tri par insertion
 