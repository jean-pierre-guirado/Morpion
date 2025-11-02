import random

# PARTIE 1 : INITIALISATION DU JEU


def initialiser_jeu():
    """
    Cree la grille vide et les dictionnaires necessaires.
    
    Retourne :
    - board : grille 3x3 vide (liste de listes)
    - position : dictionnaire pour convertir numero (0-8) en coordonnees (ligne, col)
    - valeur_magique : dictionnaire du carre magique (3 cases = 15 = victoire)
    """
    # Creer une grille vide 3x3
    board = [[" ", " ", " "],
             [" ", " ", " "], 
             [" ", " ", " "]]
    
    # Dictionnaire pour convertir numero en position
    # Exemple : 0 = ligne 0, colonne 0 (coin haut gauche)
    position = {
        0:(0,0), 1:(0,1), 2:(0,2),
        3:(1,0), 4:(1,1), 5:(1,2),
        6:(2,0), 7:(2,1), 8:(2,2)
    }
    
    # Carre magique : si 3 valeurs font 15, c'est une victoire
    # Exemple : 2+7+6=15 (ligne du haut)
    valeur_magique = {
        0:2, 1:7, 2:6,
        3:9, 4:5, 5:1,
        6:4, 7:3, 8:8
    }
    
    return board, position, valeur_magique

# PARTIE 2 : AFFICHAGE


def afficher_grille(board):
    """
    Affiche la grille actuelle avec les X et O.
    
    Parametre :
    - board : la grille de jeu
    """
    print("\n")
    # Parcourir chaque ligne de la grille
    for ligne in board:
        # Afficher les cases separees par " | "
        print(" | ".join(ligne))
        print("---------")
    print("\n")


def afficher_grille_numerotee(position):
    """
    Affiche la grille avec les numeros des cases (0 a 8).
    Permet au joueur de savoir quel numero taper.
    
    Parametre :
    - position : dictionnaire des positions
    """
    # Creer une grille temporaire pour afficher les numeros
    grille_num = [[" ", " ", " "], 
                  [" ", " ", " "], 
                  [" ", " ", " "]]
    
    # Remplir la grille avec les numeros (0 a 8)
    for num, (ligne, col) in position.items():
        # Convertir le numero en texte pour l'affichage
        grille_num[ligne][col] = str(num)
    
    print("\n=== Numerotation des cases ===")
    # Afficher la grille numerotee
    for ligne in grille_num:
        print(" | ".join(ligne))
        print("---------")
    print("\n")

# PARTIE 3 : LOGIQUE DU JEU

def placer_coup(board, position, index, signe):
    """
    Place un signe (X ou O) dans une case.
    
    Parametres :
    - board : la grille de jeu
    - position : dictionnaire des positions
    - index : numero de la case (0-8)
    - signe : "X" ou "O"
    
    Retourne :
    - True si le coup est valide
    - False si la case est deja prise
    """
    # Recuperer les coordonnees de la case
    ligne, col = position[index]
    
    # Verifier si la case est libre
    if board[ligne][col] != " ":
        return False
    
    # Placer le signe dans la case
    board[ligne][col] = signe
    return True


def obtenir_cases_libres(board, position):
    """
    Retourne la liste des cases vides.
    
    Parametres :
    - board : la grille de jeu
    - position : dictionnaire des positions
    
    Retourne :
    - libres : liste des numeros de cases libres
    """
    libres = []
    
    # Parcourir toutes les cases (0 a 8)
    for index in range(9):
        # Recuperer les coordonnees
        ligne, col = position[index]
        
        # Si la case est vide, l'ajouter a la liste
        if board[ligne][col] == " ":
            libres.append(index)
    
    return libres


