from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from functools import partial
from CreateSave import *
from Partie import *
import shutil
import sys
import random


def Verifcara(chaine1 : str):

    liste_1 = ["/", ":", "*", "?", "|", ";", "<", ">", '"', "\n", "\t", '"', "\\"]

    for char in chaine1:
        if char in liste_1:
            return False

    return True

def menuChoisirLivre(win):
    """Permet de charger le menu de choix de livre"""
    win.clear_w()
    win.choisirLivre()

#choisir livre
def valideLivre(win):
    """Permet de choisir le livre auquel on souhaite jouer parmis la liste"""
    l = win.listWidget.selectedItems()
    if l != []:
        titre = l[0].text()
        loadLivre(titre)
        livre = getLivre(titre)
        menuCommencer(win,livre)
    else:
        msgBoxSelect()


#Menu commencer
def menuCommencer(win,livre):
    """Charge le menu de choix/cretaion de partie"""
    win.clear_w()
    win.menuCommencer(livre)


def bcreerPartie(win,livre:Livre,lineEdit:QLineEdit):
    """Fonction appelée apres l'appui du bouton creer pour creer une partie"""
    titre = lineEdit.text()
    titre = titre.strip()
    existe = False
    if livre in os.listdir("parties"):
        if titre in os.listdir("parties/"+livre.titre):
            existe = True

    if not existe:
        if titre != "":
            if Verifcara(titre):
                p = Partie(livre,titre)
                p.objets = livre.objets.copy()
                p.compteurs = livre.compteurs.copy()

                p.sauvegarder()
            else:
                msgBoxCaractereInterdit()
        else:
            msgBoxExiste()
    else:
        msgBoxExiste()

    actualiseListCommencer(win,livre)
    lineEdit.setText("")



def bsupprimerPartie(win,livre:Livre):
    """Permet de supprimer une partie"""
    l = win.listWidget.selectedItems()
    if l != []:
        nom_partie = l[0].text()
        shutil.rmtree("parties/"+livre.titre+"/"+nom_partie)
        actualiseListCommencer(win,livre)
    else:
        msgBoxSelect()





def actualiseListCommencer(win,livre:Livre):
    """Pemret d'actualiser la liste des partie disponibles"""
    win.listWidget.clear()
    if livre.titre in os.listdir("parties"):
        for elem in os.listdir("parties/"+livre.titre):
            win.listWidget.addItem(elem)


def bvaliderPartie(win,livre:Livre):
    """Permet de lancer le jeu si une partie est selectionnée dans la liste"""
    l = win.listWidget.selectedItems()
    if l != []:
        nom_partie = l[0].text()

        partie = getPartie(livre,nom_partie)
        menuPage(win,partie)
    else:
        msgBoxSelect()


#Menu Page
def menuPage(win, partie:Partie):
    """Permet de charger le menu des pages"""
    win.clear_w()
    win.menuPage(partie)


def verifConditions(win, partie:Partie, option:Option):
    """Permet de vérifier sile joueur vérifie les conditions de passge qu'on a imposé au passge de l'option"""

    passage = True #creation d'une variable passage qui determinera la possibilié de passer
    l = []

    #Verification des condition de compteur
    for condition in option.conditions:
        if condition.isCompteur():
            if not condition.isRespected(partie):
                passage = False

        #verification des conditions d'objets
        elif condition.isObjet():
            if not condition.isRespected(partie):
                passage = False

        elif condition.isDe():
            l.append(condition)

    #pour les dés
    compteur = 0
    for condition in l:
        if condition.passage == -1:
            compteur += 1
        elif condition.passage == 0:
            compteur -= 1

    #declenché si aucun dé n'a été tiré
    if compteur == len(l) and compteur!=0:
        msgBox("Vous Devez d'abord tirer les dés pour essayer de passer")
        return

    #déclenché si tous les dés ont étés tirés et que le joueur à échoué
    elif -compteur == len(l) and compteur!=0:
        msgBox("Vous avez raté le jet de dé. Vous ne pouvez donc pas passer")
        return

    #
    if option.conditions != []:
        if passage:
            if len(option.conditions) != len(l):
                #affichage des conséquences de l'action
                win.otherWindow(1,partie,option)

            else:
                pageSuivante(win, partie, option)

        else:
            #affichages des raison de l'impossibilité du passage
            win.otherWindow(2,partie,option)
    else:
        pageSuivante(win,partie,option)


