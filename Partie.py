import Livre
import os
from Objet import *
from Compteur import *

parties = []

class Partie():

    def __init__(self,livre:Livre, titre:str):
        self.livre = livre
        self.titre = titre
        self.page_actuelle = self.livre.getPage(1)
        self.objets = []
        self.compteurs = []
        parties.append(self)

    def sauvegarder(self):
        if self.livre.titre not in os.listdir("parties"):
            os.mkdir("parties/"+self.livre.titre)

        if self.titre not in os.listdir("parties/"+self.livre.titre):
            os.mkdir("parties/"+self.livre.titre+"/"+self.titre)

        path = "parties/"+self.livre.titre+"/"+self.titre
        with open("parties/"+self.livre.titre+"/"+self.titre + "/page.txt", "w")as f:
            f.write(str(self.page_actuelle.numero))
            f.close()

        with open(path+ "/objets.txt","w") as f:
            f.close()

        for elem in self.objets:
            addTxt(elem.nom+";"+elem.path_image,path+"/objets.txt")


        with open(path+"/compteurs.txt","w")as f:
            f.close()

        for elem in self.compteurs:
            addTxt(elem.nom + ";" + str(elem.valeur),path+"/compteurs.txt")


    def getCompteur(self, nom_compteur:str):
        for compteur in self.compteurs:
            if compteur.nom == nom_compteur:
                return compteur

        return None


def getPartie(livre:Livre,nom_partie:str):
    for elem in parties:
        if elem.titre == nom_partie:
            return elem


    if nom_partie in os.listdir("parties/"+livre.titre):
        path = "parties/"+livre.titre+"/"+nom_partie
        p = Partie(livre,nom_partie)

        with open(path+"/page.txt","r")as f:
            p.page_actuelle = livre.getPage(int(f.read()))
            f.close()

        with open(path+"/objets.txt","r")as f:
            l = [elem.replace("\n","").split(";") for elem in f.readlines()]
            for elem in l:

                p.objets.append(Objet(elem[0],livre,elem[1],False))
            f.close()

        with open(path+"/compteurs.txt","r")as f:
            l = [elem.replace("\n","") for elem in f.readlines()]
            for elem in l:
                p.compteurs.append(Compteur(elem.split(";")[0],livre,float(elem.split(";")[1]),False))
            f.close()

    return p


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