def verifier_victoire(valeurs):
    """
    Verifie si 3 valeurs du carre magique font 15 (victoire).
    
    Parametre :
    - valeurs : liste des valeurs magiques jouees
    
    Retourne :
    - True si victoire
    - False sinon
    """
    # Il faut au moins 3 cases pour gagner
    if len(valeurs) < 3:
        return False
    
    # Tester toutes les combinaisons de 3 valeurs
    for i in range(len(valeurs)):
        for j in range(i + 1, len(valeurs)):
            for k in range(j + 1, len(valeurs)):
                # Si la somme fait 15, c'est une victoire
                if valeurs[i] + valeurs[j] + valeurs[k] == 15:
                    return True
    
    return False

# PARTIE 4 : INTELLIGENCE ARTIFICIELLE

def recuperer_valeurs(board, signe, position, valeur_magique):
    """
    Recupere les valeurs magiques jouees par un signe.
    
    Parametres :
    - board : la grille de jeu
    - signe : "X" ou "O"
    - position : dictionnaire des positions
    - valeur_magique : dictionnaire du carre magique
    
    Retourne :
    - valeurs : liste des valeurs magiques jouees par ce signe
    """
    valeurs = []
    
    # Parcourir toutes les cases
    for index in range(9):
        ligne, col = position[index]
        
        # Si cette case contient le signe recherche
        if board[ligne][col] == signe:
            # Ajouter sa valeur magique a la liste
            valeurs.append(valeur_magique[index])
    
    return valeurs


def peut_gagner(valeurs_actuelles, case_test, valeur_magique):
    """
    Verifie si jouer une case permet de gagner.
    
    Parametres :
    - valeurs_actuelles : valeurs deja jouees
    - case_test : case a tester
    - valeur_magique : dictionnaire du carre magique
    
    Retourne :
    - True si cette case permet de gagner
    - False sinon
    """
    # Ajouter la valeur de la case testee aux valeurs actuelles
    test_valeurs = valeurs_actuelles + [valeur_magique[case_test]]
    
    # Verifier si ca fait une victoire
    return verifier_victoire(test_valeurs)


def strategie_difficile_tour1():
    """
    Strategie de l'IA pour le tour 1 : jouer case 6 (coin bas gauche).
    
    Retourne :
    - 6 : numero de la case a jouer
    """
    return 6


def strategie_difficile_tour2(board, adversaire, position, libres):
    """
    Strategie de l'IA pour le tour 2 : s'adapter au coup du joueur.
    
    Parametres :
    - board : la grille de jeu
    - adversaire : signe de l'adversaire ("X" ou "O")
    - position : dictionnaire des positions
    - libres : liste des cases libres
    
    Retourne :
    - numero de la case a jouer ou None
    """
    # Trouver ou le joueur a joue
    case_joueur = None
    for index in range(9):
        ligne, col = position[index]
        if board[ligne][col] == adversaire:
            case_joueur = index
            break
    
    # Si le joueur a joue un bord (1, 2, 7, 8)
    if case_joueur in [1, 2, 7, 8]:
        # Jouer case 0 si libre
        if 0 in libres:
            return 0
    
    # Si le joueur a joue 0, 3 ou 5
    if case_joueur in [0, 3, 5]:
        # Jouer case 8 si libre
        if 8 in libres:
            return 8
    
    # Si le joueur a joue le centre (case 4)
    if case_joueur == 4:
        # Jouer case 2 si libre (amelioration)
        if 2 in libres:
            return 2
        # Sinon jouer case 8
        if 8 in libres:
            return 8
    
    return None


def strategie_difficile_tour3(board, signe, libres):
    """
    Strategie de l'IA pour le tour 3 : creer une fourchette.
    Une fourchette = 2 menaces de victoire en meme temps.
    
    Parametres :
    - board : la grille de jeu
    - signe : signe de l'IA ("X" ou "O")
    - libres : liste des cases libres
    
    Retourne :
    - numero de la case a jouer ou None
    """
    # Si l'IA a case 6 et case 0
    if board[2][0] == signe:
        if board[0][0] == signe:
            # Jouer case 8 pour creer une fourchette
            if 8 in libres:
                return 8
    
    # Si l'IA a case 6 et case 8
    if board[2][0] == signe:
        if board[2][2] == signe:
            # Jouer case 2 pour creer une fourchette
            if 2 in libres:
                return 2
    
    return None