def okWindow(win, partie:Partie , option:Option, suivant:bool):
    """Permet de charger la page suivante après l'appui sur le bouton ok de la seconde fenetre"""
    win.w.close()
    if suivant:
        pageSuivante(win,partie,option)


def pageSuivante(win, partie:Partie, option:Option):
    """Permet d'afficher la page suivante"""

    page_suivante = option.getPageLien()

    option.actionClic(partie)
    if option.gain_objet != []:
        msgBox("Vous venez de gagnez un ou plusieurs objets! Consultez votre inventaire")
    partie.sauvegarder()
    chargerPage(win,partie,page_suivante)


def lancerDe(win,nb_de,nb_faces,option):
    """Permet d'effectuer des lancés de dés y compris multiples"""
    l = win.w.l
    indice = win.w.indice
    l2 = [i for i in range(nb_faces)]

    valeur = 0
    for i in range(nb_de):
        valeur += random.choice(l2)
    win.w.label_4.setText("Obtenu :"+str(valeur))
    if l[indice].epreuve == ">":

        if l[indice].valeur < valeur:
            win.w.pushButton_2.setText("Fermer")
            win.w.label_5.setText("Reussi")
            for condition in option.conditions:
                if l[indice] == condition:
                    condition.passage = 1
                    return

        elif len(l)-1 == indice:
            win.w.pushButton_2.setText("Fermer")
            win.w.label_5.setText("Raté")
            for condition in option.conditions:
                if l[indice] == condition:
                    condition.passage = 0
                    break

        else:
            win.w.pushButton_2.setText("Retenter sa chance")
            for condition in option.conditions:
                if l[indice] == condition:
                    condition.passage = 0
                    break

    if l[indice].epreuve == "<":
        if l[indice].valeur > valeur:
            win.w.pushButton_2.setText("Fermer")
            win.w.label_5.setText("Reussi")
            for condition in option.conditions:
                if l[indice] == condition:
                    condition.passage = 1
                    return

        elif len(l) - 1 == indice:
            win.w.pushButton_2.setText("Fermer")
            win.w.label_5.setText("Raté")
            for condition in option.conditions:
                if l[indice] == condition:
                    condition.passage = 0
                    break

        else:
            win.w.pushButton_2.setText("Retenter sa chance")
            for condition in option.conditions:
                if l[indice] == condition:
                    condition.passage = 0
                    break

    else:
        if l[indice].valeur == valeur:
            win.w.pushButton_2.setText("Fermer")
            win.w.label_5.setText("Reussi")
            for condition in option.conditions:
                if l[indice] == condition:
                    condition.passage = 1
                    return

        elif len(l)-1 == indice:
            win.w.pushButton_2.setText("Fermer")
            win.w.label_5.setText("Raté")
            for condition in option.conditions:
                if l[indice] == condition:
                    condition.passage = 0
                    break

        else:
            win.w.pushButton_2.setText("Retenter sa chance")
            for condition in option.conditions:
                if l[indice] == condition:
                    condition.passage = 0
                    break

    win.w.indice += 1



def retenterDe(win):
    """Permet d'actualiser différents label après l'appui sur les boutons"""
    win.w.label_2.setText("Objetctif: " + win.w.l[win.w.indice].epreuve + str(win.w.l[win.w.indice].valeur))
    win.w.pushButton_2.setText("En attente de jet")
    win.w.label.setText("Jets de dé n°" + str(win.w.indice + 1))


def boutonVariable(win):
    """Permet d'effectuer différentes actions en fonction du texte du bouton"""
    if win.w.pushButton_2.text() == "Fermer":
        win.w.close()
    elif win.w.pushButton_2.text() == "Retenter sa chance":
        retenterDe(win)


def boutonVariable2(win,nb_de,nb_faces,option:Option):
    """Permet d'effectuer une action uniquement si le texte du bouton est "En attente de jets" """
    if win.w.pushButton_2.text() == "En attente de jet":
        lancerDe(win,nb_de,nb_faces,option)


