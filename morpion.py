import itertools # = bibliotheque pour calcule entre iterable
import random # = bibliotheque de randomisation utiliser pour faire un coup au hasard 
from itertools import combinations # utile pour ma somme de trio == 15 optimise mes cas de victoire et IA

# ============================================================
# JEU  TIC-TAC-TOE  VERSION TEXTE
# ============================================================

def initialiser_jeu():
    """Initialise la grille, les positions et les valeurs magiques."""
    grille = [[" "]*3 for _ in range(3)] #ma grille = 3 list rempli d espace 
    d_position = {     # dictionnaire dans le quelle j attribue des cle de 1 a 9 a ma grille me donnant des valeur pour chaque cellule  
        1:(0,0), 2:(0,1), 3:(0,2),
        4:(1,0), 5:(1,1), 6:(1,2),
        7:(2,0), 8:(2,1), 9:(2,2)
    }                         #a voir comme une layer representant ma numerotaion de cellule 
    d_valeur_magique = {      # dictionnaire de mon carre magique en  surcouche de mes valeur de 1 a 9
        1:8, 2:1, 3:6,
        4:3, 5:5, 6:7,
        7:4, 8:9, 9:2
    }                         # mon deusieme layer
    return grille, d_position, d_valeur_magique # quand j appele ma fonction me renvoie les valeur de grille, position ,valeur Magique


# initialisation du jeu 
grille, d_position, d_valeur_magique = initialiser_jeu()# quand j ai mes valeur grille ,d_position, d_valeur magique alors je lance fonction initialiser_jeu()
valeur_x = [] # = crée une liste []appeler valeur X
valeur_o = []# = crée une liste []appeler valeur o

#  choix du mode de jeu 
mode = input("Choisissez le mode de jeu :\n1 - Joueur contre IA\n2 - Joueur contre Joueur\n> ") #mode de jeu 1v1 ou 1 vs ia avec 3 ligne

# si mode IA demande qui commence
if mode == "1": # si mode == 1 donc on demande qui commence ?
    choix = input("Souhaitez-vous commencer ? (o/n) : ").lower() # choisir de jouer en premier en minuscule grace a .lower()
    tour_joueur = (choix == "o") #si choix o = tour joueur .
else:
    # en mode joueur vs joueur, le joueur 1 commence toujours
    tour_joueur = True



# FONCTIONS UTILITAIRE


def afficher_grille(): # fonction pour afficher une grille en visuel
    """Affiche la grille du jeu."""
    for ligne in grille: # pour chaque ligne je rajoute 
        print(" | ".join(ligne)) #utilise | pour chaque ligne  ligne = 1:(0,0) au debut 
        print("-" * 9) #utilise - *9 a chaque ligne

def jouer(num_case, symbole): # fonction jouer determine en interne si ma position sur la grille et occuper et place un symbole dessus
    """Place un symbole dans une case si elle est libre."""
    ligne, col = d_position[num_case]# determine ma case 
    if grille[ligne][col] != " ": #si ma grille [position] et pas egale a espace reurn false je peut pas jouer la 
        return False
    grille[ligne][col] = symbole # symbole = ma cellule definie par ma ligne et ma colonne 
    return True # ici jouer(num_case, symbole) on etais defini comme == donc on peut jouer 

def victoire(valeurs):# fonction de victoire determine la victoire en additionant 3 valeur grace a combination dans itertools
    """Verifie si une liste contient une combinaison gagnante (somme = 15)."""
    return any(sum(trio) == 15 for trio in combinations(valeurs, 3)) # renvois toute les somme = a 15 pour 3 combinaisons de valeurs 

def cases_libres(): #fonction case libre return libre comme valeur
    """Retourne la liste des cases disponibles."""
    libres = [] # cree list libres[]
    for i in range(1, 10):# parcours ma grille
        ligne, col = d_position[i] # determine l'index de la position  dans une list d_position
        if grille[ligne][col] == " ": #si ma position == espace
            libres.append(i) # ajoute un index a la liste libre
    return libres #retourne la list libre 


#                           ///// LOGIQUE DE L'IA \\\\\


def coup_ia():# fonction qui definie mes coup IA
    """ renvoie le meilleur coup pour l iA selon une logique simple."""
    libres = cases_libres() #verifie si ma case est libre dansma liste libre 

    # 1 - Gagner si possible
    for case in libres: 
        test = valeur_o + [d_valeur_magique[case]]
        if victoire(test):
            return case

    # 2 - Bloquer le joueur
    for case in libres:
        test = valeur_x + [d_valeur_magique[case]]
        if victoire(test): 
            return case

    # 3 - Prendre le centre
    if 5 in libres:
        return 5

    # 4 - Premier coup : coin aléatoire
    coins = [1, 3, 7, 9]
    coins_libres = [c for c in coins if c in libres]
    if not valeur_o and coins_libres:
        return random.choice(coins_libres)

    # 5 - Sinon, jouer au hasard
    return random.choice(libres)



#           ////// BOUCLE PRINCIPALE DU JEU \\\\\\


for tour in range(1, 10):
    afficher_grille()
    print("\nTour", tour)

    # --- Tour du joueur 1 ---
    if tour_joueur:
        num_case = input("Joueur 1 (X), choisis une case (1-9) : ")
        if not num_case.isdigit() or int(num_case) not in range(1, 10):
            print("Choix invalide. Reessaie.")
            continue

        num_case = int(num_case)
        if not jouer(num_case, "X"):
            print("Case deja prise. Reessaie.")
            continue

        valeur_x.append(d_valeur_magique[num_case])

        if victoire(valeur_x):
            afficher_grille()
            print("Le joueur 1 (X) gagne !")
            break

    # --- Tour du joueur 2 ou de l'IA ---

    else:
        if mode == "1":
            # Mode IA
            num_case_ia = coup_ia()
            jouer(num_case_ia, "O")
            valeur_o.append(d_valeur_magique[num_case_ia])
            print("L'IA joue la case", num_case_ia)
        else:
            # Mode Joueur contre Joueur
            num_case = input("Joueur 2 (O), choisis une case (1-9) : ")
            if not num_case.isdigit() or int(num_case) not in range(1, 10):
                print("Choix invalide. Reessaie.")
                continue

            num_case = int(num_case)
            if not jouer(num_case, "O"):
                print("Case deja prise. Reessaie.")
                continue

            valeur_o.append(d_valeur_magique[num_case])

        # Vérifie la victoire de O ou IA
        if victoire(valeur_o):
            afficher_grille()
            if mode == "1":
                print("L'IA gagne !")
            else:
                print("Le joueur 2 (O) gagne !")
            break

    # --- Vérifie s'il reste des cases libres ---
    if not cases_libres():
        afficher_grille()
        print("Match nul !")
        break

    # --- Changement de tour ---
    tour_joueur = not tour_joueur
