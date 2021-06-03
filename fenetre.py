from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from functools import partial
from CreateSave import *

retour = None

def Verifcara(chaine1 : str):

    liste_1 = ["/", ":", "*", "?", "|", ";", "<", ">", '"', "\n", "\t", '"', "\\"]

    for char in chaine1:
        if char in liste_1:
            return False

    return True


def bretour():
    if retour!= None:
        retour()


#Menu principal-----------------------------------------
def valider_livre(win, listWidget):
    """Fonction appelée par l'appui du bouton valider après selection du livre"""
    global retour
    l = listWidget.selectedItems()
    if l != []:
        titre = l[0].text()
        if titre not in [elem.titre for elem in livres]:

            loadLivre(titre)
        livre = getLivre(titre)

        win.clear_w()
        win.creationPageMenu(livre)
        retour = partial(retourMenuPrincipal,win)
    else:
        msgBoxSelect()


def bcreerLivre(win, lineEdit):
    """Fonction appelée après l'appui du bouton creer permettant de creer un nouveau livre"""
    global retour

    titre = lineEdit.text()
    titre = titre.strip()
    if Verifcara(titre):
        if titre != "":
            if titre not in getListNomLivre():
                createLivre(titre)
                livre = getLivre(titre)
                win.clear_w()
                win.creationPageMenu(livre)
                retour = partial(retourMenuPrincipal,win)
            else:
                msgBoxExiste()
        else:
            msgBoxExiste()
    else:
        msgBoxCaractereInterdit()

    lineEdit.setText("")


def bsupprimerLivre(win):
    """Permet de supprimer un projet après l'appui sur le bouton"""
    l = win.listWidget.selectedItems()
    if l != []:
        titre = l[0].text()
        loadLivre(titre)
        livre = getLivre(titre)
        deleteProjet(livre)
        actualiseListLivre(win)
    else:
        msgBoxSelect()


def actualiseListLivre(win):
    """Permet d'actualiser en temps réel la liste des livres"""
    win.listWidget.clear()
    L = getListNomLivre()
    for elem in L:
        win.listWidget.addItem(elem)



#Creation de page ------------------------------------
def bcreerPage(win, livre: Livre, spinBox: QSpinBox, checkBox: QCheckBox, textEdit: QTextEdit):
    """Fonction appelée apres l'appui sur le bouton creer pour creer une nouvelle page"""
    num_page = spinBox.value()
    is_fin = checkBox.isChecked()
    print(is_fin)

    texte = textEdit.toPlainText()
    if num_page != 0:
        if num_page not in getListPage(livre):
            createPage(livre, num_page, is_fin)
            actualiseListPage(win, livre)
            if texte != "":
                createPagetxt(livre.getPage(num_page), texte)
        else:
            msgBoxExiste()
    else:
        msgBoxExiste()

    textEdit.setText("")
    spinBox.setValue(0)
    checkBox.setChecked(False)


def retourMenuPrincipal(win):
    """Permet le retour au menu principal par un bouton"""
    win.clear_w()
    win.menuPrincipal()


def bmofifPage(win, livre: Livre):
    """Permet d'entrer dans le menu de modifiction de page et de création d'option"""
    global retour
    l = win.listWidget.selectedItems()
    if l != []:
        num_page = l[0].text()
        page = livre.getPage(int(num_page))
        win.listWidget.clearSelection()
        menuOption(win, page)
        retour =  partial(retourCreationPage,win,livre)
    else:
        msgBoxSelect()


def bsupprimerPage(win, livre: Livre):
    """Permet de supprimer la page selectionnée"""
    l = win.listWidget.selectedItems()
    if l != []:
        num_page = l[0].text()
        p = livre.getPage(int(num_page))

        if p.is_fin:
            path = "livres/" + livre.titre + "/pages/pages_fin/" + str(p.numero) + ".txt"
            os.remove(path)

        deletePage(p)
        livre.pages.remove(p)
        win.listWidget.clearSelection()
        actualiseListPage(win, livre)
    else:
        msgBoxSelect()


#Menu de la création des compteurs---------------------------------------
def menuCompteur(win, livre: Livre):
    """Fonction appelée pour le passage au menu gerant les compteur"""
    global retour
    win.clear_w()
    win.creationPageCompteur(livre)
    retour = partial(retourCreationPage, win, livre)


def bcreerCompteur(win, livre, lineEdit: QLineEdit, doubleSpinBox: QDoubleSpinBox):
    """Fonction appelée apres l'appui sur le bouton creer pour creer un compteur"""

    nom_comp = lineEdit.text()
    if Verifcara(nom_comp):

        valeur = doubleSpinBox.value()
        L = [elem.nom for elem in livre.compteurs]
        if nom_comp not in L and nom_comp != "":
            addCompteur(nom_comp, float(valeur), livre)
            lineEdit.setText("")
            doubleSpinBox.setValue(0.0)
            actualiseListCompteur(win, livre)
        else:
            msgBoxExiste()
    else:
        msgBoxCaractereInterdit()

def selectModifCompteur(win, livre: Livre, doubleSpinBox: QDoubleSpinBox):
    """Fonction appelée apres un clic surla liste des compteurs afin d'actualiser en temps rel leur valeur dans la
    spinBox"""
    l = win.listWidget.selectedItems()
    if l != []:
        nom_comp = l[0].text()
        valeur = livre.getCompteur(nom_comp).valeur
        doubleSpinBox.setValue(valeur)
    else:
        msgBoxSelect()


def bModifCompteur(win, livre, doubleSpinBox: QDoubleSpinBox):
    """Fonction appelée apres l'appui sur le bouton valider pour modifier la valeur d'un compteur existant"""
    l = win.listWidget.selectedItems()
    if l != []:
        nom_comp = l[0].text()
        valeur = doubleSpinBox.value()
        compteur = livre.getCompteur(nom_comp)
        compteur.valeur = valeur
        win.listWidget.clearSelection()
        doubleSpinBox.setValue(0.0)
        livre.sauvegarder
    else:
        msgBoxSelect()


def bSupprimerCompteur(win, livre, doubleSpinBox):
    """Fonction appelée apres l'appui sur le bouton supprimer dans le but de supprimer le compteur selectionné dans
    la liste"""
    l = win.listWidget.selectedItems()
    if l != []:
        nom_comp = l[0].text()
        compteur = livre.getCompteur(nom_comp)

        for page in livre.pages:
            for option in page.options:
                for elem in option.modif_compteur.copy():
                    if elem[0] == nom_comp:
                        option.modif_compteur.remove(elem)

        livre.compteurs.remove(compteur)
        win.listWidget.clearSelection()
        doubleSpinBox.setValue(0.0)
        del compteur
        actualiseListCompteur(win, livre)
        livre.sauvegarder()
    else:
        msgBoxSelect()



#Menu de la création d'objet de départ pour la partie-----------------------
def menuObjet(win, livre: Livre):
    """Permet de génerer la page du menu de création d'objet"""
    global retour
    win.clear_w()
    win.creationPageObjet(livre)
    retour = partial(retourCreationPage,win,livre)


def bcreerObjet(win, livre: Livre, lineEdit: QLineEdit):
    """Fonction appelée après appui sur le bouton creer et permettant de creer l'objet de l'utilisateur"""
    nom_obj = lineEdit.text()



    if Verifcara(nom_obj):
        L = [elem.nom for elem in livre.objets]
        if nom_obj not in L:
            if nom_obj != "":
                addObjet(livre, nom_obj,win.image_crea)
                lineEdit.setText("")
                actualiseListObjet(win, livre)
                pixmap = QtGui.QPixmap("images/vide.png")
                pixmap = pixmap.scaled(64, 64)

                win.label_6.setPixmap(pixmap)
                win.image_crea = "vide.png"
        else:
            msgBoxExiste()
    else:
        msgBoxCaractereInterdit()

def selectModifObjet(win, lineEdit: QLineEdit, livre:Livre):
    """Permet de remplir le lineEdit avec le nom de l'objet en selection de sorte à pouvoir le modifier"""
    l = win.listWidget.selectedItems()
    if l != []:
        nom_obj = l[0].text()
        objet = livre.getObjet(nom_obj)
        pixmap = QtGui.QPixmap("images/"+objet.path_image)
        pixmap = pixmap.scaled(64, 64)
        win.label_8.setPixmap(pixmap)
        lineEdit.setText(nom_obj)
    else:
        msgBoxSelect()


def bModifObjet(win, livre, lineEdit: QLineEdit):
    """Permet d'appliquer la modification apporté à un objet"""
    l = win.listWidget.selectedItems()
    if l != []:
        ancien_nom_obj = l[0].text()
        nouveau_nom_obj = lineEdit.text()
        if Verifcara(nouveau_nom_obj):

            objet = livre.getObjet(ancien_nom_obj)
            objet.nom = nouveau_nom_obj
            win.listWidget.clearSelection()
            livre.sauvegarder()
            actualiseListObjet(win, livre)
        else:
            msgBoxCaractereInterdit()
    else:
        msgBoxSelect()


def bSupprimerObjet(win, livre, lineEdit: QLineEdit):
    """Permet de supprimer l'objet selectionné"""
    l = win.listWidget.selectedItems()
    if l != []:
        nom_obj = l[0].text()
        objet = livre.getObjet(nom_obj)
        livre.objets.remove(objet)
        win.listWidget.clearSelection()
        lineEdit.setText("")
        del objet
        actualiseListObjet(win, livre)
        livre.sauvegarder()
    else:
        msgBoxSelect()


def choisirImage(win):
    """Permet de charger une image d'objet (creation)"""
    file = QFileDialog(directory="images")
    if file.exec():
        path_image = file.selectedFiles()[0].split("/")[-1]
        pixmap = QtGui.QPixmap("images/"+path_image)
        pixmap = pixmap.scaled(64, 64)
        win.label_6.setPixmap(pixmap)

        win.image_crea = path_image



def choisirImageSave(win,label:QLabel,livre:Livre):
    """Permet de choir charger et sauvegarder une image d'objet (modification)"""
    l = win.listWidget.selectedItems()
    if l != []:
        nom_objet = l[0].text()
        objet = livre.getObjet(nom_objet)
        file = QFileDialog(directory="images")
        if file.exec():
            path_image = file.selectedFiles()[0].split("/")[-1]
            pixmap = QtGui.QPixmap("images/" + path_image)
            pixmap = pixmap.scaled(64, 64)
            label.setPixmap(pixmap)
            objet.path_image = path_image
            livre.sauvegarder()
            win.image = path_image



#Menu de création d'option et de modification de page_________________________________
def menuOption(win, page: Page):
    """Permet de générer le menu de création d'option et de modification de page"""
    global retour
    win.clear_w()
    win.creationPageOption(page)
    retour = partial(retourCreationPage,win,page.livre)