def msgBox(texte:str):
    """Permet d'afficher un message en cas de non selection"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(texte)
    msg.setWindowTitle("Information")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec()

def msgBoxExiste(txt="L'élément que vous tentez de créer existe deja ou ne possède pas de nom. Veillez choisir un nom ou un numéro différent."):
    """Affiche un message indiquant l'impossibilité de créer un objet en raison d'une entrée invalide"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(txt)
    msg.setWindowTitle("Element deja existant")
    msg.setStandardButtons(QMessageBox.Ok)

    msg.exec()


def msgBoxSelect():
    """Permet d'afficher un message en cas de non selection"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Veuillez selctionner un élément dans le liste avant d'effectuer cette action")
    msg.setWindowTitle("Selection manquante")
    msg.setStandardButtons(QMessageBox.Ok)

    msg.exec()


def msgBoxCaractereInterdit():
    """Affich une msgBox renseignant les caractères non autorisés"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Certains caractères que vous avez entrez ne sont pas autorisés. Caractère non authorisés : \/*><;:|?\" ainsi que les entrées et les tabulations")
    msg.setWindowTitle("Page inexistante")
    msg.setStandardButtons(QMessageBox.Ok)

    msg.exec()


#inventaire
def menuInventaire(win,partie:Partie):
    """Permet de charger le menu de l'inventaire"""
    win.clear_w()
    win.inventaire(partie)



