import pygame


#--- Variables
BLEU_CLAIR = (0,191,200)
JAUNE = (255,255,0)
ROUGE = (255,0,0)

FENETRE_LARGEUR = 800
FENETRE_HAUTEUR = 600

BALLE_RAYON = 10

RAQUETTE_LARGEUR = 70
RAQUETTE_HAUTEUR = 10
RAQUETTE_ESPACE = 10
RAQUETTE_DEPLACEMENT = 10

VERS_DROITE = 1
VERS_GAUCHE = -1

TOUCHE_DROITE = pygame.K_RIGHT
TOUCHE_GAUCHE = pygame.K_LEFT

H = 0
V = 1

#--- Fonctions
def deplace_raquette(sens):
    raquette_position[H] += RAQUETTE_DEPLACEMENT * sens
    if raquette_position[H] < 0:
        raquette_position[H] = 0
    elif raquette_position[H] + RAQUETTE_LARGEUR >= FENETRE_LARGEUR:
        raquette_position[H] = FENETRE_LARGEUR - RAQUETTE_LARGEUR


pygame.init()

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
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            fini = True
        elif evenement.type == pygame.KEYDOWN:
            if evenement.key == TOUCHE_DROITE:
                deplace_raquette(VERS_DROITE)
            if evenement.key == TOUCHE_GAUCHE:
                deplace_raquette(VERS_GAUCHE)

    #--- Logique du jeu
    balle_position[H] = balle_position[H] + balle_vitesse[H]
    balle_position[V] = balle_position[V] + balle_vitesse[V]

    if balle_position[H] + BALLE_RAYON >= FENETRE_LARGEUR:
        balle_position[H] = FENETRE_LARGEUR - BALLE_RAYON
        balle_vitesse[H] = -balle_vitesse[H]
    else:
        if balle_position[H] < BALLE_RAYON:
            balle_position[H] = BALLE_RAYON
            balle_vitesse[H] = -balle_vitesse[H]

    if balle_position[V] + BALLE_RAYON >= FENETRE_HAUTEUR:
        balle_position[V] = FENETRE_HAUTEUR - BALLE_RAYON
        balle_vitesse[V] = -balle_vitesse[V]
    else:
        if balle_position[V] < BALLE_RAYON:
            balle_position[V] = BALLE_RAYON
            balle_vitesse[V] = -balle_vitesse[V]

    #--- Dessiner l'écran
    fenetre.fill(BLEU_CLAIR)
    pygame.draw.circle(fenetre, JAUNE, balle_position, BALLE_RAYON)
    pygame.draw.rect(fenetre, ROUGE, (raquette_position, (RAQUETTE_LARGEUR, RAQUETTE_HAUTEUR)))

    #--- Raffraichir l'écran
    pygame.display.flip()

    #--- 50 images secondes
    temps.tick(50)

pygame.display.quit()
pygame.quit()