def bmodifInfoPage(page: Page, textEdit: QTextEdit, checkBox: QCheckBox):
    """Application des modifications que le joueur souhaite apporter à la page (texte,fin)"""
    texte = textEdit.toPlainText()
    is_fin = checkBox.isChecked()

    page.texte = texte
    if page.is_fin:
        path = "livres/" + page.livre.titre + "/pages/pages_fin/" + str(page.numero) + ".txt"
        os.remove(path)
    page.is_fin = is_fin

    createPagetxt(page, texte)


def bcreerOption(win, page: Page, lineEdit: QLineEdit, spinBox: QSpinBox, textEdit: QTextEdit):
    """Permet de creer un nouvelle option pour la page en fonction des entrées de l'utilisateur"""
    L = [elem.titre for elem in page.options]
    titre_option = lineEdit.text()
    titre_option = titre_option.strip()
    if Verifcara(titre_option):

        if titre_option not in L and titre_option!="":
            lien_page = spinBox.value()
            texte_option = textEdit.toPlainText()
            createOption(page, titre_option)
            para = page.getOption(titre_option)
            if texte_option != "":
                createOptiontxt(para, texte_option)
            if lien_page != 0:
                createLienPage(para, lien_page)

            actualiseListOption(win, page)
            lineEdit.setText("")
            spinBox.setValue(0)
            textEdit.setText("")
        else:
            msgBoxExiste()
    else:
        msgBoxCaractereInterdit()

def connectionLienPage(win, option:Option):
    """Permet de passer rapidement d'une page à l'autre en appuyant sur un bouton"""
    num_lien = option.num_lien_page
    if pageExiste(option.livre.titre,num_lien):
        p = option.livre.getPage(num_lien)
        menuOption(win,p)
    else:
        msgBoxPageInexistante()


def supprimerOption(win, page : Page):
    """Permet de supprimer l'option selectionnée"""
    l = win.listWidget.selectedItems()

    if l != []:
        titre_option = l[0].text()
        option = page.getOption(titre_option)
        deleteOption(option)
        actualiseListOption(win,page)
    else:
        msgBoxSelect()




#Menu de modification d'option --------------------------------------------
def bmenuModifOption(win, page: Page):
    """Permet d'effectuer le passage au menu de modification d'option"""
    l = win.listWidget.selectedItems()
    if l != []:
        titre_option = l[0].text()
        option = page.getOption(titre_option)
        menuModifOption(win, option)
    else:
        msgBoxSelect()


def menuModifOption(win, option: Option):
    """Genere le menu de modification d'option"""
    global retour
    win.clear_w()
    win.menuModifOption(option)
    retour = partial(menuOption,win,option.page)


def bmodifOption(option: Option, textEdit: QTextEdit, lineEdit: QLineEdit, spinBox: QSpinBox, label: QLabel, pushButton:QPushButton):
    """Permet d'appliquer les modification que l'utiisatuer souhaite appliquer sur l'option"""
    titre_option = lineEdit.text()
    titre_option = titre_option.strip()
    if Verifcara(titre_option):

        texte_option = textEdit.toPlainText()
        lien_page = spinBox.value()
        l = [elem.titre for elem in option.page.options]
        l.remove(option.titre)
        if lien_page != 0:
            option.num_lien_page = lien_page
            createLienPage(option, lien_page)

        if titre_option not in l:
            path = "livres/" + option.livre.titre + "/pages/" + str(option.page.numero) + "/"
            os.rename(path + option.titre, path + titre_option)
            option.titre = titre_option
            option.texte = texte_option
            createOptiontxt(option, texte_option)
            label.setText(option.livre.titre + " Page: " + str(option.page.numero) + ": " + option.titre)
            pushButton.setText("Aller à la page : {}".format(option.num_lien_page))
    else:
        msgBoxCaractereInterdit()


def retourCreationPage(win, livre: Livre):
    """Permet le retour au menu creation de page par l'appui d'un bouton"""
    global retour
    win.clear_w()
    win.creationPageMenu(livre)
    retour = partial(retourMenuPrincipal,win)





#Menu de gain d'objet en cas de choix de l'option -------------------------------
def menuGainObjet(win,option:Option):
    """Permet de genérer le menu permettant d'ajouter des gains d'objets"""
    global retour
    win.clear_w()
    win.menuGainObjet(option)
    retour = partial(menuModifOption, win, option)


def baddGainObjet(win,lineEdit: QLineEdit, option: Option):
    """Permet d'ajouter un gain d'objet"""
    nom_objet = lineEdit.text()

    L1 = [elem.nom for elem in option.livre.objets]
    L2 = []
    livre = option.livre

    for page in livre.pages:
        for op in page.options:
            for gain_obj in op.gain_objet:
                L2.append(gain_obj)

    if nom_objet in L1:
        msgBoxExiste("L'élément que vous tentez de créer existe deja dans les objets de départ. Celui-ci ne sera effectivement ajouté "
                     "uniquement si cet élément n'est pas déja present dans l'inventaire du joueur")
    if nom_objet in L2:
        msgBoxExiste("L'élément que vous tentez de créer existe deja dans les gains d'objets d'autres options. Celui-ci sera effectivement ajouté "
                     "uniquement si cet élément n'est pas déja present dans l'inventaire du joueur")

    if Verifcara(nom_objet):
        if nom_objet not in option.gain_objet:
            addGainObjet(option,nom_objet,win.image_crea)
            actualiseListGainObjet(win,option)
            pixmap = QtGui.QPixmap("images/vide.png")
            pixmap = pixmap.scaled(64, 64)
            win.label_6.setPixmap(pixmap)
            win.image_crea = "vide.png"

        else:
            msgBoxExiste()
    else:
        msgBoxCaractereInterdit()




    lineEdit.setText("")

def supprimerGainObjet(win, lineEdit:QLineEdit ,option:Option):
    """Permet de supprimer un gain d'objet selectionné"""
    l = win.listWidget.selectedItems()
    if l != []:
        nom_objet = l[0].text()
        for gain in option.gain_objet:
            if gain[0] == nom_objet:
                option.gain_objet.remove(gain)

        option.livre.sauvegarder()
        lineEdit.setText("")
        pixmap = QtGui.QPixmap("images/vide.png")
        pixmap = pixmap.scaled(64, 64)
        win.label_8.setPixmap(pixmap)

        win.listWidget.clearSelection()


        actualiseListGainObjet(win,option)
    else:
        msgBoxSelect()


def modifGainObjet(win,lineEdit: QLineEdit,option:Option):
    """Permet d'appliquer les modifications de l'utilisateur sur le gain d'objet selectionné"""
    l = win.listWidget.selectedItems()
    if l != []:
        ancien_nom = l[0].text()
        nouveau_nom = lineEdit.text()
        if Verifcara(nouveau_nom):

            L1 = [elem.nom for elem in option.livre.objets]
            L2 = []
            livre = option.livre
            for page in livre.pages:
                for op in page.options:
                    for gain_obj in op.gain_objet:
                        L2.append(gain_obj)

            if nouveau_nom in L1:
                msgBoxExiste(
                    "L'élément que vous tentez de créer existe deja dans les objets de départ. Celui-ci ne sera effectivement ajouté "
                    "uniquement si cet élément n'est pas déja present dans l'inventaire du joueur")
            if nouveau_nom in L2 and nouveau_nom != ancien_nom:
                msgBoxExiste(
                    "L'élément que vous tentez de créer existe deja dans les gains d'objets d'autres options. Celui-ci sera effectivement ajouté "
                    "uniquement si cet élément n'est pas déja present dans l'inventaire du joueur")


            if nouveau_nom not in option.gain_objet and nouveau_nom != "":
                i = option.gain_objet.index(ancien_nom)
                option.gain_objet[i] = nouveau_nom
                option.livre.sauvegarder()
                actualiseListGainObjet(win,option)
                lineEdit.setText("")
            else:
                msgBoxExiste()
        else :
            msgBoxCaractereInterdit()
    else:
        msgBoxSelect()


def clickListGainObjet(win,lineEdit : QLineEdit,option:Option):
    """Permet de remplir la lineEdit avec les informations de l'objet selcectionné"""
    l = win.listWidget.selectedItems()
    if l != []:
        nom_objet = l[0].text()

        for gain in option.gain_objet:
            if gain[0] == nom_objet:
                pixmap = QtGui.QPixmap("images/" + gain[1])
                pixmap = pixmap.scaled(64, 64)
                win.label_8.setPixmap(pixmap)

                lineEdit.setText(nom_objet)

def choisirImageSave2(win,label:QLabel,option:Option):
    """Pemret de choisir et d'enregister l'image pour un gain d'objet"""
    l = win.listWidget.selectedItems()
    if l != []:
        nom_objet = l[0].text()

        file = QFileDialog(directory="images")
        if file.exec():
            path_image = file.selectedFiles()[0].split("/")[-1]
            pixmap = QtGui.QPixmap("images/" + path_image)
            pixmap = pixmap.scaled(64, 64)
            label.setPixmap(pixmap)
            for gain in option.gain_objet:
                if gain[0] == nom_objet:
                    gain[1] = path_image

            option.livre.sauvegarder()
            win.image = path_image



#Menu de creéation des modification de compteur en cas de choix de l'option
def menuModifCompteur(win,option:Option):
    """Permet de générer le menu de modification de compteurs"""
    global retour
    win.clear_w()
    win.menuModifCompteur(option)
    retour = partial(menuModifOption,win,option)


def creerModifCompteur(win,comboBox:QComboBox,spinBox: QDoubleSpinBox, option: Option):
    """Permet de créer une modification de compteur"""
    l = win.listWidget.selectedItems()
    if l != []:
        nom_compteur = l[0].text()
        v_combo = comboBox.currentText()
        if v_combo == "Augmenter":
            e = "+"
        elif v_combo == "Diminuer":
            e = "-"
        else:
            e = "="
        valeur = spinBox.value()
        if valeur != 0:
            addModifCompteur(option,nom_compteur,valeur,e)

            actualiseListModifCompteur(win,option)
            comboBox.setCurrentIndex(0)
            spinBox.setValue(0.0)
            win.listWidget.clearSelection()
    else:
        msgBoxSelect()


def clickListModifCompteur(win, comboBox:QComboBox, spinBox:QDoubleSpinBox):
    """Permet de remplir la SpinBox et la comboBox avec les informations de l'objet selectionné en prévision d'une modif"""
    l = win.listWidget_2.selectedItems()
    if l != []:
        var = l[0].text()
        e = var.split("\t")[1][0]
        valeur = float(var.split("\t")[1].replace(e+" ",""))

        if e == "+":
            comboBox.setCurrentIndex(0)
        elif e == "-":
            comboBox.setCurrentIndex(1)
        else:
            comboBox.setCurrentIndex(2)

        spinBox.setValue(valeur)


