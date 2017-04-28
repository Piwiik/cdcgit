#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
:mod: cdc_gr

:author: Jean-Luc Levaire

:date: 2017, march

Programme interactif de dessin de cartes du ciel. Permet de déplacer le centre
de la carte avec le bouton 1 de la souris, de zoomer avec la roulette, et d'afficher
des informations sur une étoile en cliquant dessus avec le bouton 3.
On peut également sélectionner un catalogue, une fonction de calcul du champ (selection),
et une fonction de projection de la sphère dans le plan.
CONTRAINTE: Utilise le module cdc.py en supposant que les focntions de chargement des catalogues
renvoient une liste d'étoiles. Chaque étoile doit être un dictionnaire possédant au moins un champ
'nom' de type str, un champ 'ra' et 'de' de type float contenant respectivement l'ascension droite
et la déclinaison de l'étoile en radians, et un champ 'mag' de type float contenant la magnitude
de l'étoile.
NOTE: Décommentez/ajoutez dans les dictionnaires définissant les menus, les catalogues et projections
que vous aurez implémentés.
"""

import tkinter
import math

### MODULE CDC ###
import cdc

### DICTIONNAIRES DEFINISSANT LES MENUS ###
# pour les catalogues, la valeur associée à une entrée est un couple (fonction, paramètre)
import petit_catalogue
catalogues={'Petit Catalogue': (cdc.charge_petit_catalogue, petit_catalogue.PETIT_CATALOGUE),
            'Bright Star Catalog': (cdc.charge_bright_star_5, 'bsc5.dat'),
            'Henri Draper Catalog': (cdc.charge_henri_draper, 'hd.dat.gz'),
            'Hipparcos Catalog': (cdc.charge_hipparcos, 'hip2.dat.gz')
            }
# pour les sélections et projections, la valeur associée est le nom de la fonction à appeler
# les sélections sont appelées avec les paramètres catalogue, centre et rayon
# et doivent renvoyer une liste d'index dans le catalogue des étoiles sélectionnées
selections={'Parcours Complet': cdc.selection_champ_parcours_complet,
            'Parcours Restreint': cdc.selection_champ_parcours_restreint,
            'Parcours OMG du batard': cdc.selection_omg,
            'Parcours Nouveau': cdc.nouveau_parcours_restreint
            }
# les projections sont appelées avec un paramètre point qui est un couple de flottants,
# et doivent renvoyer le point projeté sous forme d'un couple de flottants
projections={'Equirectangulaire': cdc.projection_equirectangulaire,
             'Aitoff': cdc.projection_aitoff,
             'Stéréographique': cdc.projection_stereographic,
             'Equivalente de Lambert': cdc.projection_lambert_equal_area
             }

# TAILLE DE LA ZONE DE DESSIN
LARGEUR=800
HAUTEUR=600

# PARAMETRES DE LA CARTE EN COURS DE DESSIN
catalogue=None
centre=None
rayon=None
selection=None
projection=None
echelle=None

### ELEMENTS GRAPHIQUES ###
mainwin=None
settingswin=None
leftframe=None
infowin=None
buttonwin=None
canvas=None
pxpyvalues=None
xyvalues=None
centreravalue=None
centredevalue=None
centreradvalues=None
rayonvalues=None
echellevalues=None
catalogvalue=None
selectionvalue=None
projectionvalue=None
largeur=0
hauteur=0
pxorig, pyorig = 0, 0
init=False

### INTERACTIONS ###
# infos
def rad_vers_hms(rad):
    """
Conversion de radians en heures, minutes, secondes.
- rad (float): valeur de l'angle à convertir en radians
Valeur renvoyée (int, int, float): triplet heure, minutes et secondes
CU: aucune
    """
    assert -math.pi <= rad <= (2.0 * math.pi)
    if rad < 0:
        rad += (2.0 * math.pi)
    rh=(rad * 24.0 / (2.0 * math.pi))
    h=math.floor(rh)
    rm = (rh - h) * 60.0
    m=math.floor(rm)
    s = (rm - m) * 60.0
    return (h, m , s)

def rad_vers_dms(rad):
    """
