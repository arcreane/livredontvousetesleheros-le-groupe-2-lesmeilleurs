import os
import shutil
from Livre import Livre
from Page import Page
from Option import Option
from Condition import *

livres = []
e_list = ["=",">","<"]


def projetExiste(nom_projet: str):
    """Renvoie True si un livre portant le nom rentré en argument existe"""
    return nom_projet in os.listdir("livres")


def pageExiste(nom_projet:str, numero_page:int):
    """Renvoie True si le numero de page entree en argument est dans le projet entre en argument"""
    if projetExiste(nom_projet):
        return str(numero_page) in os.listdir("livres/"+nom_projet + "/pages")


def optionExiste(nom_projet:str, numero_page:int, titre_option: str):
    """Renvoie True si l'option existe dans la pge et le projet entree en argument"""

    if pageExiste(nom_projet, numero_page):
        return titre_option in os.listdir("livres/" + nom_projet + "/pages/" + str(numero_page))




def createLivre(nom : str):
    """Permet de creer le dossier principal du livre et ses sous dossiers"""

    if not projetExiste(nom):
        os.mkdir("livres/"+nom)
        with open("livres/"+nom+"/objets.txt", "w") as f:
            f.close()
        with open("livres/"+nom+"/compteurs.txt", "w") as f:
            f.close()
        os.mkdir("livres/"+nom + "/pages")
        os.mkdir("livres/"+nom+"/pages/pages_fin")
        os.mkdir("livres/"+nom + "/sauvegardes")
        l = Livre(nom)
        livres.append(l)


    else:
        print("un projet possède deja ce nom")


def createPage(livre :Livre, numero: int, fin: bool = False):
    """Permet de creer les dossier et sous dossiers d'un page"""
    titre = livre.titre
    if projetExiste(titre):
        if fin:
            path = "livres/"+titre + "/pages/pages_fin"
            with open(path+"/"+str(numero)+".txt", "w") as f:
                f.close()
        if not pageExiste(titre, numero):
            os.mkdir("livres/"+titre + "/pages/" + str(numero))
            Page(numero, "", livre, fin)


        else:
            print("cette page existe deja")
    else:
        print("inexistant")


def createOption(page: Page, titre_option: str):
    """Permet de creer les dossiers et sous dossiers d'une option"""

    lien_page = 0
    titre = page.livre.titre
    numero_page = page.numero

    if projetExiste(titre):
        if pageExiste(titre, numero_page):
            if not optionExiste(titre, numero_page, titre_option):
                os.mkdir("livres/" + titre + "/pages/" + str(numero_page) + "/" + titre_option)
            else:
                print("Cette option existe deja")
                return
        else:
            print("La page a laquelle vous attachez cette option n'existe pas")
            return

        path = "livres/" + titre + "/pages/" + str(numero_page) + "/" + titre_option
        os.mkdir(path + "/condition")
        with open(path+"/gain_objet.txt","w")as f:
            f.close()
        with open(path+"/modif_compteur.txt","w")as f:
            f.close()

        Option(titre_option, page, lien_page, "")



def createPagetxt(page: Page, texte: str):
    """Permet d'associer un texte à une page"""

    nom_projet = page.livre.titre
    numero_page = page.numero

    path = "livres/"+nom_projet + "/pages/" + str(numero_page)
    with open(path + "/texte_page.txt", "w") as fichier:
        fichier.write(texte)
        fichier.close()

    page.texte = texte

    if page.is_fin:
        path = "livres/"+nom_projet + "/pages/pages_fin/"+str(numero_page)+".txt"
        with open(path,"w")as f:
            f.write(texte)
            f.close()


def createOptiontxt(option: Option, texte : str):
    """Permet d'assigner un texte au paragrphe passé en argument"""
    page = option.page
    nom_projet = page.livre.titre
    numero_page = page.numero
    titre_para = option.titre

    path = "livres/"+nom_projet + "/pages/" + str(numero_page) + "/" + titre_para
    with open(path + "/texte.txt", "w") as fichier:
        fichier.write(texte)
        fichier.close()
    option.texte = texte


def createLienPage(option: Option, numero_lien_page:int):
    """Permet de lié une option à un numero de page"""
    page = option.page
    livre = option.livre
    nom_projet = livre.titre
    numero_page = page.numero
    titre_option = option.titre

    path = "livres/"+nom_projet + "/pages/" + str(numero_page) + "/" + titre_option
    if numero_page != numero_lien_page:
        with open(path + "/lien_page.txt", "w") as fichier:
            fichier.write(str(numero_lien_page))
            fichier.close()
        option.num_lien_page = numero_lien_page

    else:
        print("on ne peut pas lier une option a la page à laquelle il apartient")