def modifModifCompteur(win,comboBox:QComboBox, spinBox:QDoubleSpinBox, option:Option):
    """Permet l'application de la modification de la modfication du Compteur"""
    l = win.listWidget_2.selectedItems()
    if l != []:
        txt = l[0].text()
        nom_compteur = txt.split("\t")[0]

        var = comboBox.currentText()
        if var == "Augmenter":
            e = "+"
        elif var == "Diminuer":
            e = "-"
        else:
            e = "="

        valeur = spinBox.value()

        for elem in option.modif_compteur:
            if elem[0] == nom_compteur:
                elem[1] = valeur
                elem[2] = e
        option.livre.sauvegarder()
        actualiseListModifCompteur(win,option)
        win.listWidget_2.clearSelection()
        comboBox.setCurrentIndex(0)
        spinBox.setValue(0)

    else:
        msgBoxSelect()


def supprimerModifCompteur(win,option:Option):
    """Permet la suppression de la modifcation de compteur selectionnée"""
    l = win.listWidget_2.selectedItems()
    if l != []:
        txt = l[0].text()
        nom_compteur = txt.split("\t")[0]
        e = txt.split("\t")[1][0]
        valeur = float(txt.split("\t")[1].replace(e + " ", ""))
        for modif in option.modif_compteur:
            if modif[0] == nom_compteur:
                option.modif_compteur.remove([nom_compteur,valeur,e])
                break
        option.livre.sauvegarder()
        actualiseListModifCompteur(win,option)
        win.listWidget_2.clearSelection()

    else:
        msgBoxSelect()






#Menu creation de conditions de dés
def menuConditionDe(win,option):
    """Permet de charger le menu des conditions de des"""
    global retour
    win.clear_w()
    win.menuConditionDe(option)
    retour = partial(menuModifOption,win,option)


def ajoutConditionDeSuppr(win, option:Option, spinBox_1:QSpinBox, spinBox_2:QSpinBox, spinBox_3:QSpinBox):
    """Permet de supprimer une condition de de"""
    compteur = 0

    for elem in option.conditions:
        if isinstance(elem, ConditionDe):
            compteur+= 1

    if compteur > 0:
        msgBoxSupprimer(partial(ajoutConditionDe,win,option,spinBox_1,spinBox_2,spinBox_3),None,"Cette action écrasera le jet précédent. "                                                                        "Voulez vous continuer ?")

    else:

        ajoutConditionDe(win,option,spinBox_1,spinBox_2,spinBox_3)


def ajoutConditionDe(win, option:Option, spinBox_1:QSpinBox, spinBox_2:QSpinBox, spinBox_3:QSpinBox):
    """Permet d'ajouter une condition de des"""
    for elem in option.conditions.copy():
        if elem.isDe():
            option.conditions.remove(elem)
    path = "livres/" + option.livre.titre + "/pages/" + str(
        option.page.numero) + "/" + option.titre + "/condition/condition_de.txt"

    with open(path, "w")as f:
        f.close()
    chances = spinBox_1.value()
    nb_de = spinBox_2.value()
    nb_faces = spinBox_3.value()


    for i in range(chances):
        createConditionDe(option, nb_de, ">", nb_de, nb_faces)

    actualiseListConditionDe(win, option)


def modifConditionDe(win,option:Option, comboBox:QComboBox, comboBox_2:QComboBox,spinBox:QSpinBox):
    """Permet de modifier la valeur d'une condition de de en fonction des paramètres entrés"""
    txt = comboBox.currentText()
    if txt != "":
        num = int(txt.split(":")[1])
        index = num - 1
        l = []
        for elem in option.conditions:
            if isinstance(elem, ConditionDe):
                l.append(elem)

        condition = l[index]
        combo_txt = comboBox_2.currentText()
        if combo_txt == "Superieur":
            e = ">"
        elif combo_txt == "Inferieur":
            e = "<"
        else:
            e = "="

        valeur = spinBox.value()

        condition.epreuve = e
        condition.valeur = valeur
        actualiseListConditionDe(win,option)
        option.livre.sauvegarder()



def changeConditionDe(win,option, comboBox:QComboBox,comboBox_2:QComboBox,spinBox:QSpinBox):
    """Permet l'actualisation des champs en fonction de la selection de la comboBox"""
    txt = comboBox.currentText()
    if txt != "":
        num = int(txt.split(":")[1])
        index = num-1
        l = []
        for elem in option.conditions:
            if isinstance(elem,ConditionDe):
                l.append(elem)

        condition = l[index]
        e = condition.epreuve
        valeur = condition.valeur
        if e == ">":
            comboBox_2.setCurrentIndex(0)
        elif e == "<":
            comboBox_2.setCurrentIndex(1)
        else:
            comboBox_2.setCurrentIndex(2)

        spinBox.setValue(valeur)



def supprimerConditionDe(win,option):
    """Permet de supprimer un des lancé de liste des lancés"""
    l = win.listWidget.selectedIndexes()
    if l != []:
        index = l[0].row()
        L = []
        for condition in option.conditions:
            if condition.isDe():
                L.append(condition)
        option.conditions.remove(L[index])
        option.livre.sauvegarder()
        actualiseListConditionDe(win,option)
    else:
        msgBoxSelect()



#Menu de creation des conditions d'objets
def menuConditionObjet(win,option: Option):
    """Permet de charger le menu des conditons d'objets"""
    global retour
    win.clear_w()
    win.menuConditionObjet(option)
    retour  = partial(menuModifOption,win,option)


def ajoutConditionObjet(win, option :Option, checkBox:QCheckBox):
    """Permet d'ajouter une condition d'objet"""
    l = win.listWidget.selectedItems()

    if l != []:
        nom_objet = l[0].text()
        supprime_utilisation = checkBox.isChecked()
        createConditionObjet(option,nom_objet,supprime_utilisation)
        actualiseListConditionObjet(win, option)
    else:
        msgBoxSelect()


def supprimerConditionObjet(win, option:Option):
    """Permet de supprimer une cndition d'objet de la liste"""
    l = win.listWidget_2.selectedItems()
    if l != []:
        nom_objet = l[0].text().split("\t")[0]
        L = []
        for condition in option.conditions:
            if condition.isObjet():
                L.append(condition)
        for elem in L:
            if elem.nom_objet == nom_objet:
                option.conditions.remove(elem)

        option.livre.sauvegarder()
        actualiseListConditionObjet(win, option)
        win.listWidget_2.clearSelection()
    else:
        msgBoxSelect()



#Menu de creation de condition de compteur
def menuConditionCompteur(win,option:Option):
    """Permet de charger le menu de condition de compteur"""
    global retour
    win.clear_w()
    win.menuConditionCompteur(option)
    retour = partial(menuModifOption,win,option)


def ajoutConditionCompteur(win, option:Option, comboBox:QComboBox, spinBox:QDoubleSpinBox):
    """Permet d'ajouter une conditionde compteur"""
    l = win.listWidget.selectedItems()
    if l != []:
        nom_compteur = l[0].text()
        compteur = option.livre.getCompteur(nom_compteur)
        txt = comboBox.currentText()
        if txt == "Superieur":
            e = ">"
        elif txt == "Inferieur":
            e = "<"
        else:
            e = "="
        valeur = spinBox.value()
        createConditionCompteur(option,compteur,valeur,e)
        actualiseListConditionCompteur(win,option)
        comboBox.setCurrentIndex(0)
        win.listWidget.clearSelection()
        spinBox.setValue(0.0)
    else:
        msgBoxSelect()


def supprimerConditionCompteur(win,option:Option):
    """Fonction appelé lors de l'appui du bouton suprimmer afin de supprimer une condition de compteur"""
    l = win.listWidget_2.selectedItems()
    if l != []:
        nom_compteur = l[0].text().split("\t")[0]
        L = []
        for condition in option.conditions:
            if condition.isCompteur():
                if condition.compteur.nom == nom_compteur:
                    option.conditions.remove(condition)
                    break

        option.livre.sauvegarder()
        actualiseListConditionCompteur(win,option)
    else:
        msgBoxSelect()






#Actualisation des listes --------------------------
def actualiseListPage(win, livre: Livre):
    """Permet l'actualisation de la liste affichant les différentes pages creees"""
    win.listWidget.clear()
    L = []
    for page in livre.pages:
        L.append(page.numero)
    L.sort()
    for elem in L:
        win.listWidget.addItem(str(elem))


def actualiseListCompteur(win, livre: Livre):
    """Permet l'actualisation de la liste affichantles différents compteurs crees"""
    win.listWidget.clear()
    L = [elem.nom for elem in livre.compteurs]
    L.sort()
    for elem in L:
        win.listWidget.addItem(elem)


def actualiseListObjet(win, livre: Livre):
    """Permet l'actualisation de la liste des objets"""

    win.listWidget.clear()
    pixmap = QtGui.QPixmap("images/vide.png")
    pixmap = pixmap.scaled(64, 64)

    win.label_8.setPixmap(pixmap)
    win.image = "vide.png"

    L = [elem.nom for elem in livre.objets]
    L.sort()

    for elem in L:
        win.listWidget.addItem(elem)


def actualiseListOption(win, page: Page):
    """Permet l'actualisation de la liste des options"""
    win.listWidget.clear()
    L = [elem.titre for elem in page.options]
    L.sort()
    for elem in L:
        win.listWidget.addItem(elem)


def actualiseListGainObjet(win, option:Option):
    """Permet l'actualisation de la liste des gains d'objets"""
    win.listWidget.clear()
    pixmap = QtGui.QPixmap("images/vide.png")

    win.label_8.setPixmap(pixmap)
    win.image = "vide.png"

    for elem in option.gain_objet:
        win.listWidget.addItem(elem[0])


def actualiseListModifCompteur(win, option:Option):
    """Permet l'actualisation de la liste des modifications de compteurs"""
    win.listWidget_2.clear()
    L = [[elem[0],elem[1],elem[2].replace("\n","")] for elem in option.modif_compteur]
    for elem in L:
        win.listWidget_2.addItem(elem[0]+"\t"+elem[2]+" "+str(elem[1]))


def actualiseListConditionDe(win, option:Option):
    """Permet l'actualisation de la liste du menu condition de dés"""
    win.listWidget.clear()
    win.comboBox.clear()
    compteur = 0
    for elem in option.conditions:
        if elem.isDe():
            compteur += 1
            win.listWidget.addItem("Chance : "+str(compteur)+"\t"+str(elem.nb_de)+"D"+str(elem.nb_faces)+
                                   "\t"+elem.epreuve+str(elem.valeur))
            win.comboBox.addItem("Chance : {}".format(compteur))
            if compteur == 1:
                win.spinBox_3.setValue(elem.valeur)
                win.spinBox_3.setMinimum(elem.nb_de)
                win.spinBox_3.setMaximum(elem.nb_de*elem.nb_faces)
                if elem.epreuve == ">":
                    win.comboBox_2.setCurrentIndex(0)
                elif elem.epreuve == "<":
                    win.comboBox_2.setCurrentIndex(1)
                else:
                    win.comboBox_2.setCurrentIndex(2)


