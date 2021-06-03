from Page import Page
from Objet import Objet
from Compteur import Compteur
import Partie

class Option():
    def __init__(self, titre:str, page: Page, num_lien_page : int, texte :str):

        self.gain_objet = []
        self.modif_compteur = []
        self.titre = titre
        self.page = page
        self.livre = page.livre
        self.num_lien_page = num_lien_page
        self.conditions = []
        self.texte = texte

        unique = True
        for option in page.options:
            if option.titre == titre:
                unique = False
        if unique:
            page.options.append(self)


    def isCondition(self):
        """Permet de voir si la condition est realisable, renvoie un booleen"""

        sortie = True
        for condition in self.conditions:
            if not condition.isRespected():
                sortie = False

        return sortie


    def isConditionDe(self, partie:Partie):
        sortie = True
        for condition in self.conditions:
            if condition.isDe():
                if not condition.isRespected(partie):
                    return False
        return sortie

    def isConditionObjet(self, partie:Partie):
        sortie = True
        for condition in self.conditions:
            if condition.isObjet():
                if not condition.isRespected(partie):
                    return False
        return sortie

    def isConditionCompteur(self, partie:Partie):
        sortie = True
        for condition in self.conditions:
            if condition.isCompteur():
                if not condition.isRespected(partie):
                    return False
        return sortie


    def actionClic(self, partie:Partie):
        """Applique les effets d'action si ce paragraphe est choisi"""

        for elem in self.gain_objet:
            if elem[0] not in [obj.nom for obj in partie.objets]:
                partie.objets.append(Objet(elem[0],self.livre,elem[1],False))

        for modif in self.modif_compteur:
            nom_compteur = modif[0]
            valeur = modif[1]

            epreuve = modif[2]
            compteur = partie.getCompteur(nom_compteur)
            if epreuve == "+":
                compteur.valeur += valeur
            elif epreuve == "-":
                compteur.valeur -= valeur
            else:
                compteur.valeur = valeur

        for condition in self.conditions:
            if condition.isObjet():
                if condition.supprime_utilisation:
                    nom_objet = condition.nom_objet
                    for elem in partie.objets.copy():

                        if elem.nom == nom_objet:
                            partie.objets.remove(elem)



    def getPageLien(self):
        """Recupere l'instance de page liée au numero de lien page si cette derniere a deja ete creee."""
        return self.livre.getPage(self.num_lien_page)




