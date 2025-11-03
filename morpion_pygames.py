import pygame
import random
import sys

# INITIALISATION PYGAME
pygame.init()

# CONSTANTES
LARGEUR = 600
HAUTEUR = 700
TAILLE_CASE = 180
MARGE = 30
LIGNE_LARGEUR = 5

# COULEURS
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS = (200, 200, 200)
BLEU = (52, 152, 219)
ROUGE = (231, 76, 60)
VERT = (46, 204, 113)

# FENETRE
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Tic-Tac-Toe")
horloge = pygame.time.Clock()

# POLICES
police_titre = pygame.font.Font(None, 48)
police_texte = pygame.font.Font(None, 36)
police_bouton = pygame.font.Font(None, 32)


# FONCTIONS DU JEU (Carré magique)
def initialiser_jeu():
    """Crée la grille vide et les dictionnaires nécessaires."""
    board = [[" ", " ", " "],
             [" ", " ", " "], 
             [" ", " ", " "]]
    
    position = {
        0:(0,0), 1:(0,1), 2:(0,2),
        3:(1,0), 4:(1,1), 5:(1,2),
        6:(2,0), 7:(2,1), 8:(2,2)
    }
    
    valeur_magique = {
        0:2, 1:7, 2:6,
        3:9, 4:5, 5:1,
        6:4, 7:3, 8:8
    }
    
    return board, position, valeur_magique


def obtenir_cases_libres(board, position):
    """Retourne la liste des cases vides."""
    libres = []
    for index in range(9):
        ligne, col = position[index]
        if board[ligne][col] == " ":
            libres.append(index)
    return libres


def verifier_victoire(valeurs):
    """Vérifie si 3 valeurs font 15 (victoire)."""
    if len(valeurs) < 3:
        return False
    
    for i in range(len(valeurs)):
        for j in range(i + 1, len(valeurs)):
            for k in range(j + 1, len(valeurs)):
                if valeurs[i] + valeurs[j] + valeurs[k] == 15:
                    return True
    return False


def recuperer_valeurs(board, signe, position, valeur_magique):
    """Retourne les valeurs magiques jouées par un signe."""
    valeurs = []
    for index in range(9):
        ligne, col = position[index]
        if board[ligne][col] == signe:
            valeurs.append(valeur_magique[index])
    return valeurs


def peut_gagner(valeurs_actuelles, case_test, valeur_magique):
    """Vérifie si jouer cette case permet de gagner."""
    test_valeurs = valeurs_actuelles + [valeur_magique[case_test]]
    return verifier_victoire(test_valeurs)


def strategie_difficile_tour1():
    """Stratégie IA tour 1 : jouer case 6."""
    return 6


def strategie_difficile_tour2(board, adversaire, position, libres):
    """Stratégie IA tour 2 : adapter selon le joueur."""
    case_joueur = None
    for index in range(9):
        ligne, col = position[index]
        if board[ligne][col] == adversaire:
            case_joueur = index
            break
    
    # Si joueur prend un bord (1,2,7,8) -> prendre coin opposé
    if case_joueur in [1, 2, 7, 8]:
        if 0 in libres:
            return 0
    
    # Si joueur prend un coin adjacent ou un bord latéral
    if case_joueur in [0, 3, 5]:
        if 8 in libres:
            return 8
    
    # Si joueur prend le centre -> prendre coin en diagonale (2 ou 8)
    if case_joueur == 4:
        if 2 in libres:
            return 2
        if 8 in libres:
            return 8
    
    return None


def strategie_difficile_tour3(board, signe, libres):
    """Stratégie IA tour 3 : créer une fourchette."""
    if board[2][0] == signe:
        if board[0][0] == signe:
            if 8 in libres:
                return 8
    
    if board[2][0] == signe:
        if board[2][2] == signe:
            if 2 in libres:
                return 2
    
    return None


def ia(board, signe, niveau_ia, position, valeur_magique):
    """Fonction principale de l'IA."""
    if signe not in ["X", "O"]:
        return False
    
    libres = obtenir_cases_libres(board, position)
    
    if len(libres) == 0:
        return False
    
    adversaire = "O" if signe == "X" else "X"
    
    valeurs_ia = recuperer_valeurs(board, signe, position, valeur_magique)
    valeurs_adv = recuperer_valeurs(board, adversaire, position, valeur_magique)
    
    if niveau_ia == "1":
        return random.choice(libres)
    
    if niveau_ia == "2":
        if 4 in libres:
            return 4
        return random.choice(libres)
    
    if niveau_ia == "3":
        if len(valeurs_ia) == 0:
            return strategie_difficile_tour1()
        
        if len(valeurs_ia) == 1:
            coup = strategie_difficile_tour2(board, adversaire, position, libres)
            if coup is not None:
                return coup
        
        if len(valeurs_ia) == 2:
            coup = strategie_difficile_tour3(board, signe, libres)
            if coup is not None:
                return coup
        
        for case in libres:
            if peut_gagner(valeurs_ia, case, valeur_magique):
                return case
        
        for case in libres:
            if peut_gagner(valeurs_adv, case, valeur_magique):
                return case
        
        if 4 in libres:
            return 4
        
        coins = [0, 2, 6, 8]
        for coin in coins:
            if coin in libres:
                return coin
        
        return random.choice(libres)
    
    return random.choice(libres)


