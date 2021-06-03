
from Livre import Livre


class Compteur():
    def __init__(self, nom:str, livre:Livre, valeur:float,isDepart=True):
        self.nom = nom
        self.livre = livre
        self.valeur = valeur
        unique = True
        for compteur in livre.compteurs:
            if compteur.nom == nom:
                unique = False

        if unique and isDepart:
            livre.compteurs.append(self)