def ia(board, signe, niveau_ia, position, valeur_magique):
    """
    Fonction principale de l'IA.
    Choisit la case a jouer selon le niveau de difficulte.
    
    Parametres :
    - board : grille de jeu
    - signe : "X" ou "O"
    - niveau_ia : "1" (facile), "2" (moyen) ou "3" (difficile)
    - position : dictionnaire des positions
    - valeur_magique : dictionnaire du carre magique
    
    Retourne :
    - numero de la case a jouer (0-8) ou False en cas d'erreur
    """
    # Verification : le signe doit etre X ou O
    if signe not in ["X", "O"]:
        return False
    
    # Obtenir la liste des cases libres
    libres = obtenir_cases_libres(board, position)
    
    # Si aucune case libre, retourner False
    if len(libres) == 0:
        return False
    
    # Determiner le signe de l'adversaire
    if signe == "X":
        adversaire = "O"
    else:
        adversaire = "X"
    
    # Recuperer les valeurs magiques de chaque joueur
    valeurs_ia = recuperer_valeurs(board, signe, position, valeur_magique)
    valeurs_adv = recuperer_valeurs(board, adversaire, position, valeur_magique)
    
    # NIVEAU 1 : 
    # L'IA joue au hasard
    if niveau_ia == "1":
        return random.choice(libres)
    
    #  NIVEAU 2 : MOYEN 
   # L'IA prend le centre si libre, sinon joue au hasard
    if niveau_ia == "2":
        # Si case 4 (centre) est libre
        if 4 in libres:
            return 4
        # Sinon jouer au hasard
        return random.choice(libres)
    
    # niveau 3 : difficile
    if niveau_ia == "3":
        
        # strategie generale (priorite maximale)
        
        # 1. gagner si possible
        for case in libres:
            if peut_gagner(valeurs_ia, case, valeur_magique):
                return case
        
        # 2. bloquer l'adversaire
        for case in libres:
            if peut_gagner(valeurs_adv, case, valeur_magique):
                return case
        
        # tour 1 : jouer case 6
        if len(valeurs_ia) == 0:
            return strategie_difficile_tour1()
        
        # tour 2 : s'adapter au joueur
        if len(valeurs_ia) == 1:
            coup = strategie_difficile_tour2(board, adversaire, position, libres)
            if coup is not None:
                return coup
        
        # tour 3 : creer une fourchette
        if len(valeurs_ia) == 2:
            coup = strategie_difficile_tour3(board, signe, libres)
            if coup is not None:
                return coup
        
        # 3. prendre le centre si libre
        if 4 in libres:
            return 4
        
        # 4. prendre un coin
        coins = [0, 2, 6, 8]
        for coin in coins:
            if coin in libres:
                return coin
        
        # 5. dernier recours : jouer au hasard
        return random.choice(libres)
    
    # Par defaut : jouer au hasard
    return random.choice(libres)



# PARTIE 5 : BOUCLE PRINCIPALE DU Jeu

# Initialiser le jeu
board, position, valeur_magique = initialiser_jeu()
valeur_x = []
valeur_o = []

# Afficher le titre
print("TIC-TAC-TOE")
afficher_grille_numerotee(position)

# Demander le mode de jeu
print("Choisissez le mode de jeu :")
print("1 - Joueur contre IA")
print("2 - Joueur contre Joueur")
mode = input("> ")

# Variable pour savoir si c'est le tour du joueur X
tour_joueur = True
niveau_ia = None

