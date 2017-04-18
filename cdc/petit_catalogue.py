#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
:mod: petit_catalogue

:author: Jean-Luc Levaire

:date: 2017, march

Définition d'un petit catalogue sous forme d'une liste d'étoiles.
Chaque étoile de la liste est un dictionnaire dont les champs sont:
 - 'nom' (str): nom de l'étoile
 - 'ra' (float): ascension droite en degrés de 0° à 360°
 - 'de' (float): déclinaison en degrés de -90° à +90°
 - 'Vmag' (float): magnitude apparente
"""


PETIT_CATALOGUE=[
{'ra': 101.2869, 'Vmag': -1.44, 'nom': 'Sirius', 'de': -16.716656666666665},
{'ra': 95.987975, 'Vmag': -0.62, 'nom': 'Canopus', 'de': -52.69565},
{'ra': 213.9147875, 'Vmag': -0.05, 'nom': 'Arcturus', 'de': 19.181528333333333},
{'ra': 219.89872916666667, 'Vmag': -0.01, 'nom': 'Rigil Kentaurus, Toliman', 'de': -60.83376333333333},
{'ra': 279.23484583333334, 'Vmag': 0.03, 'nom': 'Véga', 'de': 38.783818333333336},
{'ra': 79.172375, 'Vmag': 0.08, 'nom': 'Capella', 'de': 45.99780166666667},
{'ra': 78.63446666666667, 'Vmag': 0.18, 'nom': 'Rigel', 'de': -8.20164},
{'ra': 114.825175, 'Vmag': 0.4, 'nom': 'Procyon', 'de': 5.224535},
{'ra': 24.428595833333333, 'Vmag': 0.45, 'nom': 'Achernar', 'de': -57.236776666666664},
{'ra': 88.79295, 'Vmag': 0.45, 'nom': 'Bételgeuse', 'de': 7.407066666666666},
{'ra': 210.95580833333332, 'Vmag': 0.61, 'nom': 'Hadar, Agena', 'de': -60.373055},
{'ra': 297.69606666666664, 'Vmag': 0.76, 'nom': 'Altair', 'de': 8.868491666666667},
{'ra': 186.6495375, 'Vmag': 0.77, 'nom': 'Acrux', 'de': -63.099093333333336},
{'ra': 68.9801875, 'Vmag': 0.87, 'nom': 'Aldébaran', 'de': 16.509218333333333},
{'ra': 201.298225, 'Vmag': 0.98, 'nom': 'Spica', 'de': -11.161335},
{'ra': 247.3519125, 'Vmag': 1.06, 'nom': 'Antarès', 'de': -26.432011666666668},
{'ra': 116.32864583333333, 'Vmag': 1.16, 'nom': 'Pollux', 'de': 28.02618},
{'ra': 344.41285833333336, 'Vmag': 1.17, 'nom': 'Fomalhaut', 'de': -29.622308333333333},
{'ra': 191.93021666666667, 'Vmag': 1.25, 'nom': 'Mimosa', 'de': -59.68877},
{'ra': 310.35797916666667, 'Vmag': 1.25, 'nom': 'Deneb', 'de': 45.28033833333333},
{'ra': 152.09285, 'Vmag': 1.36, 'nom': 'Régulus', 'de': 11.967208333333334},
{'ra': 104.65644999999999, 'Vmag': 1.5, 'nom': 'Adhara', 'de': -28.972083333333334},
{'ra': 113.64934166666667, 'Vmag': 1.58, 'nom': 'Castor', 'de': 31.88817},
{'ra': 187.79151666666667, 'Vmag': 1.59, 'nom': 'Gacrux', 'de': -57.113328333333335},
{'ra': 263.4021625, 'Vmag': 1.62, 'nom': 'Schaula', 'de': -37.103835},
{'ra': 81.28275833333333, 'Vmag': 1.64, 'nom': 'Bellatrix', 'de': 6.349695},
{'ra': 81.57298333333334, 'Vmag': 1.65, 'nom': 'El Nath', 'de': 28.607371666666666},
{'ra': 138.29969583333335, 'Vmag': 1.67, 'nom': 'Miaplacidus', 'de': -69.71716},
{'ra': 84.0533875, 'Vmag': 1.69, 'nom': 'Alnilam', 'de': -1.2019199999999999},
{'ra': 332.0583541666667, 'Vmag': 1.73, 'nom': 'Alnair', 'de': -46.96104},
{'ra': 85.18969583333333, 'Vmag': 1.74, 'nom': 'Alnitak', 'de': -1.94257},
{'ra': 122.38312083333334, 'Vmag': 1.75, 'nom': 'Gamma Vel', 'de': -47.33658333333333},
{'ra': 193.507375, 'Vmag': 1.76, 'nom': 'Alioth', 'de': 55.95981666666667},
{'ra': 276.04297083333336, 'Vmag': 1.79, 'nom': 'Kaus Australis', 'de': -34.38467166666667},
{'ra': 51.080725, 'Vmag': 1.79, 'nom': 'Mirfak', 'de': 49.86116833333333},
{'ra': 165.9318, 'Vmag': 1.81, 'nom': 'Dubhe', 'de': 61.751018333333334},
{'ra': 107.09785, 'Vmag': 1.83, 'nom': 'Wezen', 'de': -26.393198333333334},
{'ra': 206.885075, 'Vmag': 1.85, 'nom': 'Alkaid', 'de': 49.31325833333333},
{'ra': 264.32970416666666, 'Vmag': 1.86, 'nom': 'Sargas', 'de': -42.997825},
{'ra': 125.6285, 'Vmag': 1.86, 'nom': 'Avior', 'de': -59.50949333333333},
{'ra': 89.88214166666667, 'Vmag': 1.9, 'nom': 'Menkalinan', 'de': 44.94743166666667},
{'ra': 252.16625, 'Vmag': 1.91, 'nom': 'Atria', 'de': -69.02773},
{'ra': 131.1759625, 'Vmag': 1.93, 'nom': 'Delta Vel', 'de': -54.70886333333333},
{'ra': 99.42791666666666, 'Vmag': 1.93, 'nom': 'Alhena', 'de': 16.399221666666666},
{'ra': 306.41191249999997, 'Vmag': 1.94, 'nom': 'Peacock', 'de': -56.735128333333336},
{'ra': 37.95605, 'Vmag': 1.97, 'nom': 'Polaris', 'de': 89.264105},
{'ra': 95.6749375, 'Vmag': 1.98, 'nom': 'Mirzam', 'de': -17.955916666666667},
{'ra': 141.8968375, 'Vmag': 1.99, 'nom': 'Alphard', 'de': -8.658588333333334},
{'ra': 83.0, 'Vmag': 2.23, 'nom': 'Mintaka', 'de': -0.29888888889},
{'ra': 86.9375, 'Vmag': 2.06, 'nom': 'Saiph', 'de': -9.669444444},
{'ra': 165.458333333, 'Vmag': 2.35, 'nom': 'Merak', 'de': 56.382222222},
{'ra': 178.454166667, 'Vmag': 2.40, 'nom': 'Phecda', 'de': 53.694722222},
{'ra': 183.854166667, 'Vmag': 3.30, 'nom': 'Megrez', 'de': 57.0325},
{'ra': 200.979166667, 'Vmag': 2.22, 'nom': 'Mizar', 'de': 54.925277778},
{'ra': 183.783333333, 'Vmag': 2.72, 'nom': 'Delta Crucis', 'de': -58.748888889},
]