def actualiseListConditionObjet(win, option:Option):
    """Permet l'actualisation des deux listes du menu condition d'objet"""
    win.listWidget.clear()
    win.listWidget_2.clear()
    L = []
    livre = option.livre

    for page in livre.pages:
        for op in page.options:
            for gain_obj in op.gain_objet:
                if gain_obj not in L:
                    L.append(gain_obj)

    L2 = [elem[0] for elem in L]
    for objet in livre.objets:
        if objet.nom not in L2:
            L.append([objet.nom, objet.path_image])


    for condition in option.conditions:
        for elem in L.copy():
            if condition.isObjet():
                if elem[0] == condition.nom_objet:
                    L.remove(elem)

                    if condition.supprime_utilisation:
                        su = "Oui"
                    else:
                        su = "Non"

                    win.listWidget_2.addItem(condition.nom_objet+"\t\tSuppression : "+su)

    for elem in L:
        win.listWidget.addItem(elem[0])


def actualiseListConditionCompteur(win, option: Option):
    """Permet l'actualisation des deux listes du menu condition de compteur"""
    win.listWidget.clear()
    win.listWidget_2.clear()

    L = option.livre.compteurs.copy()
    for condition in option.conditions:
        if condition.isCompteur():
            L.remove(condition.compteur)
            win.listWidget_2.addItem(condition.compteur.nom+"\t"+condition.epreuve+str(condition.valeur))

    for elem in L:
        win.listWidget.addItem(elem.nom)








def msgBoxSupprimer(command,listWidget=None,texte=""):
    """Permet d'afficher un message demandant à l'utilisateur s'il est sur de vouloir réaliser cette action"""

    if texte == "":
        texte = "Vous êtes sur le point d'effectuer une suppression qui entrainera un perte de donnée. Voulez vous continuer ?"

    if listWidget!= None:
        l = listWidget.selectedItems()
    else:
        l = [0]

    if l != []:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(texte)
        msg.setWindowTitle("Suppression")

        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.buttonClicked.connect(partial(click,command))

        msg.exec()
    else:
        msgBoxSelect()


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


def msgBoxPageInexistante():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("La page à laquelle vous tentez de vous rendre n'existe pas.")
    msg.setWindowTitle("Page inexistante")
    msg.setStandardButtons(QMessageBox.Ok)

    msg.exec()


