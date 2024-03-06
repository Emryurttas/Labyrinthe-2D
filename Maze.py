class Maze:
    """
    Classe Labyrinthe
    Représentation sous forme de graphe non-orienté
    dont chaque sommet est une cellule (un tuple (l,c))
    et dont la structure est représentée par un dictionnaire
      - clés : sommets
      - valeurs : ensemble des sommets voisins accessibles
    """
    def __init__(self, height, width):
        """
        Constructeur d'un labyrinthe de height cellules de haut
        et de width cellules de large
        Les voisinages sont initialisés à des ensembles vides
        Remarque : dans le labyrinthe créé, chaque cellule est complètement emmurée
        """
        self.height = height
        self.width = width
        self.neighbors = {(i,j): set() for i in range(height) for j in range (width)}

    def info(self):
        """
        **NE PAS MODIFIER CETTE MÉTHODE**
        Affichage des attributs d'un objet 'Maze' (fonction utile pour deboguer)
        Retour:
            chaîne (string): description textuelle des attributs de l'objet
        """
        txt = "**Informations sur le labyrinthe**\n"
        txt += f"- Dimensions de la grille : {self.height} x {self.width}\n"
        txt += "- Voisinages :\n"
        txt += str(self.neighbors)+"\n"
        valid = True
        for c1 in {(i, j) for i in range(self.height) for j in range(self.width)}:
            for c2 in self.neighbors[c1]:
                if c1 not in self.neighbors[c2]:
                    valid = False
                    break
            else:
                continue
            break
        txt += "- Structure cohérente\n" if valid else f"- Structure incohérente : {c1} X {c2}\n"
        return txt

    def __str__(self):
        """
        **NE PAS MODIFIER CETTE MÉTHODE**
        Représentation textuelle d'un objet Maze (en utilisant des caractères ascii)
        Retour:
             chaîne (str) : chaîne de caractères représentant le labyrinthe
        """
        txt = ""
        # Première ligne
        txt += "┏"
        for j in range(self.width-1):
            txt += "━━━┳"
        txt += "━━━┓\n"
        txt += "┃"
        for j in range(self.width-1):
            txt += "   ┃" if (0,j+1) not in self.neighbors[(0,j)] else "    "
        txt += "   ┃\n"
        # Lignes normales
        for i in range(self.height-1):
            txt += "┣"
            for j in range(self.width-1):
                txt += "━━━╋" if (i+1,j) not in self.neighbors[(i,j)] else "   ╋"
            txt += "━━━┫\n" if (i+1,self.width-1) not in self.neighbors[(i,self.width-1)] else "   ┫\n"
            txt += "┃"
            for j in range(self.width):
                txt += "   ┃" if (i+1,j+1) not in self.neighbors[(i+1,j)] else "    "
            txt += "\n"
        # Bas du tableau
        txt += "┗"
        for i in range(self.width-1):
            txt += "━━━┻"
        txt += "━━━┛\n"

        return txt

    def add_wall(self, c1, c2):
        """
        Cette méthode ajoute un mur entre c1 et c2
        :param c1: le sommet c1
        :param c2:  le sommet c2
        :return: rien
        """
        # Facultatif : on teste si les sommets sont bien dans le labyrinthe
        assert 0 <= c1[0] < self.height and \
               0 <= c1[1] < self.width and \
               0 <= c2[0] < self.height and \
               0 <= c2[1] < self.width, \
            f"Erreur lors de l'ajout d'un mur entre {c1} et {c2} : les coordonnées de sont pas compatibles avec les dimensions du labyrinthe"
        # Ajout du mur
        if c2 in self.neighbors[c1]:  # Si c2 est dans les voisines de c1
            self.neighbors[c1].remove(c2)  # on le retire
        if c1 in self.neighbors[c2]:  # Si c3 est dans les voisines de c2
            self.neighbors[c2].remove(c1)  # on le retire

    def get_cells(self):
        """
        Cette méthode nous donnes les cellules du labyrinthes
        :return: les cellules du labyrinthe sous forme d'une liste de tuple
        """
        L = []
        for i in range(self.height):
            for j in range(self.width):
                L.append((i, j))
        return L

    def remove_wall(self, c1, c2):
        """
        Cette méthode supprime un mur entre c1 et c2
        :param c1: la cellule 1
        :param c2: la cellule 2
        :return: rien
        """
        # Facultatif : on teste si les sommets sont bien dans le labyrinthe
        assert 0 <= c1[0] < self.height and \
               0 <= c1[1] < self.width and \
               0 <= c2[0] < self.height and \
               0 <= c2[1] < self.width, \
            f"Impossible de supprimer un mur entre {c1} et {c2} : les coordonnées de sont pas compatibles avec les dimensions du labyrinthe"
        # Suppresion du mur
        if not(c2 in self.neighbors[c1]):  # Si c2 n'est pas dans les voisines de c1
            self.neighbors[c1].add(c2)  # on le rajoute
        if not(c1 in self.neighbors[c2]):  # Si c3 n'est pas dans les voisines de c2
            self.neighbors[c2].add(c1)  # on le rajoute

    def get_walls(self)->list:
        """
        Cette méthode nous donne la liste des murs
        :return: la liste des murs sous forme d'une liste tuple
        """
        L = []
        for c1 in self.get_cells():
            c2 = (c1[0], c1[0]+1)
            if c2 in self.get_cells() and not (c2 in self.neighbors[c1]):
                L.append([c1, c2])
            c3 = (c1[0]+1, c1[1])
            if c3 in self.get_cells() and not (c3 in self.neighbors[c1]):
                L.append([c1, c3])
        return L

    def fill(self)->None:
        """
        Cette méthode rajoute tous les murs possibles au labyrinthe
        :return: rien
        """
        for i in range(self.width):
            for j in range(self.height):
                self.neighbors[(i, j)] = set()
        return None

    def empty(self):
        """
        Cette méthode Supprime tous les murs dans le labyrinthe
        :return: rien
        """
        for i in range(self.height):
            for j in range(self.width):
                # Supprime de murs vers la droite et vers le bas
                if j + 1 < self.width:
                    self.remove_wall((i, j), (i, j + 1))
                if i + 1 < self.height:
                    self.remove_wall((i, j), (i + 1, j))

    def get_contiguous_cells(self, c)->list:
        """
        Cette méthode nous donnes la liste des cellules contigües à c
        :return: la liste des cellules contigües de c
        """
        contiguous = []
        if c[0]-1 >= 0:
            contiguous.append((c[0]-1, c[1]))
        if c[0]+1 < self.height:
            contiguous.append((c[0]+1, c[1]))
        if c[1]-1 >= 0:
            contiguous.append((c[0], c[1]-1))
        if c[1]+1 < self.width:
            contiguous.append((c[0], c[1]+1))

        return contiguous

    def get_reachable_cells(self, c)->list:
        reachable = []
        contiguousCells = self.get_contiguous_cells(c)
        for cell in contiguousCells:
            if cell in self.neighbors[c]:
                reachable.append(cell)

        return reachable
