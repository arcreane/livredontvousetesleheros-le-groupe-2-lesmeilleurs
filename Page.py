
from Livre import Livre

class Page():
    def __init__(self,numero:int, texte:str, livre:Livre, is_fin :bool = False):

        self.livre = livre
        self.numero = numero
        unique = True
        for page in livre.pages:
            if page.numero == numero:
                unique = False

        if unique:
            self.texte = texte
            self.options = []
            self.is_fin = is_fin
            livre.pages.append(self)
            if is_fin:
                livre.pages_fin.append(self)

    def afficher(self):
        """permet d'afficher la page et ses options"""


    def getOption(self, titre:str):
        """Permet de recuperer un paragraphe a partir de son titre"""
        for option in self.options:
            if option.titre == titre:
                return option

        return None