def deleteProjet(livre:Livre):
    """Efface un projet"""
    shutil.rmtree("livres/"+livre.titre)
    livres.remove(livre)
    del livre

def deleteOption(option:Option):
    """Permet de supprimer une option"""
    page = option.page
    page.options.remove(option)
    nom_projet = page.livre.titre
    path = "livres/" + nom_projet + "/pages/" + str(page.numero) + "/" + option.titre
    shutil.rmtree(path)
    del option


def deletePage(page:Page):
    """Permet de supprimer une page"""
    nom_projet = page.livre.titre
    path = "livres/"+nom_projet + "/pages/" + str(page.numero)
    shutil.rmtree(path)
    for option in page.options:
        del option
    del page




def createConditionDe(option: Option, valeur:int, epreuve: str, nb_de :int = 1, faces : int = 6):
    """Permet de creer une condition de d liee a une option"""
    page = option.page
    livre = option.livre
    nom_projet = livre.titre
    numero_page = page.numero
    titre_option = option.titre
    if epreuve in e_list:
        if valeur >= nb_de and valeur <= nb_de*faces:
            path = "livres/"+nom_projet + "/pages/"+str(numero_page)+"/"+titre_option+"/condition"

            addTxt(str(nb_de)+";"+str(faces)+";"+str(epreuve)+";"+str(valeur), path+"/condition_de.txt")
            ConditionDe(option, valeur, epreuve, nb_de, faces)



def createConditionCompteur(option: Option, compteur:Compteur, valeur: int, epreuve: str):
    """Permet de creer une condition de compteur lie a une option"""
    page = option.page
    livre = option.livre
    nom_projet = livre.titre
    numero_page = page.numero
    titre_option = option.titre

    if epreuve in e_list:
        path = "livres/"+nom_projet + "/pages/"+str(numero_page)+"/"+titre_option+"/condition"
        addTxt(compteur.nom+";"+str(valeur)+";"+epreuve,path+"/condition_compteur.txt")
        ConditionCompteur(option, compteur, valeur, epreuve)


def createConditionObjet(option: Option, nom_objet:str, supprime_utilisation):
    """Permet de creer une condition d'objet lie a une option"""
    page = option.page
    livre = option.livre
    nom_projet = livre.titre
    numero_page = page.numero
    titre_option = option.titre

    path = "livres/"+nom_projet + "/pages/"+str(numero_page)+"/"+titre_option+"/condition"
    addTxt(nom_objet+";"+str(supprime_utilisation),path+"/condition_objet.txt")
    ConditionObjet(option, nom_objet,supprime_utilisation)




def addObjet(livre:Livre, nom_objet, path_image):
    """Permet de creer un objet"""
    path = "livres/"+livre.titre + "/objets.txt"
    addTxt(nom_objet+";"+path_image,path)
    Objet(nom_objet,livre,path_image)


def addCompteur(nom_compteur:str, valeur: float, livre: Livre):
    """Permet de creer un compteur"""
    path = "livres/"+livre.titre + "/compteurs.txt"
    addTxt(nom_compteur+";"+str(valeur),path)
    Compteur(nom_compteur,livre,valeur)


def addGainObjet(option: Option, nom_objet:str, path_image):
    titre_livre = option.livre.titre
    num_page = option.page.numero
    path = "livres/"+titre_livre+"/pages/"+str(num_page)+"/"+option.titre+"/gain_objet.txt"
    if nom_objet not in option.gain_objet:
        addTxt(nom_objet+";"+path_image, path)
        option.gain_objet.append([nom_objet,path_image])


def addModifCompteur(option: Option, nom_compteur: str, valeur: float, epreuve:str):
    if nom_compteur in [elem.nom for elem in option.livre.compteurs]:

        option.modif_compteur.append([nom_compteur,valeur,epreuve])

        path = "livres/"+option.livre.titre+"/pages/"+str(option.page.numero)+"/"+option.titre+"/modif_compteur.txt"
        addTxt(nom_compteur+";"+str(valeur)+";"+epreuve,path)



