import pygame
from value import *



#--- Fonctions
def position_horizontale_rel(rect):
    if balle_position[H] < rect[0][H]:
        return GAUCHE
    elif balle_position[H] > rect[0][H] + rect[1][H]:
        return DROITE
    else:
        return CENTRE

def position_verticale_rel(rect):
    if balle_position[V] < rect[0][V]:
        return HAUT
    elif balle_position[V] > rect[0][V] + rect[1][V]:
        return BAS
    else:
        return CENTRE

def position_relative(rect):
    return position_horizontale_rel(rect) + position_verticale_rel(rect)

def distance2(pt1, pt2):
    delta_h = pt1[H] - pt2[H]
    delta_v = pt1[V] - pt2[V]
    return delta_h * delta_h + delta_v * delta_v

def resoudre_collision_coin(coin, delta_h, delta_v, vitesse_h, vitesse_v):
    balle_position[H] = coin[H] + delta_h
    balle_position[V] = coin[V] + delta_v
    balle_vitesse[H] = vitesse_h
    balle_vitesse[V] = vitesse_v

def collision_coin_haut_gauche(rect):
    delta = round(BALLE_RAYON * 0.707)
    resoudre_collision_coin(rect[0], -delta, -delta, -abs(balle_vitesse[H]), -abs(balle_vitesse[V]))

def collision_coin_haut_droite(rect):
    delta = round(BALLE_RAYON * 0.707)
    resoudre_collision_coin((rect[0][H], rect[1][H], rect[0][V]), delta, -delta, abs(balle_vitesse[H]), abs(balle_vitesse[V]))

def collision_coin_bas_gauche(rect):
    delta = round(BALLE_RAYON * 0.707)
    resoudre_collision_coin((rect[0][H] +  rect[1][H], rect[0][V]), -delta, delta, -abs(balle_vitesse[H]), abs(balle_vitesse[V]))

def collision_coin_bas_droite(rect):
    delta = round(BALLE_RAYON * 0.707)
    resoudre_collision_coin((rect[0][H] + rect[1][H], rect[0][V] + rect[1][V]), delta, delta, abs(balle_vitesse[H]), abs(balle_vitesse[V]))

def deplace_raquette(sens):
    raquette_position[H] += RAQUETTE_DEPLACEMENT * sens
    test_touche_droite(raquette_position, RAQUETTE_LARGEUR,FENETRE_LARGEUR)
    test_touche_gauche(raquette_position, 0, 0)

def test_collision(rect):
    ball_rect = pygame.Rect((balle_position[H] - BALLE_RAYON, balle_position[V] - BALLE_RAYON),(BALLE_DIAM, BALLE_DIAM))
    rayon2 = BALLE_RAYON * BALLE_RAYON
    if ball_rect.colliderect(rect):
        position = position_relative(rect)
        if position == GAUCHE:
            if test_touche_droite(balle_position, BALLE_RAYON, rect[0][H]):
                balle_vitesse[H] = -abs(balle_vitesse[H])
        elif position == DROITE:
            if test_touche_gauche(balle_position, BALLE_RAYON, rect[0][H] + rect[1][H]):
                balle_vitesse[H] = abs(balle_vitesse[H])
        elif position ==  HAUT:
            if test_touche_bas(balle_position, BALLE_RAYON, rect[0][V]):
                balle_vitesse[V] = -balle_vitesse[V]
        elif position == BAS:
            if test_touche_haut(balle_position, BALLE_RAYON, rect[0][V] + rect[1][V]):
                balle_vitesse[V] = -balle_vitesse[V]
        elif position == HAUT_GAUCHE:
            if distance2(balle_position, rect[0]) <= rayon2:
                collision_coin_haut_gauche(rect)
        elif position == HAUT_DROITE:
            if distance2(balle_position, (rect[0][H] + rect[1][H], rect[0][V])) <= rayon2:
                collision_coin_haut_droite(rect)
        elif position == BAS_GAUCHE:
            if distance2(balle_position, (rect[0][H], rect[0][V] + rect[1][V])) <= rayon2:
                collision_coin_bas_gauche(rect)
        elif position == BAS_DROITE:
            if distance2(balle_position, (rect[0][H] + rect[1][H], rect[0][V] + rect[1][V])) <= rayon2:
                collision_coin_bas_droite(rect)
        else:
            delta_g = abs(balle_position[H] - rect[0][H])
            delta_d = abs(balle_position[H] - rect[0][H] - rect[1][H])
            if delta_g < delta_d:
                balle_position[H] = rect[0][H] - BALLE_RAYON
                balle_vitesse[H] = -abs(balle_vitesse[H])
            else:
                balle_position[H] = rect[0][H] + rect[1][H] + BALLE_RAYON
                balle_vitesse[H] = abs(balle_vitesse[H])