# FONCTIONS PYGAME
def dessiner_grille():
    """Dessine la grille du jeu."""
    ecran.fill(BLANC)
    
    # Lignes verticales
    pygame.draw.line(ecran, NOIR, (MARGE + TAILLE_CASE, MARGE + 100), 
                     (MARGE + TAILLE_CASE, MARGE + 100 + TAILLE_CASE * 3), LIGNE_LARGEUR)
    pygame.draw.line(ecran, NOIR, (MARGE + TAILLE_CASE * 2, MARGE + 100), 
                     (MARGE + TAILLE_CASE * 2, MARGE + 100 + TAILLE_CASE * 3), LIGNE_LARGEUR)
    
    # Lignes horizontales
    pygame.draw.line(ecran, NOIR, (MARGE, MARGE + 100 + TAILLE_CASE), 
                     (MARGE + TAILLE_CASE * 3, MARGE + 100 + TAILLE_CASE), LIGNE_LARGEUR)
    pygame.draw.line(ecran, NOIR, (MARGE, MARGE + 100 + TAILLE_CASE * 2), 
                     (MARGE + TAILLE_CASE * 3, MARGE + 100 + TAILLE_CASE * 2), LIGNE_LARGEUR)


def dessiner_symboles(board):
    """Dessine les X et O sur la grille."""
    for ligne in range(3):
        for col in range(3):
            symbole = board[ligne][col]
            x = MARGE + col * TAILLE_CASE + TAILLE_CASE // 2
            y = MARGE + 100 + ligne * TAILLE_CASE + TAILLE_CASE // 2
            
            if symbole == "X":
                # Dessiner X
                pygame.draw.line(ecran, BLEU, 
                               (x - 50, y - 50), (x + 50, y + 50), 8)
                pygame.draw.line(ecran, BLEU, 
                               (x + 50, y - 50), (x - 50, y + 50), 8)
            
            elif symbole == "O":
                # Dessiner O
                pygame.draw.circle(ecran, ROUGE, (x, y), 50, 8)


def dessiner_texte(texte, x, y, police, couleur):
    """Affiche un texte à l'écran."""
    surface = police.render(texte, True, couleur)
    rect = surface.get_rect(center=(x, y))
    ecran.blit(surface, rect)


