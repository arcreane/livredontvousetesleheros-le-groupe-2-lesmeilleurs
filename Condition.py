from Option import Option
import random
from Compteur import Compteur
from Objet import Objet
import Partie

class Condition:

    def __init__(self, option: Option):
        self.option = option
        self.page = option.page
        self.livre = option.livre

    def isRespected(self, partie:Partie):
        pass

    def isDe(self):
        pass

    def isCompteur(self):
        pass

    def isObjet(self):
        pass


class ConditionDe(Condition):
    def __init__(self, option, valeur: int, epreuve: str, nb_de: int = 1, nb_faces: int = 6):
        Condition.__init__(self, option)
        self.valeur = valeur
        self.epreuve = epreuve
        self.nb_de = nb_de
        self.nb_faces = nb_faces
        self.passage = -1
        self.option.conditions.append(self)


    def isRespected(self,partie : Partie):
        """Renvoie un booléen suivant le fait que la condition soit respectée"""
        valeur = jetDe()

        if self.epreuve == ">":
            return self.valeur > valeur
        elif self.epreuve == "<":
            return self.valeur < valeur

    def isDe(self):
        return isinstance(self,ConditionDe)

    def isCompteur(self):
        return isinstance(self,ConditionCompteur)

    def isObjet(self):
        return  isinstance(self,ConditionObjet)



class ConditionCompteur(Condition):

    def __init__(self, option:Option, compteur: Compteur, valeur: int, epreuve=str):
        Condition.__init__(self, option)
        self.compteur = compteur
        self.valeur = valeur
        self.epreuve = epreuve
        self.option.conditions.append(self)

    def isRespected(self, partie:Partie):
        if self.epreuve == "=":
            return self.valeur == self.compteur.valeur
        elif self.epreuve == ">":
            return self.compteur.valeur > self.valeur
        elif self.epreuve == "<":
            return self.compteur.valeur < self.valeur


    def isDe(self):
        return isinstance(self,ConditionDe)

    def isCompteur(self):
        return isinstance(self,ConditionCompteur)

    def isObjet(self):
        return  isinstance(self,ConditionObjet)


class ConditionObjet(Condition):
    def __init__(self, option, nom_objet: str, supprime_utilisation:bool):
        Condition.__init__(self, option)
        self.nom_objet = nom_objet
        self.option.conditions.append(self)
        self.supprime_utilisation = supprime_utilisation

    def isRespected(self, partie :Partie):
        return self.nom_objet in [elem.nom for elem in partie.objets]


    def isDe(self):
        return isinstance(self,ConditionDe)

    def isCompteur(self):
        return isinstance(self,ConditionCompteur)

    def isObjet(self):
        return  isinstance(self,ConditionObjet)







def jetDe(nb=1, faces=6):
    L = [i for i in range(1, faces + 1)]
    somme = 0
    for i in range(nb):
        somme += random.choice(L)

    return somme