def test_touche_gh(objet, distance, point, direction, separe):
    if objet[direction] - distance <= point:
        if separe:
            objet[direction] = point + distance
        return True
    else:
        return False

def test_touche_db(objet, distance, point, direction, separe):
    if objet[direction] + distance >= point:
        if separe:
            objet[direction] = point - distance
        return True
    else:
        return False

def test_touche_droite(objet, largeur_droite, point_droit, separe=True):
    return test_touche_db(objet, largeur_droite, point_droit, H, separe)
    
def test_touche_gauche(objet, largeur_gauche, point_gauche, separe = True):
    return test_touche_gh(objet, largeur_gauche, point_gauche, H, separe)

def test_touche_haut(objet, hauteur_haut, point_haut, separe = True):
    return test_touche_gh(objet, hauteur_haut, point_haut, V, separe)

def test_touche_bas(objet, hauteur_bas, point_bas, separe = True):
    return test_touche_db(objet, hauteur_bas, point_bas, V, separe)

def traite_entrees():

    global fini
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            fini = True
        elif evenement.type == pygame.KEYDOWN:
            if evenement.key == TOUCHE_DROITE:
                deplace_raquette(VERS_DROITE)
            if evenement.key == TOUCHE_GAUCHE:
                deplace_raquette(VERS_GAUCHE)

def anime():
    global fini
    balle_position[H] = balle_position[H] + balle_vitesse[H]
    balle_position[V] = balle_position[V] + balle_vitesse[V]


    if test_touche_droite(balle_position, BALLE_RAYON, FENETRE_LARGEUR - MUR_EPAISSEUR) \
       or test_touche_gauche(balle_position, BALLE_RAYON, 0):
        balle_vitesse[H] = -balle_vitesse[H]

    if test_touche_haut(balle_position, BALLE_RAYON, MUR_EPAISSEUR):
        balle_vitesse[V] = -balle_vitesse[V]

    test_collision((raquette_position, (RAQUETTE_LARGEUR, RAQUETTE_HAUTEUR)))

    if test_touche_bas(balle_position, BALLE_RAYON, FENETRE_HAUTEUR + BALLE_DIAM):
        fini = True
       
def dessine_court():

    fenetre.fill(BLEU_CLAIR)
    pygame.draw.circle(fenetre, JAUNE, balle_position, BALLE_RAYON)
    pygame.draw.rect(fenetre, ROUGE, (raquette_position, (RAQUETTE_LARGEUR, RAQUETTE_HAUTEUR)))
    pygame.draw.rect(fenetre, GRIS, ((0,0), (MUR_EPAISSEUR,FENETRE_HAUTEUR)))
    pygame.draw.rect(fenetre, GRIS, ((MUR_EPAISSEUR,0), (FENETRE_LARGEUR - 2 * MUR_EPAISSEUR, MUR_EPAISSEUR)))
    pygame.draw.rect(fenetre, GRIS, ((FENETRE_LARGEUR - MUR_EPAISSEUR, 0), (MUR_EPAISSEUR, FENETRE_HAUTEUR)))
    

pygame.init()
pygame.key.set_repeat(200,25)

fenetre_taille = (FENETRE_LARGEUR, FENETRE_HAUTEUR)
fenetre = pygame.display.set_mode(fenetre_taille)

fenetre.fill(BLEU_CLAIR)

balle_vitesse = [5, 5]
balle_position = [10, 300]
raquette_position = [FENETRE_LARGEUR//2 - RAQUETTE_LARGEUR//2,  FENETRE_HAUTEUR - RAQUETTE_ESPACE - RAQUETTE_HAUTEUR]

fini = False
temps = pygame.time.Clock()

#--- Boucle principale
while not fini:

    #--- Quitter l'écran avec la croix
    traite_entrees()

    #--- Logique du jeu
    anime()

    #--- Dessiner l'écran

    dessine_court()

    #--- Raffraichir l'écran
    pygame.display.flip()

    #--- 50 images secondes
    temps.tick(50)

pygame.display.quit()
pygame.quit()