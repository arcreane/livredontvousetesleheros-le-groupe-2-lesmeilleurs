from Livre import Livre


class Objet():
    def __init__(self, nom:str, livre : Livre, path_image:str="vide.png", isDepart:bool=True):
        self.nom = nom
        self.livre = livre
        self.path_image = path_image
        if isDepart:
            livre.objets.append(self)