Conversion de radians en degrés, minutes d'arc, secondes d'arc.
- rad (float): valeur de l'angle à convertir en radians
Valeur renvoyée (int, int, float): triplet degrés, minutes d'arc et secondes d'arc
CU: aucune
    """
    rd=(rad * 360.0 / (2.0 * math.pi))
    d=math.trunc(rd)
    rm = abs(rd - d) * 60.0
    m=math.trunc(rm)
    s = (rm - m) * 60.0
    return (d, m , s)

def callback_centre_update():
    global centre, centreravalue, centredevalue, centreradvalues
    rahms=rad_vers_hms(centre[0])
    dedms=rad_vers_dms(centre[1])
    rastr='{0[0]:02d}h{0[1]:02d}m{0[2]:04.1f}s'.format(rahms)
    destr='{0[0]:03d}°{0[1]:02d}\'{0[2]:04.1f}"'.format(dedms)
    centreravalue.set(rastr)
    centredevalue.set(destr)
    centreradvalues.set('({: >+6.4f}, {: >+6.4f})'.format(centre[0], centre[1]))
def callback_rayon_update():
    global rayon, rayonvalues
    rayonstr='{0[0]:03d}°{0[1]:02d}\'{0[2]:04.1f}"'.format(rad_vers_dms(rayon))
    rayonvalues.set(rayonstr)
    #rayonvalues.set(' ({: >+8.6f})'.format(rayon)) # en radians
# menus
def callback_menu_catalog(e, f, g):
    global catalogvalue, catalogue, init
    print('Chargement du catalogue '+catalogvalue.get())
    charge, arg =  catalogues[catalogvalue.get()]
    catalogue=charge(arg)
    if init: rafraichir_carte()
def callback_menu_selection(e, f, g):
    global selectionvalue, selection, init
    print('Choix de sélection: '+selectionvalue.get())
    selection =  selections[selectionvalue.get()]
    if init: rafraichir_carte()
def callback_menu_projection(e, f, g):
    global projectionvalue, projection, init
    print('Choix de projection: '+projectionvalue.get())
    projection =  projections[projectionvalue.get()]
    if init: rafraichir_carte()
# buttons
def callback_imprimer_carte():
    global catalogue, centre, rayon, projection, selection
    cdc.imprimer_carte(catalogue, centre, rayon, projection, selection, 1440, 720)

def callback_exporter_csv():
    global catalogue, centre, rayon, selection
    champ=selection(catalogue, centre, rayon)
    cdc.champ_vers_csv(catalogue, champ)

# Souris
# motion
def callback_motion(e):
    global echelle, largeur, hauteur, pxpyvalues, xyvalues
    pxpyvalues.set('('+str(e.x)+','+str(e.y)+')')
    x=((largeur/2) - e.x)/echelle
    y=((hauteur/2) - e.y)/echelle
    xyvalues.set('({: >+6.4f}, {: >+6.4f})'.format(x, y))
# button1: change le centre
def callback_button1(e):
    global canvas, pxorig, pyorig
    canvas.delete('texte_etoile')
    canvas.config(cursor='fleur')
    canvas.update_idletasks()
    pxorig, pyorig=e.x, e.y
def callback_releasebutton1(e):
    global centre, echelle, rayon
    deltax, deltay = e.x-pxorig, e.y-pyorig
    #print(deltax, deltay)
    ra0, de0 = centre
    ra0+=deltax/echelle
    de0+=deltay/echelle
    ra0=((ra0 + math.pi) % (2.0*math.pi)) - math.pi
    if de0 > (math.pi / 2.0):
        de0 = math.pi - de0
        ra0 = -ra0
    elif de0 < -(math.pi / 2.0):
        de0 = - math.pi  - de0
        ra0 = -ra0
    centre=(ra0, de0)
    callback_centre_update()
    canvas.config(cursor='tcross')
    rafraichir_carte()
#molette/button2: change le rayon de la zone (zoome/dézoome)
def callback_button4(e):
    global rayon, echelle, projection, largeur, hauteur
    canvas.delete('texte_etoile')
    canvas.update_idletasks()
    rayon=rayon/math.sqrt(2)
    if rayon < math.pi/(180.0*3600.0)*10: # 10 arcsec
        rayon = math.pi/(180.0*3600.0)*10
    #print('nouveau rayon:', rayon)
    callback_rayon_update()
    rafraichir_carte()
def callback_button5(e):
    global rayon, echelle, projection, largeur, hauteur
    canvas.delete('texte_etoile')
    canvas.update_idletasks()
    rayon=rayon*math.sqrt(2)
    if rayon > math.pi:
        rayon=math.pi
    #print('nouveau rayon:', rayon)
    callback_rayon_update()
    rafraichir_carte()
# Pour Windows/MacOS
def callback_mousewheel(e):
    #print(e.delta)
    if e.delta <= 0:
        callback_button5(e)
    else:
        callback_button4(e)
#button3: affiche le nom de l'étoile cliquée
def callback_etoile_button3(e):
    c=e.widget
    x, y = e.x, e.y
    #print('button3', x, y)
    if c.find_withtag(tkinter.CURRENT):
        tags=c.gettags(tkinter.CURRENT)
        anchor='sw'
        if y < 15:
            anchor='nw'
        if x > c.winfo_reqwidth() - 150.0:
            anchor=anchor[0]+'e'
        texte_item=c.create_text((x,y), anchor=anchor, text=tags[1], tags='texte_etoile')
        rect_item=c.create_rectangle(c.bbox(texte_item), fill='white', tags='texte_etoile')
        c.tag_lower(rect_item, texte_item)
        c.update_idletasks()
        c.tag_bind(tkinter.CURRENT, '<ButtonRelease-3>', callback_etoile_buttonrelease3)
def callback_etoile_buttonrelease3(e):
    c=e.widget
    #print('buttonrelease3', e.x, e.y)
    c.delete('texte_etoile')
    c.update_idletasks()
    c.tag_unbind(tkinter.CURRENT, '<ButtonRelease-3>')

### FONCTIONS DE DESSIN ###
def effacer_carte():
    """
