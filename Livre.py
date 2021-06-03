import os


class Livre():
    def __init__(self, titre: str):
        self.titre = titre
        self.pages = []
        self.compteurs = []
        self.objets = []
        self.pages_fin = []

    def sauvegarder(self):
        """Permet de sauvegarder l'ensemble des information sur un livre"""

        path = "livres/"+self.titre+"/compteurs.txt"
        with open(path,"w") as f:
            f.close()
        for compteur in self.compteurs:
            addTxt(compteur.nom+";"+str(compteur.valeur),path)

        path = "livres/" + self.titre + "/objets.txt"
        with open(path, "w") as f:
            f.close()
        for objet in self.objets:
            addTxt(objet.nom+";"+objet.path_image,path)


        for page in self.pages:
            for option in page.options:
                #gain objets
                path = "livres/" + self.titre + "/pages/" + str(page.numero) + "/" + option.titre + "/gain_objet.txt"
                with open(path, "w")as f:
                    f.close()
                for obj in option.gain_objet:
                    addTxt(obj[0]+";"+obj[1],path)

                #modif compteurs
                path = "livres/" + self.titre + "/pages/" + str(page.numero) + "/" + option.titre + "/modif_compteur.txt"
                with open(path, "w")as f:
                    f.close()
                for modif in option.modif_compteur:
                    addTxt(modif[0]+";"+str(modif[1])+";"+modif[2],path)

                #conditions de
                path = "livres/" + self.titre + "/pages/" + str(page.numero) + "/" + option.titre+"/condition/condition_de.txt"
                try:
                    with open(path,"r") as f:
                        f.close()
                    with open(path,"w")as f:
                        f.close()
                    for elem in option.conditions:
                        if elem.isDe():
                            addTxt(str(elem.nb_de)+";"+str(elem.nb_faces)+";"+elem.epreuve+";"+str(elem.valeur),path)
                except Exception:
                    pass

                #condition Objet
                path = "livres/" + self.titre + "/pages/" + str(page.numero) + "/" + option.titre+"/condition/condition_objet.txt"
                try:
                    with open(path,"r")as f:
                        f.close()
                    with open(path,"w")as f:
                        f.close()
                    for elem in option.conditions:
                        if elem.isObjet():
                            addTxt(elem.nom_objet+";"+str(elem.supprime_utilisation))
                except Exception:
                    pass

                #condition compteur
                path = "livres/" + self.titre + "/pages/" + str(
                    page.numero) + "/" + option.titre + "/condition/condition_compteur.txt"
                try:
                    with open(path, "r")as f:
                        f.close()
                    with open(path, "w")as f:
                        f.close()
                    for elem in option.conditions:
                        if elem.isCompteur():
                            addTxt(elem.compteur.nom + ";" + str(elem.valeur)+";"+elem.epreuve)
                except Exception:
                    pass













    def trouveProbleme(self):
        """Permet de detecter et de stocker dans des listes les numero des pages menant a un cul de sac
        ainsi que les pages qui font l'objet de boucle"""

        L = []
        boucle = []
        culDeSac = []

        for page in self.pages:
            for option in page.options:
                if option.num_lien_page not in L:
                    L.append(option.num_lien_page)
                else:
                    boucle.append(option.num_lien_page)

                if option.getPageLien() == None:
                    culDeSac.append(option.num_lien_page)

        return boucle, culDeSac


    def getPage(self, numero_page: int):
        """permet de recupérer une instance de page a partir de son numero"""
        for page in self.pages:
            if page.numero == numero_page:
                return page

        return None

    def getCompteur(self, nom: str):
        """Permet de recuperer une instance de compteur a partir de son nom"""
        for compteur in self.compteurs:
            if compteur.nom == nom:
                return compteur
        return None

    def getObjet(self, nom: str):
        """Permet de recuperer une instance d'objet a partir de son nom"""
        for objet in self.objets:
            if objet.nom == nom:
                return objet

        return None

def addTxt(texte:str, fichier:str):
    chaine = ""
    try:
        with open(fichier,"r")as f:
            chaine = f.read()+"\n"
            f.close()
    except Exception:
        pass

    if chaine == "\n":
        chaine = ""
    with open(fichier,"w") as f:
        f.write(chaine+texte)
        f.close()