class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.widget_list = []
        self.resize(971, 702)

        self.window_lay = QVBoxLayout()
        self.window_lay.setObjectName("window_lay")
        self.setLayout(self.window_lay)
        self.setWindowTitle("HistoryMaker")
        self.setWindowIcon(QtGui.QIcon("logo.png"))

    def otherWindow(self, type:int, partie:Partie, option:Option):
        self.w = SecondWindow(self)
        if type == 0:
            compteur = 0
            l = []
            for condition in option.conditions:
                if condition.isDe():
                    l.append(condition)

            for elem in l:
                if elem.passage == -1:
                    compteur+=1

            if compteur == len(l):
                self.w.jetDeDes(partie,option)
            else:
                msgBox("Vous avez déja tiré les dés")
                return
        elif type == 1:
            self.w.respecte(partie,option)
        else:

            self.w.nonRespecte(partie,option)

        self.w.show()


    def clear_w(self):
        """Permet de vider un fenetre de l'entierté de ses elements afin de changer son contenu"""
        for elem in self.widget_list:
            elem.setParent(None)
        nb = self.window_lay.count()

        for i in range(nb):
            self.window_lay.removeItem(self.window_lay.itemAt(0))

        self.widget_list = []


    def choisirLivre(self):
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout.setSpacing(30)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label = QLabel()
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.label)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        self.widget_list.append(self.line)

        self.verticalLayout.addWidget(self.line)

        self.listWidget = QListWidget()
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.widget_list.append(self.listWidget)

        for elem in os.listdir("livres"):
            self.listWidget.addItem(elem)


        self.pushButton = QPushButton()
        self.pushButton.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.widget_list.append(self.pushButton)
        self.pushButton.clicked.connect(partial(valideLivre,self))

        self.label.setText("Choisir un livre")
        self.pushButton.setText("Valider")

        self.verticalLayout.addWidget(self.pushButton, 0, QtCore.Qt.AlignHCenter)

        self.window_lay.addLayout(self.verticalLayout)

    def menuPage(self,partie:Partie):

        self.verticalLayout_17 = QVBoxLayout()
        self.verticalLayout_17.setContentsMargins(50, 20, 50, 20)
        self.verticalLayout_17.setSpacing(20)
        self.verticalLayout_17.setObjectName("verticalLayout_17")

        self.pushButton = QPushButton()
        self.pushButton.setMinimumSize(QtCore.QSize(150, 30))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_17.addWidget(self.pushButton, 0, QtCore.Qt.AlignRight)
        self.widget_list.append(self.pushButton)
        self.pushButton.clicked.connect(partial(menuInventaire,self,partie))

        self.label = QLabel()
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_17.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.label)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_17.addWidget(self.line)
        self.widget_list.append(self.line)

        font = QtGui.QFont()
        font.setPointSize(11)
        self.plainTextEdit = QPlainTextEdit()
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout_17.addWidget(self.plainTextEdit)
        self.widget_list.append(self.plainTextEdit)
        self.plainTextEdit.setPlainText(partie.page_actuelle.texte)

        self.line_2 = QFrame()
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_17.addWidget(self.line_2)
        self.widget_list.append(self.line_2)

        font = QtGui.QFont()
        font.setPointSize(12)

        self.label_2 = QLabel()
        self.label_2.setObjectName("label_2")
        self.label_2.setFont(font)
        self.verticalLayout_17.addWidget(self.label_2, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.label_2)

        self.tabWidget = QTabWidget()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")
        self.widget_list.append(self.tabWidget)

        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout = QVBoxLayout(self.tab)
        self.widget_list.append(self.tab)

        chargerPage(self,partie,partie.page_actuelle)

        self.pushButton.setText("Inventaire")
        self.label.setText("Page "+str(partie.page_actuelle.numero))
        self.label_2.setText("Options")

        self.verticalLayout_17.addWidget(self.tabWidget)

        self.window_lay.addLayout(self.verticalLayout_17)

    def menuCommencer(self,livre : Livre):
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_3.setSpacing(30)
        self.verticalLayout_3.setObjectName("verticalLayout_3")


        self.pushButton_4 =QPushButton()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout_3.addWidget(self.pushButton_4, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.pushButton_4)
        self.pushButton_4.clicked.connect(partial(menuChoisirLivre,self))

        self.label = QLabel()
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.label)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_3.addWidget(self.line)
        self.widget_list.append(self.line)


        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_2.setSpacing(20)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(50)
        self.verticalLayout.setObjectName("verticalLayout")



        self.label_3 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.widget_list.append(self.label_3)


        self.label_4 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.widget_list.append(self.label_4)


        self.lineEdit = QLineEdit()
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.widget_list.append(self.lineEdit)


        self.pushButton_2 = QPushButton()
        self.pushButton_2.setMinimumSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.pushButton_2)
        self.pushButton_2.clicked.connect(partial(bcreerPartie,self,livre,self.lineEdit))


        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.line_2 = QFrame()
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_2.addWidget(self.line_2)
        self.widget_list.append(self.line_2)


        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_2.setSpacing(20)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.label_2 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.widget_list.append(self.label_2)


        self.listWidget = QListWidget()
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_2.addWidget(self.listWidget)
        self.widget_list.append(self.listWidget)

        actualiseListCommencer(self,livre)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setSpacing(15)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.pushButton = QPushButton()
        self.pushButton.setMinimumSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.pushButton)
        self.pushButton.clicked.connect(partial(bvaliderPartie,self,livre))


        self.pushButton_3 = QPushButton()
        self.pushButton_3.setMinimumSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.pushButton_3)
        self.pushButton_3.clicked.connect(partial(bsupprimerPartie,self,livre))

        self.pushButton_4.setText("Retour")
        self.label.setText("Choisir une partie")
        self.label_3.setText("Créer une nouvelle partie")
        self.label_4.setText("Titre de la nouvelle partie ")
        self.pushButton_2.setText("Creer")
        self.label_2.setText("Charger une partie")
        self.pushButton.setText("Valider")
        self.pushButton_3.setText("Supprimer")

        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.window_lay.addLayout(self.verticalLayout_3)


    def inventaire(self, partie:Partie):
        self.lay_list = []

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout.setSpacing(30)
        self.verticalLayout.setObjectName("verticalLayout")

        self.pushButton = QPushButton()
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.pushButton)
        self.pushButton.clicked.connect(partial(menuPage,self,partie))

        self.label = QLabel()
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.label)


        self.label_2 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.label_2)


        self.scrollArea = QScrollArea()
        self.scrollArea.setMinimumSize(QtCore.QSize(531, 221))
        self.scrollArea.setMaximumSize(QtCore.QSize(531, 221))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 529, 219))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout_3")
        self.lay_list.append(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.scrollArea)
        self.scrollAreaWidgetContents


        self.label_3 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.label_3)

        self.pushButton.setText("Retour")
        self.label.setText("Inventaire")
        self.label_2.setText("Objets")
        self.label_3.setText("Compteurs")

        self.listWidget = QListWidget()
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.window_lay.addLayout(self.verticalLayout)
        self.widget_list.append(self.listWidget)
        listObjet(self,partie)


        for elem in partie.compteurs:
            self.listWidget.addItem(elem.nom+'\t=\t'+str(elem.valeur))

