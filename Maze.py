import random


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

    def get_walls(self) -> list:
        """
        Cette méthode nous donne la liste des murs
        :return: la liste des murs sous forme d'une liste de listes de tuples
        """
        walls = []
        for ligne in range(self.height):
            for col in range(self.width):
                cell = (ligne, col)
                if col + 1 < self.width and not ((ligne, col + 1) in self.neighbors[cell]):
                    walls.append([cell, (ligne, col + 1)])
                if ligne + 1 < self.height and not ((ligne + 1, col) in self.neighbors[cell]):
                    walls.append([cell, (ligne + 1, col)])
        return walls

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
        """
        Cette méthode retourne la liste des cellules accessibles depuis c
        :param c: la cellule dont on veut savoir les cellules accessibles
        :return: la liste des cellules accessibles depuis c
        """
        reachable = []
        contiguousCells = self.get_contiguous_cells(c)
        for cell in contiguousCells:
            if cell in self.neighbors[c]:
                reachable.append(cell)

        return reachable

    @classmethod
    def gen_btree(cls, h, w):
        """
        Méthode de classe pour générer un labyrinthe à h lignes et w colonnes
        en utilisant l'algorithme de construction par arbre binaire.
        :param h: la hauteur du labyrinthe
        :param w: la largeur du labyrinthe
        :return: le nouveau labyrinthe
        """
        maze = cls(h, w)

        for i in range(h):
            for j in range(w):
                if i < h - 1 and j < w - 1:
                    direction = random.choice(["EST", "SUD"])
                elif i < h - 1:
                    direction = "SUD"
                elif j < w - 1:
                    direction = "EST"
                else:
                    direction = None

                if direction == "EST":
                    maze.remove_wall((i, j), (i, j + 1))
                elif direction == "SUD":
                    maze.remove_wall((i, j), (i + 1, j))

        return maze

    @classmethod
    def gen_slidewinder(cls, h, w):
        """
        Cette méthode génère un labyrinthe selon l'algorithme de sidewinder
        :param h: la hauteur du labyrinthe
        :param w: la largeur du labyrinthe
        :return: le nouveau labyrinthe
        """
        maze = cls(h, w)

        for i in range(h - 1):
            sequence = []

            for j in range(w - 1):
                sequence.append((i, j))

                if random.random() < 0.5:  # si c'est pile
                    maze.remove_wall((i, j), (i, j + 1))
                else:
                    if sequence:  # si la séquence n'est pas vide
                        random_cell = random.choice(sequence)
                        maze.remove_wall(random_cell, (random_cell[0] + 1, random_cell[1]))
                    sequence = []

                    # ajouter la dernière cellule à la séquence
            sequence.append((i, w - 1))

            #Casser le mur SUD d'une cellule aléatoire dans la séquence
            if sequence:
                random_cell = random.choice(sequence)
                maze.remove_wall(random_cell, (random_cell[0] + 1, random_cell[1]))

        #Casser tous les murs EST de la dernière ligne
        for j in range(w - 1):
            maze.remove_wall((h - 1, j), (h - 1, j + 1))
        return maze

    @classmethod
    def gen_fusion(cls, h, w):
        """
        Méthode de classe pour générer un labyrinthe à h lignes et w colonnes
        en utilisant l'algorithme de fusion.
        :param h: la hauteur du labyrinthe
        :param w: la largeur du labyrinthe
        return: retourne le labyrinthe parfait
        """
        maze = cls(h, w)
        maze.fill()
        labels = []

        # Labélisation des cellules de 1 à n
        for i in range(h):
            for j in range(w):
                labels.append(i * w + j + 1)

        # Extraction de la liste des murs
        walls = maze.get_walls()
        # On permute les murs
        random.shuffle(walls)
        # Pour chaque mur de la liste
        for wall in walls:
            label_c1 = labels[wall[0][0] * w + wall[0][1]]
            label_c2 = labels[wall[1][0] * w + wall[1][1]]

            if label_c1 != label_c2:  # Si les deux cellules n'ont pas le même label
                maze.remove_wall(wall[0], wall[1])  # Casser le mur

                # Affecter le label de l'une des deux cellules à l'autre et à toutes celles qui ont le même label que la deuxième
                for i in range(h * w):
                    if labels[i] == label_c2:
                        labels[i] = label_c1
        return maze

    @classmethod
    def gen_exploration(cls, h, w):
        """
        Cette méthode génère un labyrinthe selon l'algorithme de d'exploration exhaustive
        :param h: la hauteur du labyrinthe
        :param w: la largeur du labyrinthe
        :return: le nouveau labyrinthe
        """
        maze = cls(h, w)
        cells = maze.get_cells()
        # Choisir une cellule aléatoire
        randomCell = random.choice(cells)
        # Liste des cellules visitées
        marked = [randomCell]
        # Créer la pile et ajouter la cellule aléatoirement choisie
        pile = [randomCell]

        while len(pile) > 0:
            # Prendre la cellule au dessus de la pile et la retirer
            higherCell = pile[len(pile) - 1]
            pile.pop(len(pile) - 1)
            # Vérifier les voisins non marqués de la cellule
            neighbors = maze.get_contiguous_cells(higherCell)

            nonMarkedNeighbors = []
            for neighbor in neighbors:
                if neighbor not in marked:
                    nonMarkedNeighbors.append(neighbor)

            # Si cette cellule a des voisins qui n'ont pas encore été visités
            if len(nonMarkedNeighbors) > 0:
                # Remettre la cellule sur la pile
                pile.append(higherCell)
                # Choisir au hasard l'une de ses cellules contiguës qui n’a pas été visitée
                randomContigue = random.choice(nonMarkedNeighbors)
                # Casser le mur entre la cellule (celle qui a été dépilée) et celle qui vient d’être choisie
                maze.remove_wall(higherCell, randomContigue)
                # Marquer la cellule qui vient d’être choisie comme visitée
                marked.append(randomContigue)
                # Et la mettre sur la pile
                pile.append(randomContigue)

        return maze