def msgBoxCaractereInterdit():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Certains caractères que vous avez entrez ne sont pas autorisés. Caractère non authorisés : \/*><;:|?\" ainsi que les entrées et les tabulations")
    msg.setWindowTitle("Page inexistante")
    msg.setStandardButtons(QMessageBox.Ok)

    msg.exec()



def click(command,i):
    """Execution de la commande de msgBoxSupprimer en cas de réponse Ok"""
    if i.text() == "OK":
        command()






class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.widget_list = []
        self.resize(971, 702)

        self.window_lay = QVBoxLayout()
        self.window_lay.setObjectName("window_lay")
        self.setWindowTitle("HistoryMaker")
        self.setWindowIcon(QtGui.QIcon("logo.png"))


    def clear_w(self):
        """Permet de vider un fenetre de l'entierté de ses elements afin de changer son contenu"""
        for elem in self.widget_list:
            elem.setParent(None)
        nb = self.window_lay.count()

        for i in range(nb):
            self.window_lay.removeItem(self.window_lay.itemAt(0))

        self.widget_list = []


    def menuPrincipal(self):
        """Permet l'affichage du premier menu"""
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setContentsMargins(20, 30, 20, 20)
        self.verticalLayout.setSpacing(40)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label_hm = QLabel()

        font = QtGui.QFont()
        font.setPointSize(26)
        self.label_hm.setFont(font)
        self.label_hm.setObjectName("label_hm")
        self.label_hm.setText("HistoryMaker")
        self.widget_list.append(self.label_hm)

        self.verticalLayout.addWidget(self.label_hm, 0, QtCore.Qt.AlignHCenter)
        self.line_hori = QFrame()
        self.line_hori.setFrameShape(QFrame.HLine)
        self.line_hori.setFrameShadow(QFrame.Sunken)
        self.line_hori.setObjectName("line_hori")
        self.verticalLayout.addWidget(self.line_hori)
        self.widget_list.append(self.line_hori)

        self.lab_desc = QLabel()
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lab_desc.setFont(font)
        self.lab_desc.setObjectName("lab_desc")
        self.lab_desc.setText("Créez votre propre livre")
        self.verticalLayout.addWidget(self.lab_desc, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.lab_desc)

        self.hori_2_lay = QHBoxLayout()
        self.hori_2_lay.setSpacing(50)
        self.hori_2_lay.setObjectName("hori_2_lay")

        self.vert_lay_gauche1 = QVBoxLayout()
        self.vert_lay_gauche1.setContentsMargins(10, 10, 10, 10)
        self.vert_lay_gauche1.setSpacing(20)
        self.vert_lay_gauche1.setObjectName("vert_lay_gauche1")

        self.lab_continuer_livre = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)

        self.lab_continuer_livre.setFont(font)
        self.lab_continuer_livre.setObjectName("lab_continuer_livre")
        self.lab_continuer_livre.setText("Continuer un livre")
        self.widget_list.append(self.lab_continuer_livre)

        self.vert_lay_gauche1.addWidget(self.lab_continuer_livre)

        self.vertlay_gauche2 = QVBoxLayout()
        self.vertlay_gauche2.setContentsMargins(10, 10, 10, 10)
        self.vertlay_gauche2.setSpacing(15)
        self.vertlay_gauche2.setObjectName("vertlay_gauche2")

        self.listWidget = QListWidget()
        self.listWidget.setObjectName("listWidget")

        actualiseListLivre(self)

        self.vertlay_gauche2.addWidget(self.listWidget)
        self.widget_list.append(self.listWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.b_valider = QPushButton()
        self.b_valider.setMinimumSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.b_valider.setFont(font)
        self.b_valider.setObjectName("b_valider")
        self.horizontalLayout.addWidget(self.b_valider, 0, QtCore.Qt.AlignLeft)
        self.b_valider.clicked.connect(partial(valider_livre, self, self.listWidget))
        self.widget_list.append(self.b_valider)
        self.b_valider.setText("Valider")

        self.pushButton = QPushButton()
        self.pushButton.setMinimumSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.vertlay_gauche2.addLayout(self.horizontalLayout)
        self.widget_list.append(self.pushButton)
        self.pushButton.setText("Supprimer")
        self.pushButton.clicked.connect(partial(msgBoxSupprimer,partial(bsupprimerLivre,self),self.listWidget,""))

        self.vertlay_gauche2.addWidget(self.b_valider, 0, QtCore.Qt.AlignLeft)
        self.vert_lay_gauche1.addLayout(self.vertlay_gauche2)

        self.vertlay_droite = QVBoxLayout()
        self.vertlay_droite.setContentsMargins(20, 10, 10, 50)
        self.vertlay_droite.setObjectName("vertlay_droite")

        self.lab_cree_livre = QLabel()
        self.lab_cree_livre.setMaximumSize(QtCore.QSize(241, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lab_cree_livre.setFont(font)
        self.lab_cree_livre.setObjectName("lab_cree_livre")
        self.lab_cree_livre.setText("Créer un nouveau livre")
        self.widget_list.append(self.lab_cree_livre)

        self.vertlay_droite.addWidget(self.lab_cree_livre)

        self.lineEdit = QLineEdit()
        self.lineEdit.setObjectName("lineEdit")
        self.vertlay_droite.addWidget(self.lineEdit)
        self.widget_list.append(self.lineEdit)

        self.b_creer = QPushButton()
        self.b_creer.setObjectName("b_creer")
        self.b_creer.setText("Créer")

        self.b_creer.clicked.connect(partial(bcreerLivre, self, self.lineEdit))
        self.vertlay_droite.addWidget(self.b_creer, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.b_creer)

        spacerItem1 = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.vertlay_droite.addItem(spacerItem1)
        self.hori_2_lay.addLayout(self.vertlay_droite)
        self.verticalLayout.addLayout(self.hori_2_lay)

        self.line_vert = QFrame()
        self.line_vert.setFrameShape(QFrame.VLine)
        self.line_vert.setFrameShadow(QFrame.Sunken)
        self.line_vert.setObjectName("line_vert")
        self.hori_2_lay.addWidget(self.line_vert)
        self.widget_list.append(self.line_vert)

        self.hori_2_lay.addLayout(self.vert_lay_gauche1)

        self.window_lay.addLayout(self.verticalLayout)
        self.setLayout(self.window_lay)


    def creationPageMenu(self, livre: Livre):
        """Permet l'affichage du menu de creation de pages"""

        self.lab_titre = QLabel()
        font = QtGui.QFont()
        font.setPointSize(16)

        self.pushButton = QPushButton()
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Retour")
        self.window_lay.addWidget(self.pushButton, 0, QtCore.Qt.AlignLeft)
        self.pushButton.clicked.connect(bretour)
        self.widget_list.append(self.pushButton)

        self.lab_titre.setFont(font)
        self.lab_titre.setObjectName("lab_titre")
        self.lab_titre.setText(livre.titre)
        self.widget_list.append(self.lab_titre)

        self.window_lay.addWidget(self.lab_titre, 0, QtCore.Qt.AlignHCenter)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        self.widget_list.append(self.line)

        self.window_lay.addWidget(self.line)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_3.setSpacing(50)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")

        self.lab_creer_page = QLabel()
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lab_creer_page.setFont(font)
        self.lab_creer_page.setObjectName("lab_creer_page")
        self.lab_creer_page.setText("Créer une page")
        self.widget_list.append(self.lab_creer_page)

        self.verticalLayout.addWidget(self.lab_creer_page)

        self.label_2 = QLabel()
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        self.label_2.setText("Numéro de page")
        self.widget_list.append(self.label_2)

        self.spinBox = QSpinBox()
        self.spinBox.setMinimumSize(QtCore.QSize(200, 0))
        self.spinBox.setObjectName("spinBox")
        self.verticalLayout.addWidget(self.spinBox, 0, QtCore.Qt.AlignLeft)
        self.spinBox.setMaximum(1000000000)
        self.widget_list.append(self.spinBox)

        self.b_creer_page = QPushButton()
        self.b_creer_page.setMinimumSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.b_creer_page.setFont(font)
        self.b_creer_page.setObjectName("b_creer_page")
        self.b_creer_page.setText("Créer")

        self.widget_list.append(self.b_creer_page)

        self.verticalLayout.addWidget(self.b_creer_page, 0, QtCore.Qt.AlignLeft)
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_7.setSpacing(15)
        self.verticalLayout_7.setObjectName("verticalLayout_7")

        self.label = QLabel()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.widget_list.append(self.label)

        self.verticalLayout_7.addWidget(self.label, 0, QtCore.Qt.AlignLeft)
        self.textEdit = QTextEdit()
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_7.addWidget(self.textEdit)
        self.widget_list.append(self.textEdit)

        self.checkBox = QCheckBox()
        font = QtGui.QFont()
        font.setPointSize(8)

        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.widget_list.append(self.checkBox)
        self.verticalLayout_7.addWidget(self.checkBox, 0, QtCore.Qt.AlignLeft)

        self.horizontalLayout_3.addLayout(self.verticalLayout_7)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.b_creer_page.clicked.connect(partial(bcreerPage, self, livre, self.spinBox, self.checkBox, self.textEdit))
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_2.setSpacing(20)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.lab_modif_page = QLabel()
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lab_modif_page.setFont(font)
        self.lab_modif_page.setObjectName("lab_modif_page")
        self.widget_list.append(self.lab_modif_page)

        self.verticalLayout_2.addWidget(self.lab_modif_page, 0, QtCore.Qt.AlignLeft)
        self.listWidget = QListWidget()
        self.listWidget.setObjectName("listWidget")

        actualiseListPage(self, livre)

        self.verticalLayout_2.addWidget(self.listWidget)
        self.widget_list.append(self.listWidget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.b_valider = QPushButton()
        self.b_valider.setMinimumSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.b_valider.setFont(font)
        self.b_valider.setObjectName("b_valider")
        self.horizontalLayout_2.addWidget(self.b_valider, 0, QtCore.Qt.AlignHCenter)
        self.b_valider.clicked.connect(partial(bmofifPage, self, livre))
        self.widget_list.append(self.b_valider)

        self.pushButton_2 = QPushButton()
        self.pushButton_2.setMinimumSize(QtCore.QSize(150, 0))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.pushButton_2.setText("Supprimer")
        self.widget_list.append(self.pushButton_2)
        self.pushButton_2.clicked.connect(partial(msgBoxSupprimer,partial(bsupprimerPage, self, livre),self.listWidget,""))

        self.verticalLayout_2.addWidget(self.b_valider, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.line_2 = QFrame()
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.widget_list.append(self.line_2)

        self.horizontalLayout.addWidget(self.line_2)
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_6.setSpacing(20)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_4.setSpacing(20)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)

        self.lab_compteur = QLabel()
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lab_compteur.setFont(font)
        self.lab_compteur.setObjectName("lab_compteur")
        self.verticalLayout_4.addWidget(self.lab_compteur, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.lab_compteur)

        self.b_creer_comp = QPushButton()
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_creer_comp.sizePolicy().hasHeightForWidth())
        self.b_creer_comp.setSizePolicy(sizePolicy)
        self.b_creer_comp.setMinimumSize(QtCore.QSize(290, 50))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.b_creer_comp.setFont(font)
        self.b_creer_comp.setObjectName("b_creer_comp")
        self.verticalLayout_4.addWidget(self.b_creer_comp)
        self.widget_list.append(self.b_creer_comp)

        self.b_creer_comp.clicked.connect(partial(menuCompteur, self, livre))

        spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)
        self.verticalLayout_6.addLayout(self.verticalLayout_4)
        self.line_4 = QFrame()
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout_6.addWidget(self.line_4)
        self.widget_list.append(self.line_4)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_5.setSpacing(15)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        spacerItem2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem2)

        self.lab_objets = QLabel()
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lab_objets.setFont(font)
        self.lab_objets.setObjectName("lab_objets")
        self.verticalLayout_5.addWidget(self.lab_objets, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.lab_objets)

        self.b_creer_obj = QPushButton()
        self.b_creer_obj.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.b_creer_obj.setFont(font)
        self.b_creer_obj.setObjectName("b_creer_obj")
        self.verticalLayout_5.addWidget(self.b_creer_obj)
        self.widget_list.append(self.b_creer_obj)
        self.b_creer_obj.clicked.connect(partial(menuObjet, self, livre))

        spacerItem3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem3)
        self.verticalLayout_6.addLayout(self.verticalLayout_5)
        self.horizontalLayout.addLayout(self.verticalLayout_6)
        self.window_lay.addLayout(self.horizontalLayout)

        self.lab_modif_page.setText("Modifier page/Ajouter des informations à une page")
        self.b_valider.setText("Modifier")
        self.lab_compteur.setText("Créer compteurs")
        self.b_creer_comp.setText("Créer/Modifier")
        self.lab_objets.setText("Créer objets")
        self.b_creer_obj.setText("Créer/Modifier")
        self.checkBox.setText("Cocher cette case si la page est une page de fin")
        self.label.setText("Texte de page")


    def creationPageCompteur(self, livre: Livre):
        """Permet l'affichage du menu permettant de creer des compteurs"""
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_4.setSpacing(10)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        self.pushButton_4 = QPushButton()
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout_4.addWidget(self.pushButton_4, 0, QtCore.Qt.AlignLeft)

        self.widget_list.append(self.pushButton_4)
        self.pushButton_4.clicked.connect(bretour)

        self.label = QLabel()
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.label)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_4.addWidget(self.line)
        self.widget_list.append(self.line)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_2.setSpacing(40)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label_2 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.widget_list.append(self.label_2)

        self.label_3 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.widget_list.append(self.label_3)

        self.lineEdit = QLineEdit()
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.lineEdit)

        self.label_4 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.widget_list.append(self.label_4)

        self.doubleSpinBox = QDoubleSpinBox()
        self.doubleSpinBox.setMinimumSize(QtCore.QSize(150, 0))
        self.doubleSpinBox.setBaseSize(QtCore.QSize(100, 0))
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.verticalLayout.addWidget(self.doubleSpinBox, 0, QtCore.Qt.AlignLeft)
        self.doubleSpinBox.setMaximum(1000000000.0)
        self.widget_list.append(self.doubleSpinBox)

        self.pushButton = QPushButton()
        self.pushButton.setObjectName("pushButton")
        self.widget_list.append(self.pushButton)
        self.pushButton.clicked.connect(partial(bcreerCompteur, self, livre, self.lineEdit, self.doubleSpinBox))

        self.verticalLayout.addWidget(self.pushButton)

        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.line_2 = QFrame()
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_2.addWidget(self.line_2)
        self.widget_list.append(self.line_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_3.setSpacing(20)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.label_5 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_3.addWidget(self.label_5)
        self.widget_list.append(self.label_5)

        self.listWidget = QListWidget()
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_3.addWidget(self.listWidget)
        self.widget_list.append(self.listWidget)
        actualiseListCompteur(self, livre)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)
        # self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.label_6 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
        self.widget_list.append(self.label_6)

        self.doubleSpinBox_2 = QDoubleSpinBox()
        self.doubleSpinBox_2.setMinimumSize(QtCore.QSize(150, 0))
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        self.verticalLayout_2.addWidget(self.doubleSpinBox_2, 0, QtCore.Qt.AlignHCenter)
        self.doubleSpinBox_2.setMaximum(1000000000.0)
        self.widget_list.append(self.doubleSpinBox_2)

        self.listWidget.clicked.connect(partial(selectModifCompteur, self, livre, self.doubleSpinBox_2))

        self.pushButton_2 = QPushButton()
        self.pushButton_2.setMinimumSize(QtCore.QSize(150, 0))
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_2.addWidget(self.pushButton_2, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.pushButton_2)
        self.pushButton_2.clicked.connect(partial(bModifCompteur, self, livre, self.doubleSpinBox_2))

        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_5.setSpacing(20)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem1)

        self.pushButton_3 = QPushButton()
        self.pushButton_3.setMinimumSize(QtCore.QSize(150, 0))
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_5.addWidget(self.pushButton_3, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.pushButton_3)

        self.pushButton_3.clicked.connect(partial(msgBoxSupprimer,partial(bSupprimerCompteur,self,livre,self.doubleSpinBox_2),self.listWidget,
                                                          "Attention supprimer un compteur supprimera également les possibles modifications de compteurs dans vos options. Souhaitez vous continuer ?"))


        self.horizontalLayout.addLayout(self.verticalLayout_5)

        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.window_lay.addLayout(self.verticalLayout_4)

        self.pushButton_4.setText("Retour")
        self.label.setText("Compteurs")
        self.label_2.setText("Créer")
        self.label_3.setText("Nom du compteur")
        self.label_4.setText("Valeur initiale")
        self.pushButton.setText("Valider")
        self.label_5.setText("Modifier")
        self.label_6.setText("Valeur initiale")
        self.pushButton_2.setText("Modifier")
        self.pushButton_3.setText("Supprimer")


    def creationPageObjet(self, livre: Livre):
        self.image_crea = "vide.png"
        self.image = "vide.png"

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_4.setSpacing(20)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        self.pushButton = QPushButton()
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_4.addWidget(self.pushButton, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.pushButton)
        self.pushButton.clicked.connect(bretour)

        self.label = QLabel()
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.label)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_4.addWidget(self.line)
        self.widget_list.append(self.line)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_2.setSpacing(30)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label_2 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.widget_list.append(self.label_2)

        self.label_3 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.widget_list.append(self.label_3)

        self.lineEdit = QLineEdit()
        self.lineEdit.setMinimumSize(QtCore.QSize(150, 0))
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.lineEdit)

        pixmap = QtGui.QPixmap("images/vide.png")
        pixmap = pixmap.scaled(64, 64)
        self.label_6 = QLabel()
        self.label_6.setMinimumSize(QtCore.QSize(64, 64))
        self.label_6.setMaximumSize(QtCore.QSize(64, 64))
        self.label_6.setObjectName("label_6")
        self.label_6.setPixmap(pixmap)
        self.verticalLayout.addWidget(self.label_6, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.label_6)

        self.pushButton_5 = QPushButton()
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout.addWidget(self.pushButton_5)
        self.pushButton_5.setText("Selectionner image")
        self.widget_list.append(self.pushButton_5)
        self.pushButton_5.clicked.connect(partial(choisirImage,self))

        self.pushButton_2 = QPushButton()
        self.pushButton_2.setMinimumSize(QtCore.QSize(150, 0))
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.pushButton_2)
        self.pushButton_2.clicked.connect(partial(bcreerObjet, self, livre, self.lineEdit))

        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.line_2 = QFrame()
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_2.addWidget(self.line_2)
        self.widget_list.append(self.line_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_3.setSpacing(20)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.label_4 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.widget_list.append(self.label_4)

        self.listWidget = QListWidget()
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_3.addWidget(self.listWidget)
        self.widget_list.append(self.listWidget)


        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_2.setSpacing(20)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.label_5 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.label_5)

        self.lineEdit_2 = QLineEdit()
        self.lineEdit_2.setMinimumSize(QtCore.QSize(200, 0))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout_2.addWidget(self.lineEdit_2, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.lineEdit_2)

        self.listWidget.clicked.connect(partial(selectModifObjet, self, self.lineEdit_2,livre))

        self.pushButton_3 = QPushButton()
        self.pushButton_3.setMinimumSize(QtCore.QSize(200, 0))
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_2.addWidget(self.pushButton_3, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.pushButton_3)
        self.pushButton_3.clicked.connect(partial(bModifObjet, self, livre, self.lineEdit_2))

        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_6.setObjectName("verticalLayout_6")

        self.label_7 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_7.setFont(font)
        self.label_7.setText("Modification image")
        self.label_7.setObjectName("label_7")
        self.verticalLayout_6.addWidget(self.label_7, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.label_7)


        pixmap = QtGui.QPixmap("images/vide.png")
        pixmap = pixmap.scaled(64, 64)
        self.label_8 = QLabel()
        self.label_8.setMinimumSize(QtCore.QSize(64, 64))
        self.label_8.setMaximumSize(QtCore.QSize(64, 64))
        self.label_8.setObjectName("label_8")
        self.label_8.setPixmap(pixmap)
        self.verticalLayout_6.addWidget(self.label_8, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.label_8)

        self.pushButton_6 = QPushButton()
        self.pushButton_6.setObjectName("pushButton_6")
        self.verticalLayout_6.addWidget(self.pushButton_6)
        self.horizontalLayout.addLayout(self.verticalLayout_6)
        self.pushButton_6.setText("Selectionner image")
        self.widget_list.append(self.pushButton_6)

        self.pushButton_6.clicked.connect(partial(choisirImageSave,self,self.label_8,livre))

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_5.setSpacing(20)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem1)

        self.pushButton_4 = QPushButton()
        self.pushButton_4.setMinimumSize(QtCore.QSize(200, 0))
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout_5.addWidget(self.pushButton_4, 0, QtCore.Qt.AlignHCenter)
        self.pushButton_4.clicked.connect(partial(bSupprimerObjet, self, livre, self.lineEdit_2))
        self.widget_list.append(self.pushButton_4)
        self.horizontalLayout.addLayout(self.verticalLayout_5)

        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.window_lay.addLayout(self.verticalLayout_4)

        actualiseListObjet(self, livre)

        self.pushButton.setText("Retour")
        self.label.setText("Objets")
        self.label_2.setText("Créer")
        self.label_3.setText("Nom de l\'objet")
        self.pushButton_2.setText("Créer")
        self.label_4.setText("Modifier")
        self.label_5.setText("Modification nom")
        self.pushButton_3.setText("Modifier")
        self.pushButton_4.setText("Supprimer")


    def creationPageOption(self, page: Page):
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_7.setSpacing(20)
        self.verticalLayout_7.setObjectName("verticalLayout_7")

        self.pushButton = QPushButton()
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_7.addWidget(self.pushButton, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.pushButton)
        self.pushButton.clicked.connect(bretour)

        self.label = QLabel()
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_7.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.label)

        self.line_2 = QFrame()
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_7.addWidget(self.line_2)
        self.widget_list.append(self.line_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()

        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label_2 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.widget_list.append(self.label_2)

        self.textEdit = QTextEdit()
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.widget_list.append(self.textEdit)
        self.textEdit.setText(page.texte)

        self.checkBox = QCheckBox()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout.addWidget(self.checkBox)
        self.widget_list.append(self.checkBox)
        self.checkBox.setChecked(page.is_fin)

        self.pushButton_2 = QPushButton()
        self.pushButton_2.setMinimumSize(QtCore.QSize(150, 0))
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.pushButton_2)
        self.pushButton_2.clicked.connect(partial(bmodifInfoPage, page, self.textEdit, self.checkBox))

        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_2.addWidget(self.line)
        self.widget_list.append(self.line)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_6.setSpacing(20)
        self.verticalLayout_6.setObjectName("verticalLayout_6")

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_4.setSpacing(20)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        self.label_3 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.widget_list.append(self.label_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_2.setSpacing(20)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.label_4 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.widget_list.append(self.label_4)

        self.lineEdit = QLineEdit()
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_2.addWidget(self.lineEdit)
        self.widget_list.append(self.lineEdit)

        self.label_7 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(9)

        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_2.addWidget(self.label_7)
        self.label_7.setText("Lien page")
        self.widget_list.append(self.label_7)

        self.spinBox = QSpinBox()
        self.spinBox.setObjectName("spinBox")
        self.verticalLayout_2.addWidget(self.spinBox)
        self.widget_list.append(self.spinBox)

        self.pushButton_3 = QPushButton()
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_2.addWidget(self.pushButton_3)
        self.widget_list.append(self.pushButton_3)

        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_3.setSpacing(20)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.label_5 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_3.addWidget(self.label_5)
        self.widget_list.append(self.label_5)

        self.textEdit_2 = QTextEdit()
        self.textEdit_2.setObjectName("textEdit_2")
        self.verticalLayout_3.addWidget(self.textEdit_2)
        self.widget_list.append(self.textEdit_2)

        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.verticalLayout_6.addLayout(self.verticalLayout_4)

        self.line_3 = QFrame()
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_6.addWidget(self.line_3)
        self.widget_list.append(self.line_3)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_5.setSpacing(20)
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        self.label_6 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_5.addWidget(self.label_6)
        self.widget_list.append(self.label_6)

        self.listWidget = QListWidget()
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_5.addWidget(self.listWidget)
        self.widget_list.append(self.listWidget)
        actualiseListOption(self, page)

        self.pushButton_3.clicked.connect(
            partial(bcreerOption, self, page, self.lineEdit, self.spinBox, self.textEdit_2))

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.pushButton_4 = QPushButton()
        self.pushButton_4.setMinimumSize(QtCore.QSize(150, 0))
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_3.addWidget(self.pushButton_4, 0, QtCore.Qt.AlignHCenter)

        self.widget_list.append(self.pushButton_4)
        self.pushButton_4.clicked.connect(partial(bmenuModifOption, self, page))

        self.pushButton_5 = QPushButton()
        self.pushButton_5.setMinimumSize(QtCore.QSize(150, 0))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.setText("Supprimer")
        self.horizontalLayout_3.addWidget(self.pushButton_5, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.pushButton_5)

        self.pushButton_5.clicked.connect(partial(msgBoxSupprimer,partial(supprimerOption,self,page),self.listWidget,""))

        self.verticalLayout_5.addLayout(self.horizontalLayout_3)

        self.verticalLayout_6.addLayout(self.verticalLayout_5)
        self.horizontalLayout_2.addLayout(self.verticalLayout_6)
        self.verticalLayout_7.addLayout(self.horizontalLayout_2)
        self.window_lay.addLayout(self.verticalLayout_7)

        self.label.setText(page.livre.titre + ": Page " + str(page.numero))
        self.pushButton.setText("Retour")
        self.label_2.setText("Texte de page")
        self.checkBox.setText("Cocher cette case si la page est une page de fin")
        self.pushButton_2.setText("Valider")
        self.label_3.setText("Ajout option")
        self.label_4.setText("Titre")
        self.pushButton_3.setText("Valider")
        self.label_5.setText("Texte Option")
        self.label_6.setText("Modifier Option /ajout conséquences")
        self.pushButton_4.setText("Modifier")


    def menuModifOption(self, option: Option):

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_3.setSpacing(20)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.pushButton = QPushButton()
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_3.addWidget(self.pushButton, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.pushButton)
        self.pushButton.clicked.connect(bretour)

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

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label_5 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.widget_list.append(self.label_5)

        self.label_2 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.widget_list.append(self.label_2)

        self.textEdit = QTextEdit()
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.widget_list.append(self.textEdit)
        self.textEdit.setText(option.texte)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_2.setSpacing(30)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QSpacerItem(120, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_4.setObjectName("verticalLayout_4")


        self.label_3 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.widget_list.append(self.label_3)

        self.lineEdit = QLineEdit()
        self.lineEdit.setMinimumSize(QtCore.QSize(150, 0))
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_4.addWidget(self.lineEdit, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.lineEdit)
        self.lineEdit.setText(option.titre)

        self.label_4 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_4.addWidget(self.label_4)
        self.widget_list.append(self.label_4)

        self.spinBox = QSpinBox()
        self.spinBox.setMinimumSize(QtCore.QSize(150, 0))
        self.spinBox.setObjectName("spinBox")
        self.verticalLayout_4.addWidget(self.spinBox, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.spinBox)
        self.spinBox.setValue(option.num_lien_page)

        self.pushButton_2 = QPushButton()
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_4.addWidget(self.pushButton_2, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.pushButton_2)

        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem1)

        self.pushButton_6 = QPushButton()
        self.pushButton_6.setObjectName("pushButton_6")
        self.verticalLayout_5.addWidget(self.pushButton_6)
        self.widget_list.append(self.pushButton_6)
        self.pushButton_6.setText("Aller à la page : {}".format(option.num_lien_page))
        self.pushButton_6.clicked.connect(partial(connectionLienPage,self,option))

        self.pushButton_2.clicked.connect(
            partial(bmodifOption, option, self.textEdit, self.lineEdit, self.spinBox, self.label,self.pushButton_6))

        spacerItem2 = QSpacerItem(20, 55, QSizePolicy.Minimum, QSizePolicy.Preferred)
        self.verticalLayout_5.addItem(spacerItem2)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        spacerItem3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)

        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.line_2 = QFrame()
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)
        self.widget_list.append(self.line_2)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_2.setSpacing(30)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.label_6 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.label_6)

        self.pushButton_3 = QPushButton()
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_2.addWidget(self.pushButton_3, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.pushButton_3)
        self.pushButton_3.clicked.connect(partial(menuGainObjet,self,option))

        self.line_3 = QFrame()
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_2.addWidget(self.line_3)
        self.widget_list.append(self.line_3)

        self.label_7 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_2.addWidget(self.label_7, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.label_7)

        self.pushButton_4 = QPushButton()
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout_2.addWidget(self.pushButton_4, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.pushButton_4)
        self.pushButton_4.clicked.connect(partial(menuModifCompteur,self,option))

        self.line_4 = QFrame()
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout_2.addWidget(self.line_4)
        self.widget_list.append(self.line_4)

        self.label_8 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_2.addWidget(self.label_8, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.label_8)

        self.pushButton_5 = QPushButton()
        self.pushButton_5.setMinimumSize(QtCore.QSize(220, 0))
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout_2.addWidget(self.pushButton_5, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.pushButton_5)
        self.pushButton_5.clicked.connect(partial(menuConditionDe,self,option))

        self.pushButton_7 = QPushButton()
        self.pushButton_7.setMinimumSize(QtCore.QSize(220, 0))
        self.pushButton_7.setObjectName("pushButton_7")
        self.verticalLayout_2.addWidget(self.pushButton_7, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.pushButton_7)
        self.pushButton_7.clicked.connect(partial(menuConditionCompteur,self,option))

        self.pushButton_8 = QPushButton()
        self.pushButton_8.setMinimumSize(QtCore.QSize(220, 0))
        self.pushButton_8.setObjectName("pushButton_8")
        self.verticalLayout_2.addWidget(self.pushButton_8, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.pushButton_8)
        self.pushButton_8.clicked.connect(partial(menuConditionObjet,self,option))


        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.window_lay.addLayout(self.verticalLayout_3)

        self.pushButton.setText("Retour")
        self.label.setText(option.livre.titre + " Page: " + str(option.page.numero) + ": " + option.titre)
        self.label_5.setText("Modifier")
        self.label_2.setText("Texte d\'option")
        self.label_3.setText("Titre d\'option")
        self.label_4.setText("Lien page")
        self.pushButton_2.setText("Confirmer modification")
        self.label_6.setText("Ajout d\'un gain d\'objet si l\'option est choisie")
        self.pushButton_3.setText("Gerer gain objet")
        self.label_7.setText("Modification d\'un compteur si l\'option est choisie")
        self.pushButton_4.setText("Modification compteurs")
        self.label_8.setText("Ajout de conditions de passage pour l\'option")
        self.pushButton_5.setText("Conditions de passage de dé")
        self.pushButton_7.setText("Conditions de passage de compteurs")
        self.pushButton_8.setText("Conditions de passage d\'objet")


    def menuGainObjet(self, option:Option):
        self.image = "vide.png"
        self.image_crea = "vide.png"


        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_4.setSpacing(20)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        self.pushButton = QPushButton()
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_4.addWidget(self.pushButton, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.pushButton)
        self.pushButton.clicked.connect(bretour)

        self.label = QLabel()
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.label)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_4.addWidget(self.line)
        self.widget_list.append(self.line)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_2.setSpacing(30)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label_2 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.widget_list.append(self.label_2)

        self.label_3 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.widget_list.append(self.label_3)

        self.lineEdit = QLineEdit()
        self.lineEdit.setMinimumSize(QtCore.QSize(150, 0))
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.lineEdit)

        pixmap = QtGui.QPixmap("images/vide.png")
        pixmap = pixmap.scaled(64, 64)
        self.label_6 = QLabel()
        self.label_6.setMinimumSize(QtCore.QSize(64, 64))
        self.label_6.setMaximumSize(QtCore.QSize(64, 64))
        self.label_6.setObjectName("label_6")
        self.label_6.setPixmap(pixmap)
        self.verticalLayout.addWidget(self.label_6, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.label_6)

        self.pushButton_5 = QPushButton()
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout.addWidget(self.pushButton_5)
        self.pushButton_5.setText("Selectionner image")
        self.widget_list.append(self.pushButton_5)
        self.pushButton_5.clicked.connect(partial(choisirImage, self))

        self.pushButton_2 = QPushButton()
        self.pushButton_2.setMinimumSize(QtCore.QSize(150, 0))
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.pushButton_2)
        self.pushButton_2.clicked.connect(partial(baddGainObjet,self,self.lineEdit,option))


        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.line_2 = QFrame()
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_2.addWidget(self.line_2)
        self.widget_list.append(self.line_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_3.setSpacing(20)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.label_4 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.widget_list.append(self.label_4)

        self.listWidget = QListWidget()
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_3.addWidget(self.listWidget)
        self.widget_list.append(self.listWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_2.setSpacing(20)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.label_5 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.label_5)

        self.lineEdit_2 = QLineEdit()
        self.lineEdit_2.setMinimumSize(QtCore.QSize(200, 0))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout_2.addWidget(self.lineEdit_2, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.lineEdit_2)

        self.listWidget.clicked.connect(partial(clickListGainObjet,self,self.lineEdit_2,option))

        self.pushButton_3 = QPushButton()
        self.pushButton_3.setMinimumSize(QtCore.QSize(200, 0))
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_2.addWidget(self.pushButton_3, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.pushButton_3)
        self.pushButton_3.clicked.connect(partial(modifGainObjet,self,self.lineEdit_2,option))


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_6.setObjectName("verticalLayout_6")

        self.label_7 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_7.setFont(font)
        self.label_7.setText("Modification image")
        self.label_7.setObjectName("label_7")
        self.verticalLayout_6.addWidget(self.label_7, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.label_7)

        pixmap = QtGui.QPixmap("images/vide.png")
        pixmap = pixmap.scaled(64, 64)
        self.label_8 = QLabel()
        self.label_8.setMinimumSize(QtCore.QSize(64, 64))
        self.label_8.setMaximumSize(QtCore.QSize(64, 64))
        self.label_8.setObjectName("label_8")
        self.label_8.setPixmap(pixmap)
        self.verticalLayout_6.addWidget(self.label_8, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.label_8)

        self.pushButton_6 = QPushButton()
        self.pushButton_6.setObjectName("pushButton_6")
        self.verticalLayout_6.addWidget(self.pushButton_6)
        self.horizontalLayout.addLayout(self.verticalLayout_6)
        self.pushButton_6.setText("Selectionner image")
        self.widget_list.append(self.pushButton_6)

        self.pushButton_6.clicked.connect(partial(choisirImageSave2, self, self.label_8, option))

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_5.setSpacing(20)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem1)

        self.pushButton_4 = QPushButton()
        self.pushButton_4.setMinimumSize(QtCore.QSize(200, 0))
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout_5.addWidget(self.pushButton_4, 0, QtCore.Qt.AlignHCenter)
        self.pushButton_4.clicked.connect(partial(supprimerGainObjet,self,self.lineEdit_2,option))

        self.widget_list.append(self.pushButton_4)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.window_lay.addLayout(self.verticalLayout_4)

        actualiseListGainObjet(self, option)

        self.pushButton.setText("Retour")
        self.label.setText(option.titre+": Gain objets")
        self.label_2.setText("Ajouter")
        self.label_3.setText("Nom de l\'objet")
        self.pushButton_2.setText("Créer")
        self.label_4.setText("Modifier")
        self.label_5.setText("Modification nom")
        self.pushButton_3.setText("Valider")
        self.pushButton_4.setText("Supprimer")


    def menuModifCompteur(self, option:Option):
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pushButton = QPushButton()
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_3.addWidget(self.pushButton, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.pushButton)
        self.pushButton.clicked.connect(bretour)


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


        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_3.setSpacing(30)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label_4 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.widget_list.append(self.label_4)


        self.label_2 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.widget_list.append(self.label_2)


        self.listWidget = QListWidget()
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.widget_list.append(self.listWidget)
        for compteur in option.livre.compteurs:
            self.listWidget.addItem(compteur.nom)

        self.comboBox = QComboBox()
        self.comboBox.setMinimumSize(QtCore.QSize(150, 0))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("Augmenter")
        self.comboBox.addItem("Diminuer")
        self.comboBox.addItem("Assigner")
        self.verticalLayout.addWidget(self.comboBox, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.comboBox)


        self.label_3 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.widget_list.append(self.label_3)


        self.doubleSpinBox = QDoubleSpinBox()
        self.doubleSpinBox.setMinimumSize(QtCore.QSize(150, 0))
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.verticalLayout.addWidget(self.doubleSpinBox, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.doubleSpinBox)
        self.doubleSpinBox.setMaximum(1000000.0)
        self.doubleSpinBox.setMinimum(-1000000.0)


        self.pushButton_2 = QPushButton()
        self.pushButton_2.setMinimumSize(QtCore.QSize(150, 0))
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.pushButton_2)
        self.pushButton_2.clicked.connect(partial(creerModifCompteur, self, self.comboBox, self.doubleSpinBox, option))


        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.line_2 = QFrame()
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_3.addWidget(self.line_2)
        self.widget_list.append(self.line_2)


        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_2.setSpacing(30)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.label_5 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.widget_list.append(self.label_5)

        self.listWidget_2 = QListWidget()
        self.listWidget_2.setObjectName("listWidget_2")
        self.verticalLayout_2.addWidget(self.listWidget_2)
        self.widget_list.append(self.listWidget_2)
        actualiseListModifCompteur(self,option)


        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")


        self.comboBox_2 = QComboBox()
        self.comboBox_2.setMinimumSize(QtCore.QSize(150, 0))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("Augmenter")
        self.comboBox_2.addItem("Diminuer")
        self.comboBox_2.addItem("Assigner")
        self.widget_list.append(self.comboBox_2)



        self.horizontalLayout_2.addWidget(self.comboBox_2, 0, QtCore.Qt.AlignHCenter)

        self.doubleSpinBox_2 = QDoubleSpinBox()
        self.doubleSpinBox_2.setMinimumSize(QtCore.QSize(150, 0))
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        self.horizontalLayout_2.addWidget(self.doubleSpinBox_2, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.doubleSpinBox_2)
        self.doubleSpinBox_2.setMaximum(1000000.0)
        self.doubleSpinBox_2.setMinimum(-1000000.0)

        self.listWidget_2.clicked.connect(partial(clickListModifCompteur, self, self.comboBox_2, self.doubleSpinBox_2))

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setObjectName("horizontalLayout")


        self.pushButton_3 = QPushButton()
        self.pushButton_3.setMinimumSize(QtCore.QSize(150, 0))
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.pushButton_3)
        self.pushButton_3.clicked.connect(partial(modifModifCompteur,self,self.comboBox_2,self.doubleSpinBox_2,option))



        self.pushButton_4 = QPushButton()
        self.pushButton_4.setMinimumSize(QtCore.QSize(150, 0))
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.pushButton_4)
        self.pushButton_4.clicked.connect(partial(supprimerModifCompteur,self,option))


        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.window_lay.addLayout(self.verticalLayout_3)

        self.pushButton.setText("Retour")
        self.label.setText("Modification compteur")
        self.label_4.setText("Créer")
        self.label_2.setText("Choix compteur")
        self.label_3.setText("Valeur")
        self.pushButton_2.setText("Valider")
        self.label_5.setText("Modifier")
        self.pushButton_3.setText("Modifier")
        self.pushButton_4.setText("Supprimer")


    def menuConditionDe(self, option: Option):
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_8.setSpacing(20)
        self.verticalLayout_8.setObjectName("verticalLayout_8")

        self.pushButton = QPushButton()
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_8.addWidget(self.pushButton, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.pushButton)
        self.pushButton.clicked.connect(bretour)


        self.label = QLabel()
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_8.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.label)


        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_8.addWidget(self.line)
        self.widget_list.append(self.line)


        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(24)
        self.verticalLayout.setObjectName("verticalLayout")

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_9.setObjectName("verticalLayout_9")


        self.label_2 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_9.addWidget(self.label_2)
        self.widget_list.append(self.label_2)


        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")


        self.label_12 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_6.addWidget(self.label_12)
        self.widget_list.append(self.label_12)


        self.spinBox_4 = QSpinBox()
        self.spinBox_4.setMinimumSize(QtCore.QSize(150, 0))
        self.spinBox_4.setMinimum(1)
        self.spinBox_4.setObjectName("spinBox_4")
        self.horizontalLayout_6.addWidget(self.spinBox_4, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.spinBox_4)

        self.verticalLayout_9.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.label_5 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.widget_list.append(self.label_5)


        self.spinBox = QSpinBox()
        self.spinBox.setMinimumSize(QtCore.QSize(150, 0))
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(100)
        self.spinBox.setProperty("value", 1)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout_2.addWidget(self.spinBox, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.spinBox)

        self.verticalLayout_9.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.label_6 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_3.addWidget(self.label_6)
        self.widget_list.append(self.label_6)

        self.spinBox_2 = QSpinBox()
        self.spinBox_2.setMinimumSize(QtCore.QSize(150, 0))
        self.spinBox_2.setMinimum(1)
        self.spinBox_2.setMaximum(100)
        self.spinBox_2.setObjectName("spinBox_2")
        self.horizontalLayout_3.addWidget(self.spinBox_2, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.spinBox_2)


        self.verticalLayout_9.addLayout(self.horizontalLayout_3)

        self.pushButton_2 = QPushButton()
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_9.addWidget(self.pushButton_2, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.pushButton_2)


        self.verticalLayout.addLayout(self.verticalLayout_9)



        self.horizontalLayout_5.addLayout(self.verticalLayout)

        self.line_2 = QFrame()
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_5.addWidget(self.line_2)
        self.widget_list.append(self.line_2)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_7.setSpacing(30)
        self.verticalLayout_7.setObjectName("verticalLayout_7")

        self.label_7 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_7.addWidget(self.label_7)
        self.widget_list.append(self.label_7)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_4.setSpacing(20)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_2.setSpacing(15)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.label_8 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_2.addWidget(self.label_8)
        self.widget_list.append(self.label_8)

        self.comboBox = QComboBox()
        self.comboBox.setMinimumSize(QtCore.QSize(200, 0))
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout_2.addWidget(self.comboBox, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.comboBox)

        self.pushButton_2.clicked.connect(
            partial(ajoutConditionDeSuppr, self, option, self.spinBox_4, self.spinBox, self.spinBox_2))



        self.verticalLayout_5.addLayout(self.verticalLayout_2)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_4.setSpacing(15)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        self.label_9 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_4.addWidget(self.label_9)
        self.widget_list.append(self.label_9)

        self.comboBox_2 = QComboBox()
        self.comboBox_2.setMinimumSize(QtCore.QSize(200, 25))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.verticalLayout_4.addWidget(self.comboBox_2, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.comboBox_2)

        self.verticalLayout_5.addLayout(self.verticalLayout_4)
        self.horizontalLayout_4.addLayout(self.verticalLayout_5)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_6.setObjectName("verticalLayout_6")

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.label_10 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_3.addWidget(self.label_10)
        self.widget_list.append(self.label_10)

        self.spinBox_3 = QSpinBox()
        self.spinBox_3.setMinimum(0)
        self.spinBox_3.setMaximum(1000000)
        self.spinBox_3.setProperty("value", 1)
        self.spinBox_3.setObjectName("spinBox_3")
        self.verticalLayout_3.addWidget(self.spinBox_3)
        self.widget_list.append(self.spinBox_3)

        self.verticalLayout_6.addLayout(self.verticalLayout_3)

        self.pushButton_4 = QPushButton()
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout_6.addWidget(self.pushButton_4)
        self.widget_list.append(self.pushButton_4)

        self.horizontalLayout_4.addLayout(self.verticalLayout_6)
        self.verticalLayout_7.addLayout(self.horizontalLayout_4)


        self.horizontalLayout_5.addLayout(self.verticalLayout_7)
        self.verticalLayout_8.addLayout(self.horizontalLayout_5)

        self.label_4 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_8.addWidget(self.label_4, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.label_4)

        self.listWidget = QListWidget()
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setMinimumSize(QtCore.QSize(800, 0))
        self.verticalLayout_8.addWidget(self.listWidget, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.listWidget)

        actualiseListConditionDe(self, option)

        self.pushButton_3 = QPushButton()
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_8.addWidget(self.pushButton_3, 0, QtCore.Qt.AlignHCenter)
        self.widget_list.append(self.pushButton_3)
        self.pushButton_3.clicked.connect(partial(supprimerConditionDe,self,option))


        self.comboBox.currentTextChanged.connect(partial(changeConditionDe,self,option,self.comboBox,self.comboBox_2,self.spinBox_3))
        self.pushButton_4.clicked.connect(partial(modifConditionDe,self,option, self.comboBox,self.comboBox_2,self.spinBox_3))

        self.window_lay.addLayout(self.verticalLayout_8)

        self.pushButton.setText("Retour")
        self.label.setText("Condition d\'execution de l\'action: Lancé de dé")
        self.label_2.setText("Ajouter un jet")
        self.label_12.setText("Nombre de chances")
        self.label_5.setText("Nombre de dés")
        self.label_6.setText("Nombre de faces ")
        self.pushButton_2.setText("Ajouter")
        self.label_4.setText("Listes des jets")
        self.pushButton_3.setText("Supprimer")
        self.label_7.setText("Ajouter une condition")
        self.label_8.setText("Selection du jet pour la condition")
        self.label_9.setText("Selection de la condition")
        self.comboBox_2.setItemText(0,  "Superieur")
        self.comboBox_2.setItemText(1, "Inferieur")
        self.comboBox_2.setItemText(2,"Egale")
        self.label_10.setText("Résultat cible")
        self.pushButton_4.setText("Valider")


    def menuConditionObjet(self, option:Option):
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_3.setSpacing(20)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.pushButton = QPushButton()
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_3.addWidget(self.pushButton, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.pushButton)
        self.pushButton.clicked.connect(bretour)

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

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label_2 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.widget_list.append(self.label_2)


        self.label_3 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.widget_list.append(self.label_3)


        self.listWidget = QListWidget()
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.widget_list.append(self.listWidget)


        self.checkBox = QCheckBox()
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout.addWidget(self.checkBox)
        self.widget_list.append(self.checkBox)


        self.pushButton_2 = QPushButton()
        self.pushButton_2.setMinimumSize(QtCore.QSize(150, 0))
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.pushButton_2)
        self.pushButton_2.clicked.connect(partial(ajoutConditionObjet,self,option,self.checkBox))


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.line_2 = QFrame()
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)
        self.widget_list.append(self.line_2)


        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_2.setSpacing(20)
        self.verticalLayout_2.setObjectName("verticalLayout_2")


        self.label_4 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.widget_list.append(self.label_4)


        self.listWidget_2 = QListWidget()
        self.listWidget_2.setObjectName("listWidget_2")
        self.verticalLayout_2.addWidget(self.listWidget_2)
        self.widget_list.append(self.listWidget_2)


        self.pushButton_3 = QPushButton()
        self.pushButton_3.setMinimumSize(QtCore.QSize(150, 0))
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_2.addWidget(self.pushButton_3, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.pushButton_3)
        self.pushButton_3.clicked.connect(partial(supprimerConditionObjet,self,option))

        self.pushButton.setText("Retour")
        self.label.setText("Condition d\'execution de l\'action: Possession objet")
        self.label_2.setText("Création de la condition")
        self.label_3.setText("Possession de l\'objet")
        self.checkBox.setText("Supression de l\'objet après utilisation")
        self.pushButton_2.setText("Ajouter")
        self.label_4.setText("Conditions créées")
        self.pushButton_3.setText("Supprimer")


        actualiseListConditionObjet(self, option)


        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.window_lay.addLayout(self.verticalLayout_3)


    def menuConditionCompteur(self,option:Option):

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_3.setSpacing(20)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.pushButton = QPushButton()
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_3.addWidget(self.pushButton, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.pushButton)
        self.pushButton.clicked.connect(bretour)

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


        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")


        self.label_2 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.widget_list.append(self.label_2)


        self.label_3 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.widget_list.append(self.label_3)


        self.listWidget = QListWidget()
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.widget_list.append(self.listWidget)


        self.label_4 =QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.widget_list.append(self.label_4)


        self.comboBox = QComboBox()
        self.comboBox.setMinimumSize(QtCore.QSize(150, 0))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.verticalLayout.addWidget(self.comboBox, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.comboBox)


        self.label_5 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.widget_list.append(self.label_5)


        self.doubleSpinBox = QDoubleSpinBox()
        self.doubleSpinBox.setMinimumSize(QtCore.QSize(150, 0))
        self.doubleSpinBox.setBaseSize(QtCore.QSize(0, 0))
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.doubleSpinBox.setMaximum(float(1000000))
        self.doubleSpinBox.setMinimum(float(-1000000))
        self.verticalLayout.addWidget(self.doubleSpinBox, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.doubleSpinBox)


        self.pushButton_2 = QPushButton()
        self.pushButton_2.setMinimumSize(QtCore.QSize(150, 0))
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2, 0, QtCore.Qt.AlignLeft)
        self.widget_list.append(self.pushButton_2)
        self.pushButton_2.clicked.connect(partial(ajoutConditionCompteur,self,option,self.comboBox,self.doubleSpinBox))


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.line_2 = QFrame()
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)
        self.widget_list.append(self.line_2)


        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_2.setSpacing(20)
        self.verticalLayout_2.setObjectName("verticalLayout_2")


        self.label_6 = QLabel()
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)
        self.widget_list.append(self.label_6)


        self.listWidget_2 = QListWidget()
        self.listWidget_2.setObjectName("listWidget_2")
        self.verticalLayout_2.addWidget(self.listWidget_2)
        self.widget_list.append(self.listWidget_2)


        self.pushButton_3 = QPushButton()
        self.pushButton_3.setMinimumSize(QtCore.QSize(150, 0))
        self.pushButton_3.setObjectName("pushButton_3")
        self.widget_list.append(self.pushButton_3)
        self.pushButton_3.clicked.connect(partial(supprimerConditionCompteur,self,option))

        actualiseListConditionCompteur(self,option)

        self.pushButton.setText("Retour")
        self.label.setText("Condition d\'execution de l\'action : Compteur")
        self.label_2.setText("Création de condition")
        self.label_3.setText("Choix compteur")
        self.label_4.setText("Action de comparaison")
        self.comboBox.setItemText(0,"Superieur")
        self.comboBox.setItemText(1,"Inferieur")
        self.comboBox.setItemText(2, "Egal")
        self.label_5.setText("Valeur de comparaison")
        self.pushButton_2.setText("Ajouter")
        self.label_6.setText("Conditions créées")
        self.pushButton_3.setText("Supprimer")

        self.verticalLayout_2.addWidget(self.pushButton_3, 0, QtCore.Qt.AlignLeft)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.window_lay.addLayout(self.verticalLayout_3)


def run():
    """Lance le programme"""
    import sys

    app = QApplication.instance()
    app = QApplication(sys.argv)

    w = MainWindow()
    w.menuPrincipal()
    w.show()
    app.exec()

run()