class SecondWindow(QWidget):
    def __init__(self,w):
        QWidget.__init__(self)
        self.widget_list = []
        self.resize(655, 339)
        self.w = w

        self.window_lay = QVBoxLayout()
        self.window_lay.setObjectName("window_lay")
        self.setLayout(self.window_lay)
        self.setWindowTitle("Informations")

    def clear_w(self):
        """Permet de vider un fenetre de l'entierté de ses elements afin de changer son contenu"""
        for elem in self.widget_list:
            elem.setParent(None)
        nb = self.window_lay.count()

        for i in range(nb):
            self.window_lay.removeItem(self.window_lay.itemAt(0))

        self.widget_list = []

    def jetDeDes(self, partie:Partie,option:Option):
        self.l = []
        self.indice = 0

        for condition in option.conditions:
            if condition.isDe():
                self.l.append(condition)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.label = QLabel()
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.label_2 = QLabel()
        self.label_2.setMinimumSize(QtCore.QSize(174, 24))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.widget_list.append(self.label_2)

        self.pushButton = QPushButton()
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.widget_list.append(self.pushButton)
        self.pushButton.clicked.connect(partial(boutonVariable2,self.w,self.l[self.indice].nb_de,self.l[self.indice].nb_faces,option))


        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 =QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.label_4 = QLabel()
        self.label_4.setMinimumSize(QtCore.QSize(173, 24))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.widget_list.append(self.label_4)

        self.pushButton_2 = QPushButton()
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_2.addWidget(self.pushButton_2)
        self.widget_list.append(self.pushButton_2)
        self.pushButton_2.clicked.connect(partial(boutonVariable,self.w))

        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.label_3 = QLabel()
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")

        self.verticalLayout_3.addWidget(self.label_3)

        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_5 = QLabel()
        self.label_5.setObjectName("label_5")
        self.label_5.setFont(font)
        self.verticalLayout_3.addWidget(self.label_5, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.label_5)

        self.widget_list.append(self.label_3)

        self.window_lay.addLayout(self.verticalLayout_3)

        self.label.setText("Jets de dé n°"+str(self.indice+1))

        self.label_2.setText("Objetctif: "+self.l[self.indice].epreuve+str(self.l[self.indice].valeur))
        self.pushButton.setText("Lancer les dés")
        self.label_4.setText("Obtenu :")

        if self.indice -1 == len(self.l):
            self.pushButton_2.setText("Fermer")
        else:
            self.pushButton_2.setText("En attente de jet")

    def nonRespecte(self,partie:Partie,option:Option):

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_3.setSpacing(20)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.label = QLabel()
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setSpacing(15)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")


        self.label_2 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.widget_list.append(self.label_2)
        self.listWidget = QListWidget()
        self.listWidget.setMinimumSize(QtCore.QSize(288, 89))
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.widget_list.append(self.listWidget)
        for condition in option.conditions:
            if condition.isCompteur():
                if not condition.isRespected(partie):
                    self.listWidget.addItem(condition.compteur.nom+" "+condition.epreuve+str(condition.valeur)+"    Actuelle: "
                                            +str(partie.getCompteur(condition.compteur.nom).valeur))
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3 = QLabel()
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.widget_list.append(self.label_3)

        self.listWidget_2 = QListWidget()
        self.listWidget_2.setMinimumSize(QtCore.QSize(288, 89))
        self.listWidget_2.setObjectName("listWidget_2")
        self.verticalLayout_2.addWidget(self.listWidget_2)
        self.widget_list.append(self.listWidget_2)
        for condition in option.conditions:
            if condition.isObjet():
                if not condition.isRespected(partie):
                    self.listWidget_2.addItem("Objet Manquant: \t"+condition.nom_objet)

        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.pushButton = QPushButton()
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_3.addWidget(self.pushButton, 0, QtCore.Qt.AlignRight)
        self.widget_list.append(self.pushButton)
        self.pushButton.clicked.connect(partial(okWindow,self.w,partie,option,False))

        self.window_lay.addLayout(self.verticalLayout_3)

        self.label.setText("Passage impossibe")
        self.label_2.setText("Compteurs")
        self.label_3.setText("Objets Manquants")
        self.pushButton.setText("Ok")

    def respecte(self, partie:Partie, option:Option):

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_3.setSpacing(20)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.label = QLabel()
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setSpacing(15)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.label_2 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.widget_list.append(self.label_2)

        self.listWidget = QListWidget()
        self.listWidget.setMinimumSize(QtCore.QSize(288, 89))
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.widget_list.append(self.listWidget)


        for elem in option.modif_compteur:
            self.listWidget.addItem(elem[0]+elem[2]+str(elem[1]))


        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.label_3 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.widget_list.append(self.label_3)

        self.listWidget_2 = QListWidget()
        self.listWidget_2.setMinimumSize(QtCore.QSize(288, 89))
        self.listWidget_2.setObjectName("listWidget_2")
        self.verticalLayout_2.addWidget(self.listWidget_2)
        self.widget_list.append(self.listWidget_2)


        for elem in option.gain_objet:
            self.listWidget_2.addItem("Gain: \t"+elem)

        for condition in option.conditions:
            if condition.isObjet():
                if condition.supprime_utilisation:
                    self.listWidget_2.addItem("Perte: \t"+condition.nom_objet)


        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.pushButton = QPushButton()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_3.addWidget(self.pushButton, 0, QtCore.Qt.AlignRight)
        self.widget_list.append(self.pushButton)
        self.pushButton.clicked.connect(partial(okWindow,self.w,partie,option,True))

        self.label.setText("Conséquences de l\'action")
        self.label_2.setText("Compteurs")
        self.label_3.setText("Objets")
        self.pushButton.setText("Ok")
        self.window_lay.addLayout(self.verticalLayout_3)