Efface la zone de dessin, et donc la carte courante.
Valeur renvoyée: aucune
CU: aucune
    """
    global canvas
    canvas.delete(tkinter.ALL)
    canvas.update_idletasks()

def rafraichir_carte():
    """
Réaffiche la zone de dessin en redessinant la carte.
Lie également le bouton 3 de la souris avec l'affichage du nom des étoiles.
Valeur renvoyée: aucune
CU: aucune
    """
    global canvas, echelle, echellevalues
    effacer_carte()
    dessiner_carte()
    canvas.tag_bind('etoile', '<Button-3>', callback_etoile_button3)
    echellevalues.set('{: >+6.2f}'.format(echelle))

def dessiner_etoile(point, diametre=2, tags=None):
    """
Dessine une étoile dans la zone de dessin. L'étoile est représentée par un cercle
de diamètre diametre dont le centre est aux coordonnées point dans la zone de dessin.
 - point (int, int): couple (px, py) des coordonnées du centre de l'étoile
 - diametre (int): diamètre du cercle à dessiner
 - tags (object): étiquette servant à afficher le nom de l'étoile à l'aide du bouton 3 de la souris
                  (passer le nom de l'étoile comme valeur)
Valeur renvoyée: None
CU: aucune
    """
    global canvas
    x, y = point
    radiusm=diametre//2
    radiusp=diametre//2 - 1 if diametre % 2 == 0 else diametre // 2
    e=canvas.create_oval(x-radiusm, y-radiusm, x+radiusp, y+radiusp, fill='black', tags='etoile')
    if tags is not None:
        canvas.addtag_withtag(tags, e)

def dessiner_carte():
    """
Dessine la carte de la zone observée. Le dessin se fait à partir des valeurs courantes
des variables globales catalogue, centre, rayon, projection, selection, largeur et hauteur.
Valeur renvoyée: aucune
CU: aucune
    """
    global catalogue, centre, rayon, projection, selection, largeur, hauteur, echelle
    champ=selection(catalogue, centre, rayon)
    echelle = cdc.echelle_projection(projection, rayon, largeur, hauteur)
    for index in champ:
        etoile=catalogue[index]
        ra = etoile['ra']
        de = etoile['de']
        ra_centre, de_centre = cdc.changement_de_repere((ra, de), centre)
        x, y = projection((ra_centre, de_centre))
        # en astronomie, l'axe ra est inversé, d'où le -x
        px = (-x * echelle) + (largeur / 2)
        # l'axe des py dans tk est inversé, d'où le -y
        py = (-y * echelle) + (hauteur/2)
        dessiner_etoile((px, py), tags=etoile['nom'], diametre=max((6-math.floor(etoile['mag'])), 1))



### PROGRAMME PRINCIPAL ###
def main():
    global mainwin, canvas
    global pxpyvalues, xyvalues, centreravalue, centredevalue, centreradvalues
    global rayonvalues, echellevalues
    global catalogvalue, selectionvalue, projectionvalue
    global largeur, hauteur
    global leftframe, infowin, settingswin
    global centre, rayon
    global init
    mainwin=tkinter.Tk()
    mainwin.title("Carte du ciel")
    largeur=LARGEUR
    hauteur=HAUTEUR
    leftframe=tkinter.Frame(mainwin)
    settingswin=tkinter.LabelFrame(leftframe,text='Préférences')
    infowin=tkinter.LabelFrame(leftframe,text='Infos')
    buttonwin=tkinter.LabelFrame(leftframe,text='Actions')
    settingswin.pack(fill='x', expand=1)
    infowin.pack(fill='y', expand=1)
    buttonwin.pack(fill='x', expand=1)
    leftframe.pack(side='left', fill='y', expand=0)
    # canvas
    canvas=tkinter.Canvas(master=mainwin,width=LARGEUR, height=HAUTEUR, bg='white')
    canvas.config(scrollregion=canvas.bbox(tkinter.ALL), cursor='tcross')
    canvas.pack(fill='both', expand=1, side='left')
    #settingswin
    catalogvalue=tkinter.StringVar()
    catalogvalue.trace('w', callback_menu_catalog)
    cnames=list(catalogues.keys())
    cnames.sort()
    optionmenu_catalog=tkinter.OptionMenu(settingswin, catalogvalue, *cnames)
    catalogvalue.set(cnames[0])
    optionmenu_catalog.pack(fill='x', expand=1)
    selectionvalue=tkinter.StringVar()
    selectionvalue.trace('w', callback_menu_selection)
    snames=list(selections.keys())
    snames.sort()
    optionmenu_selection=tkinter.OptionMenu(settingswin, selectionvalue, *snames)
    selectionvalue.set(snames[0])
    optionmenu_selection.pack(fill='x', expand=1)
    projectionvalue=tkinter.StringVar()
    projectionvalue.trace('w', callback_menu_projection)
    pnames=list(projections.keys())
    pnames.sort()
    optionmenu_projection=tkinter.OptionMenu(settingswin, projectionvalue, *pnames)
    projectionvalue.set(pnames[0])
    optionmenu_projection.pack(fill='x', expand=1)
    # infowin
    #(px, py)
    label_pxpy= tkinter.Label(infowin, text='(px, py): ')
    label_pxpy.grid(row=0, column=0, sticky=tkinter.E)
    pxpyvalues=tkinter.StringVar()
    pxpyvalues.set('(----,----)')
    label_pxpyvalues= tkinter.Label(infowin, textvariable=pxpyvalues)
    label_pxpyvalues.grid(row=0, column=1, sticky=tkinter.W)
    #(x, y)
    label_xy= tkinter.Label(infowin, text='(x, y): ')
    label_xy.grid(row=1, column=0, sticky=tkinter.E)
    xyvalues=tkinter.StringVar()
    xyvalues.set('(----,----)')
    label_xyvalues= tkinter.Label(infowin, textvariable=xyvalues)
    label_xyvalues.grid(row=1, column=1, sticky=tkinter.W)
    #Centre
    label_centre= tkinter.Label(infowin, text='Centre: ')
    label_centre.grid(row=2, column=0, sticky=tkinter.E)
    centreradvalues=tkinter.StringVar()
    centreradvalues.set('(----, ----)')
    label_centreradvalues= tkinter.Label(infowin, textvariable=centreradvalues)
    label_centreradvalues.grid(row=2, column=1, sticky=tkinter.W)
    tkinter.Label(infowin, text='ra0:').grid(row=3, column=0, sticky=tkinter.E)
    centreravalue=tkinter.StringVar()
    centreravalue.set('----')
    label_centreravalue= tkinter.Label(infowin, textvariable=centreravalue)
    label_centreravalue.grid(row=3, column=1, sticky=tkinter.W)
    tkinter.Label(infowin, text='de0:').grid(row=4, column=0, sticky=tkinter.E)
    centredevalue=tkinter.StringVar()
    centredevalue.set('----')
    label_centredevalue= tkinter.Label(infowin, textvariable=centredevalue)
    label_centredevalue.grid(row=4, column=1, sticky=tkinter.W)
    #rayon
    label_rayon= tkinter.Label(infowin, text='Rayon: ')
    label_rayon.grid(row=5, column=0, sticky=tkinter.E)
    rayonvalues=tkinter.StringVar()
    rayonvalues.set('------')
    label_rayonvalues= tkinter.Label(infowin, textvariable=rayonvalues)
    label_rayonvalues.grid(row=5, column=1, sticky=tkinter.W)
    #echelle
    label_echelle= tkinter.Label(infowin, text='Echelle: ')
    label_echelle.grid(row=6, column=0, sticky=tkinter.E)
    echellevalues=tkinter.StringVar()
    echellevalues.set('------')
    label_echellevalues= tkinter.Label(infowin, textvariable=echellevalues)
    label_echellevalues.grid(row=6, column=1, sticky=tkinter.W)
    #buttonwin
    button_exporter= tkinter.Button(buttonwin,text="Exporter csv",command=callback_exporter_csv)
    button_exporter.pack(fill='x', expand=1)
    button_imprimer= tkinter.Button(buttonwin,text="Imprimer",command=callback_imprimer_carte)
    button_imprimer.pack(fill='x', expand=1)
    button_quit= tkinter.Button(buttonwin,text="Quitter",command=mainwin.destroy)
    button_quit.pack(fill='x', expand=1)
    #bindings
    canvas.bind('<Motion>', callback_motion)
    canvas.bind('<Button-1>', callback_button1)
    canvas.bind('<ButtonRelease-1>', callback_releasebutton1)
    canvas.bind('<Button-4>', callback_button4)
    canvas.bind('<Button-5>', callback_button5)
    canvas.bind('<MouseWheel>', callback_mousewheel)
    # dessin initial
    # centre: sur le point vernal
    centre=(0.0, 0.0)
    callback_centre_update()
    # rayon: toute la sphère
    rayon=math.pi
    callback_rayon_update()
    rafraichir_carte()

    #boucle principale
    init=True
    mainwin.winfo_toplevel().resizable(width=False, height=False)
    mainwin.mainloop()

if __name__ == '__main__':
    import doctest
    doctest.testmod ()

    main ()