def dessiner_bouton(texte, x, y, largeur, hauteur, couleur):
    """Dessine un bouton et retourne son rectangle."""
    rect = pygame.Rect(x - largeur // 2, y - hauteur // 2, largeur, hauteur)
    pygame.draw.rect(ecran, couleur, rect, border_radius=10)
    pygame.draw.rect(ecran, NOIR, rect, 3, border_radius=10)
    dessiner_texte(texte, x, y, police_bouton, BLANC)
    return rect


def obtenir_case_cliquee(pos):
    """Retourne l'index de la case cliquée (0-8) ou None."""
    x, y = pos
    
    if x < MARGE or x > MARGE + TAILLE_CASE * 3:
        return None
    if y < MARGE + 100 or y > MARGE + 100 + TAILLE_CASE * 3:
        return None
    
    col = (x - MARGE) // TAILLE_CASE
    ligne = (y - MARGE - 100) // TAILLE_CASE
    
    index = ligne * 3 + col
    return index


def ecran_menu():
    """Affiche le menu principal."""
    en_cours = True
    choix = None
    
    while en_cours:
        ecran.fill(BLANC)
        
        dessiner_texte("TIC-TAC-TOE", LARGEUR // 2, 80, police_titre, NOIR)
        
        bouton_ia = dessiner_bouton("Jouer contre IA", LARGEUR // 2, 200, 300, 60, BLEU)
        bouton_2j = dessiner_bouton("2 Joueurs", LARGEUR // 2, 300, 300, 60, VERT)
        bouton_quitter = dessiner_bouton("Quitter", LARGEUR // 2, 400, 300, 60, ROUGE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                if bouton_ia.collidepoint(pos):
                    choix = "ia"
                    en_cours = False
                
                elif bouton_2j.collidepoint(pos):
                    choix = "2j"
                    en_cours = False
                
                elif bouton_quitter.collidepoint(pos):
                    pygame.quit()
                    sys.exit()
        
        pygame.display.flip()
        horloge.tick(60)
    
    return choix


def ecran_difficulte():
    """Affiche le choix de difficulté."""
    en_cours = True
    niveau = None
    
    while en_cours:
        ecran.fill(BLANC)
        
        dessiner_texte("Choisissez la difficulté", LARGEUR // 2, 80, police_titre, NOIR)
        
        bouton_facile = dessiner_bouton("Facile", LARGEUR // 2, 200, 300, 60, VERT)
        bouton_moyen = dessiner_bouton("Moyen", LARGEUR // 2, 300, 300, 60, BLEU)
        bouton_difficile = dessiner_bouton("Difficile", LARGEUR // 2, 400, 300, 60, ROUGE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                if bouton_facile.collidepoint(pos):
                    niveau = "1"
                    en_cours = False
                
                elif bouton_moyen.collidepoint(pos):
                    niveau = "2"
                    en_cours = False
                
                elif bouton_difficile.collidepoint(pos):
                    niveau = "3"
                    en_cours = False
        
        pygame.display.flip()
        horloge.tick(60)
    
    return niveau


def jeu_principal(mode, niveau_ia=None):
    """Boucle principale du jeu."""
    board, position, valeur_magique = initialiser_jeu()
    valeur_x = []
    valeur_o = []
    
    if niveau_ia == "3":
        tour_joueur = False
    else:
        tour_joueur = True
    
    jeu_termine = False
    message = ""
    
    while True:
        dessiner_grille()
        dessiner_symboles(board)
        
        if not jeu_termine:
            if tour_joueur:
                dessiner_texte("Tour du Joueur X", LARGEUR // 2, 40, police_texte, BLEU)
            else:
                if mode == "ia":
                    dessiner_texte("Tour de l'IA (O)", LARGEUR // 2, 40, police_texte, ROUGE)
                else:
                    dessiner_texte("Tour du Joueur O", LARGEUR // 2, 40, police_texte, ROUGE)
        else:
            dessiner_texte(message, LARGEUR // 2, 40, police_texte, VERT)
            bouton_menu = dessiner_bouton("Menu", LARGEUR // 2, 650, 200, 50, BLEU)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                if jeu_termine:
                    if 'bouton_menu' in locals():
                        if bouton_menu.collidepoint(pos):
                            return
                
                if not jeu_termine:
                    if tour_joueur:
                        index = obtenir_case_cliquee(pos)
                        
                        if index is not None:
                            ligne, col = position[index]
                            
                            if board[ligne][col] == " ":
                                board[ligne][col] = "X"
                                valeur_x.append(valeur_magique[index])
                                
                                if verifier_victoire(valeur_x):
                                    message = "Le Joueur X gagne !"
                                    jeu_termine = True
                                
                                elif len(obtenir_cases_libres(board, position)) == 0:
                                    message = "Match nul !"
                                    jeu_termine = True
                                
                                else:
                                    tour_joueur = False
                    
                    else:
                        if mode == "2j":
                            index = obtenir_case_cliquee(pos)
                            
                            if index is not None:
                                ligne, col = position[index]
                                
                                if board[ligne][col] == " ":
                                    board[ligne][col] = "O"
                                    valeur_o.append(valeur_magique[index])
                                    
                                    if verifier_victoire(valeur_o):
                                        message = "Le Joueur O gagne !"
                                        jeu_termine = True
                                    
                                    elif len(obtenir_cases_libres(board, position)) == 0:
                                        message = "Match nul !"
                                        jeu_termine = True
                                    
                                    else:
                                        tour_joueur = True
        
        # Tour de l'IA
        if not jeu_termine:
            if not tour_joueur:
                if mode == "ia":
                    pygame.time.wait(500)
                    
                    coup_ia = ia(board, "O", niveau_ia, position, valeur_magique)
                    
                    if coup_ia is not False:
                        ligne, col = position[coup_ia]
                        board[ligne][col] = "O"
                        valeur_o.append(valeur_magique[coup_ia])
                        
                        if verifier_victoire(valeur_o):
                            message = "L'IA gagne !"
                            jeu_termine = True
                        
                        elif len(obtenir_cases_libres(board, position)) == 0:
                            message = "Match nul !"
                            jeu_termine = True
                        
                        else:
                            tour_joueur = True
        
        pygame.display.flip()
        horloge.tick(60)


# BOUCLE PRINCIPALE
def main():
    """Fonction principale."""
    while True:
        mode = ecran_menu()
        
        if mode == "ia":
            niveau = ecran_difficulte()
            jeu_principal("ia", niveau)
        
        elif mode == "2j":
            jeu_principal("2j")


if __name__ == "__main__":
    main()