def chargerPage(win,partie:Partie, page:Page):
    """Permet de charger une page. On crée ici les tab qui permettront la naviqation entre les option"""
    partie.page_actuelle = page
    win.plainTextEdit.setPlainText(page.texte)
    win.tabWidget.clear()
    win.label.setText("Page "+str(page.numero))

    if not page.is_fin:
        for option in page.options:
            passage = True
            conditionDe = []
            conditionObjet = []
            conditionCompteur = []



            for condition in option.conditions:
                if condition.isDe():
                    conditionDe.append(condition)
                    condition.passage = -1
                elif condition.isObjet():
                    conditionObjet.append(condition)
                elif condition.isCompteur():
                    conditionCompteur.append(condition)

            tab = QWidget()
            tab.setObjectName("tab")

            texte = option.texte+"\n"

            verticalLayout = QVBoxLayout(tab)
            verticalLayout.setObjectName("verticalLayout")
            horizontalLayout = QHBoxLayout()
            horizontalLayout.setContentsMargins(10, 10, 10, 10)
            horizontalLayout.setSpacing(10)
            horizontalLayout.setObjectName("horizontalLayout")

            plainTextEdit_3 = QPlainTextEdit(tab)
            plainTextEdit_3.setReadOnly(True)
            plainTextEdit_3.setObjectName("plainTextEdit_3")
            horizontalLayout.addWidget(plainTextEdit_3)


            if conditionObjet != [] or conditionCompteur != []:
                x = 0
                if conditionObjet == []:
                    x = 1
                if conditionCompteur == []:
                    x = 2

                if x == 1 or x == 0:
                    if option.isConditionCompteur(partie):
                        texte += "\n Vos compteurs respectent les conditions"
                    else:
                        texte += "\nCertains de vos compteurs ne respectent pas les conditions pour choisr cette action"
                        passage = False
                else:
                    if option.isConditionObjet(partie):
                        texte += "\nVous avez les objets necessaires pour passer"
                    else:
                        texte +="\nIl vous manque un objet pour passer"
                        passage = False


                if x == 0:
                    if option.isConditionObjet(partie):
                        texte += "\nVous avez les objets necessaires pour passer"
                    else:
                        texte += "\nIl vous manque un objet pour passer"
                        passage = False


            verticalLayout.addLayout(horizontalLayout)
            horizontalLayout_6 = QHBoxLayout()
            horizontalLayout_6.setContentsMargins(10, 10, 10, 10)
            horizontalLayout_6.setSpacing(10)
            horizontalLayout_6.setObjectName("horizontalLayout_6")

            font = QtGui.QFont()
            font.setPointSize(11)

            if not passage:
                font.setStrikeOut(True)
            else:
                font.setStrikeOut(False)

            pushButton = QPushButton(tab)
            pushButton.setMinimumSize(QtCore.QSize(150, 30))
            pushButton.setObjectName("pushButton")
            pushButton.setFont(font)
            horizontalLayout_6.addWidget(pushButton, 0, QtCore.Qt.AlignLeft)
            pushButton.setText("Choisir cette option")
            pushButton.clicked.connect(partial(verifConditions,win,partie,option))



            if conditionDe != []:
                pushButton_2 = QPushButton(tab)
                pushButton_2.setMinimumSize(QtCore.QSize(150, 30))
                pushButton_2.setObjectName("pushButton_2")
                horizontalLayout_6.addWidget(pushButton_2, 0, QtCore.Qt.AlignLeft)
                pushButton_2.setText("lancer les dés")
                pushButton_2.clicked.connect(partial(win.otherWindow,0,partie,option))

            spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            horizontalLayout_6.addItem(spacerItem1)
            verticalLayout.addLayout(horizontalLayout_6)
            win.tabWidget.addTab(tab, option.titre)
            plainTextEdit_3.setPlainText(texte)

    else:
        win.label_2.setParent(None)
        win.tabWidget.setParent(None)
        win.plainTextEdit.setPlainText(page.texte+"\n\nCeci est une fin du livre. Merci d'avoir joué")