# Configuration selon le mode choisi
if mode == "1":
    # Mode IA : demander le niveau
    print("\nChoisissez le niveau :")
    print("1 - Facile")
    print("2 - Moyen")
    print("3 - Difficile")
    niveau_ia = input("> ")
    
    # En mode difficile, l'IA commence
    if niveau_ia == "3":
        print("\nEn mode difficile, l'IA commence toujours !")
        tour_joueur = False
    else:
        # Demander qui commence
        choix = input("\nSouhaitez-vous commencer ? (o/n) : ").lower()
        if choix == "o":
            tour_joueur = True
        else:
            tour_joueur = False
else:
    # Mode 2 joueurs : joueur X commence
    tour_joueur = True
    niveau_ia = None

# Compteur de tours
tour = 1

# Boucle principale : maximum 9 tours
while tour <= 9:
    # Afficher la grille et le numero du tour
    afficher_grille(board)
    print("Tour", tour)
    
    # TOUR DU JOUEUR X 
    if tour_joueur:
        choix_valide = False
        
        # Boucle jusqu'a ce que le joueur fasse un coup valide
        while not choix_valide:
            index = input("Joueur 1 (X), choisis une case (0-8) : ")
            
            # Verifier que c'est un nombre
            if not index.isdigit():
                print("Erreur : tape un numero entre 0 et 8")
                continue
            
            # Convertir en entier
            index = int(index)
            
            # Verifier que c'est entre 0 et 8
            if index < 0:
                print("Erreur : tape un numero entre 0 et 8")
                continue
            
            if index > 8:
                print("Erreur : tape un numero entre 0 et 8")
                continue
            
            # Essayer de placer le coup
            if placer_coup(board, position, index, "X"):
                # Ajouter la valeur magique
                valeur_x.append(valeur_magique[index])
                choix_valide = True
            else:
                print("Case deja prise ! Choisis-en une autre.")
        
        # Verifier si le joueur X a gagne
        if verifier_victoire(valeur_x):
            afficher_grille(board)
            print("Le joueur 1 (X) gagne !")
            break
    
    #  TOUR DU JOUEUR O OU IA
    else:
        # Si mode IA
        if mode == "1":
            # Appeler la fonction IA
            coup_ia = ia(board, "O", niveau_ia, position, valeur_magique)
            
            # Verifier que l'IA a pu jouer
            if coup_ia is False:
                print("Erreur de l'IA !")
                break
            
            # Placer le coup de l'IA
            placer_coup(board, position, coup_ia, "O")
            valeur_o.append(valeur_magique[coup_ia])
            print("L'IA joue la case", coup_ia)
        
        # Si mode 2 joueurs
        else:
            choix_valide = False
            
            # Boucle jusqu'a ce que le joueur fasse un coup valide
            while not choix_valide:
                index = input("Joueur 2 (O), choisis une case (0-8) : ")
                
                # Verifier que c'est un nombre
                if not index.isdigit():
                    print("Erreur : tape un numero entre 0 et 8")
                    continue
                
                # Convertir en entier
                index = int(index)
                
                # Verifier que c'est entre 0 et 8
                if index < 0:
                    print("Erreur : tape un numero entre 0 et 8")
                    continue
                
                if index > 8:
                    print("Erreur : tape un numero entre 0 et 8")
                    continue
                
                # Essayer de placer le coup
                if placer_coup(board, position, index, "O"):
                    valeur_o.append(valeur_magique[index])
                    choix_valide = True
                else:
                    print("Case deja prise ! Choisis-en une autre.")
        
        # Verifier si le joueur O ou l'IA a gagne
        if verifier_victoire(valeur_o):
            afficher_grille(board)
            if mode == "1":
                print("L'IA gagne !")
            else:
                print("Le joueur 2 (O) gagne !")
            break
    
    # Verifier si toutes les cases sont remplies (match nul)
    if len(obtenir_cases_libres(board, position)) == 0:
        afficher_grille(board)
        print("Match nul ! Bien joue a tous les deux.")
        break
    
    # Changer de joueur pour le prochain tour
    tour_joueur = not tour_joueur
    
    # Incrementer le compteur de tours
    tour += 1