def loadLivre(nom_livre: str):
    """Permet de charger un livre existant a partir de son nom"""
    if projetExiste(nom_livre):

        livre = Livre(nom_livre)
        livres.append(livre)
        loadObjet(nom_livre)
        loadCompteur(nom_livre)


        pages = os.listdir("livres/"+nom_livre+"/pages")
        try:
            pages.remove("pages_fin")
        except Exception:
            pass

        #chargement des pages, options et conditions
        for page in pages:
            path = "livres/"+nom_livre+"/pages/"+ page
            try:
                with open(path+"/texte_page.txt","r")as f:
                    txt = f.read()
                    f.close()
            except Exception:
                txt = ""
            p = Page(int(page),txt,livre,str(page)+".txt" in os.listdir("livres/"+nom_livre+"/pages/pages_fin"))

            options = os.listdir(path)

            try:
                options.remove("texte_page.txt")
            except Exception:
                pass

            #chargement des options et conditions

            for option in options:

                path = "livres/"+nom_livre+"/pages/"+ page + "/" + option
                try:
                    with open(path + "/texte.txt", "r")as f:
                        txt = f.read()
                        f.close()
                except Exception:
                    txt = ""

                #chargement des liens des pages
                try:
                    with open(path + "/lien_page.txt", "r")as f:
                        lien_page = f.read()
                        lien_page = int(lien_page)
                        f.close()
                except Exception:
                    lien_page = 0

                Option(option, p, lien_page, txt)
                option = p.getOption(option)

                # chargement des gains d'objets
                try:

                    with open(path + "/gain_objet.txt", "r")as f:
                        l = f.readlines()
                        L = []
                        for elem in l:
                            L.append(elem.replace("\n","").split(";"))
                        option.gain_objet = L[:]
                        f.close()
                except Exception:
                    pass

                #chargement des modifications de compteurs

                try:
                    with open(path+"/modif_compteur.txt","r")as f:
                        l = f.readlines()
                        L = []
                        L.clear()
                        for elem in l:
                            L.append(elem.split(";"))

                        for elem in L:
                            option.modif_compteur.append([elem[0],float(elem[1]),elem[2].replace("\n","")])



                        f.close()


                except Exception:
                    pass

                path = path+"/condition"



                # chargement des Conditions de de
                try:
                    with open(path+"/condition_de.txt","r") as f:
                        l = f.readlines()
                        l2 = []
                        for elem in l:
                            l2.append(elem.replace("\n","").split(";"))


                        for condition in l2:

                            ConditionDe(option,int(condition[3]),condition[2],int(condition[0]),int(condition[1]))
                        f.close()


                except Exception:
                    pass

                # chargement des Conditions de compteurs
                try:
                    with open(path+"/condition_compteur.txt","r") as f:
                        l = f.readlines()
                        l2 = []
                        for elem in l:
                            l2.append(elem.replace("\n","").split(";"))
                        for condition in l2:
                            ConditionCompteur(option,livre.getCompteur(condition[0]),float(condition[1]),
                                              condition[2])
                        f.close()
                except Exception:
                    pass

                # chargement des Conditions d'objets
                try:
                    with open(path+"/condition_objet.txt","r") as f:
                        l = f.readlines()
                        l2 = []
                        for elem in l:
                            l2.append(elem.replace("\n","").split(";"))
                        for condition in l2:
                            ConditionObjet(option,condition[0],condition[1])
                        f.close()
                except Exception:
                    pass



def loadObjet(nom_livre:str):
    """Permet de cHarger les objet d'un livre"""
    path = "livres/"+nom_livre + "/objets.txt"
    with open(path, "r")as f:
        l = [elem.replace("\n","").split(";") for elem in f.readlines()]
        f.close()

    for elem in l:
        Objet(elem[0], getLivre(nom_livre),elem[1])


def loadCompteur(nom_livre:str):
    """Permet de charger les compteurs d'un livre"""
    path = "livres/"+nom_livre + "/compteurs.txt"
    l2 = []
    with open(path, "r")as f:
        l = f.readlines()
        for elem in l:
            l2.append(elem.replace("\n", "").split(";"))
    f.close()

    for elem in l2:
        Compteur(elem[0], getLivre(nom_livre), float(elem[1]))



def getLivre(nom_livre : str):
    """Permet de recuperer une instance de livre à partir de son nom"""
    for livre in livres:
        if livre.titre == nom_livre:
            return livre
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


def getListNomLivre():
    return os.listdir("livres")


def getListPage(livre: Livre):
    L = []
    titre = livre.titre
    for elem in os.listdir("livres/"+titre+"/pages"):
        if elem != "pages_fin":
            L.append(int(elem))
    L.sort()
    return L