def ajoutLigne(win):
    """Permet d'ajouter une ligne d'objet a la liste des objets de l'inventaire"""
    if win.lay_list[-1].count() == 5:



        lay = QHBoxLayout()
        lay.setContentsMargins(10, 10, 10, 10)
        lay.setSpacing(10)
        lay.setObjectName("horizontalLayout_3")
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        lay.addItem(spacerItem)
        win.lay_list.append(lay)
        win.verticalLayout_2.addLayout(lay)


def listObjet(win,partie:Partie):
    """Permet de creer la liste d'objet avec leurs images dans l'inventaire"""
    list_objet = partie.objets.copy()
    for objet in list_objet:
        ajoutLigne(win)

        verticalLayout = QVBoxLayout()
        verticalLayout.setContentsMargins(10, 10, 10, 10)
        verticalLayout.setSpacing(10)
        verticalLayout.setObjectName("verticalLayout")

        pixmap = QtGui.QPixmap("images/" + objet.path_image)
        pixmap = pixmap.scaled(64, 64)

        label_2 = QLabel()
        label_2.setEnabled(True)
        label_2.setMinimumSize(QtCore.QSize(64, 64))
        label_2.setMaximumSize(QtCore.QSize(64, 64))
        label_2.setObjectName("label_2")
        label_2.setPixmap(pixmap)

        verticalLayout.addWidget(label_2, 0, QtCore.Qt.AlignHCenter)
        label = QLabel()
        label.setEnabled(True)
        label.setObjectName("label")
        label.setText(objet.nom)
        label.setWordWrap(True)
        verticalLayout.addWidget(label, 0, QtCore.Qt.AlignHCenter)

        win.lay_list[-1].addLayout(verticalLayout)


def run():
    """Lance le programme"""

    app = QApplication.instance()
    app = QApplication(sys.argv)

    w = MainWindow()
    w.choisirLivre()
    w.show()
    app.exec()

run()