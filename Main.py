import sys
import requests
from Api import *
from PyQt5.QtWidgets import qApp, QWidget, QPushButton, QLabel, QGridLayout, QApplication, QLineEdit
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

listPokemon = []
currentPokemon = "https://pokeapi.co/api/v2/pokemon/1/"
listEquipe = []
isTeamList = False

class WidgetPokemon(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    # fonction qui sera appelé une seule fois uniquement lors de l'initialisation
    def initUI(self):
        # pokemon est un objet "Pokemon" avec les informations récupérées via l'url du current pokémon
        pokemon = getPokemon(currentPokemon)
        # télécharge les images en écrasant les anciennes quand le pokémon change
        rFront = requests.get(pokemon.frontImg, allow_redirects=True)
        open('front.png', 'wb').write(rFront.content)
        rBack = requests.get(pokemon.backImg, allow_redirects=True)
        open('back.png', 'wb').write(rBack.content)


        # initialisation de tous les attributs
        self.name = QLabel(pokemon.name)
        self.name.setAlignment(Qt.AlignCenter)
        self.heightLabel = QLabel("Taille : ")
        self.height = QLabel(str(pokemon.height))
        self.weightLabel = QLabel("Poids : ")
        self.weight = QLabel(str(pokemon.weight))
        self.typesLabel = QLabel("Type : ")
        self.types = QLabel(pokemon.types)
        self.labelFrontImg = QLabel(self)
        self.frontImg = QPixmap('front.png')
        self.labelFrontImg.setPixmap(self.frontImg)
        self.labelBackImg = QLabel(self)
        self.backImg = QPixmap('back.png')
        self.labelBackImg.setPixmap(self.backImg)
        self.search = QLineEdit()
        self.searchBtn = QPushButton("Rechercher")
        self.searchBtn.clicked.connect(self.getSearchPokemon)
        self.label = QLabel()
        self.indexEquipe = QLabel()
        backBtn = QPushButton("Précédent")
        nextBtn = QPushButton("Suivant")
        addBtn = QPushButton('Ajouter à l''équipe')
        # ce bouton sert à switcher entre la vision du pokédex et de son équipe
        viewTeamBtn = QPushButton('Voir l''équipe/pokédex')
        backBtn.clicked.connect(self.backPokemon)
        nextBtn.clicked.connect(self.nextPokemon)
        addBtn.clicked.connect(self.addToTeam)
        viewTeamBtn.clicked.connect(self.viewTeam)

        # système de grille pour placer tous les éléments 
        grid = QGridLayout()
        grid.addWidget(self.search, 1, 0)
        grid.addWidget(self.searchBtn, 2, 0)
        grid.addWidget(self.label, 0, 3)
        grid.addWidget(self.name, 1, 3)
        grid.addWidget(self.indexEquipe, 1, 5)
        grid.addWidget(self.labelFrontImg, 2, 2)
        grid.addWidget(self.labelBackImg, 2, 4)
        grid.addWidget(self.heightLabel, 3, 0)
        grid.addWidget(self.height, 3, 1)
        grid.addWidget(self.weightLabel, 3, 3)
        grid.addWidget(self.weight, 3, 4)
        grid.addWidget(self.typesLabel, 3, 5)
        grid.addWidget(self.types, 3, 6)
        grid.addWidget(backBtn, 4, 0)
        grid.addWidget(addBtn, 4, 2)
        grid.addWidget(viewTeamBtn, 4, 4)
        grid.addWidget(nextBtn, 4, 5)

        self.setLayout(grid)
        self.setGeometry(300, 300, 200, 200)
        self.show()

    # cette fonction sera appelée à chaque changement de pokémon du pokédex ou de l'équipe
    # elle sert à afficher un pokémon en réattribuant les nouvelles données
    def updateUI(self):
        # même principe que l'initialisation
        pokemon = getPokemon(currentPokemon)
        rFront = requests.get(pokemon.frontImg, allow_redirects=True)
        open('front.png', 'wb').write(rFront.content)
        rBack = requests.get(pokemon.backImg, allow_redirects=True)
        open('back.png', 'wb').write(rBack.content)

        self.label.setText("")
        self.name.setText(pokemon.name)
        self.height.setText(str(pokemon.height))
        self.weight.setText(str(pokemon.weight))
        self.types.setText(pokemon.types)
        self.frontImg = QPixmap('front.png')
        self.labelFrontImg.setPixmap(self.frontImg)
        self.backImg = QPixmap('back.png')
        self.labelBackImg.setPixmap(self.backImg)

    # fonction aller au pokémon précédent 
    def backPokemon(self):
        global currentPokemon
        # La fonction vérifie si on affiche l'équipe ou le pokédex et parcours la bonne liste 
        # mais effectue la même chose pour chaque liste à l'éxception de l'affichage de l'index du pokémon pour l'affichage de l'équipe
        if isTeamList:
            # récupère l'index de la liste du pokémon courant 
            # PS: petit bug ici lorsqu'il y a plusieurs fois le même pokémon dans l'équipe car l'index selectionné sera toujours le même, même en naviguant dans la liste 
            i = listEquipe.index(currentPokemon)
            # navigue au pokémon précédent
            if i == 0:
                i = len(listEquipe) - 1
            else:
                i -= 1
            # redéfinie le bon pokémon courant
            currentPokemon = listEquipe[i]
            self.indexEquipe.setText("Pokémon de votre équipe : " + str(i+1) + "/" + str(len(listEquipe)))
        else:
            i = listPokemon.index(currentPokemon)
            if i == 0:
                i = len(listPokemon) - 1
            else:
                i -= 1
            currentPokemon = listPokemon[i]
        self.updateUI()

    # même chose que pour afficher le pokémon précédent mais en allant à la suite
    def nextPokemon(self):
        global currentPokemon
        if isTeamList:
            i = listEquipe.index(currentPokemon)
            if i == len(listEquipe) - 1:
                i = 0
            else:
                i += 1
            currentPokemon = listEquipe[i]
            self.indexEquipe.setText("Pokémon de votre équipe : " + str(i+1) + "/" + str(len(listEquipe)))
        else:
            i = listPokemon.index(currentPokemon)
            if i == len(listPokemon) - 1:
                i = 0
            else:
                i += 1
            currentPokemon = listPokemon[i]
        self.updateUI()

    # Cette fonction ajoute le pokémon courant dans une liste différente qui contient les urls de chaque pokémon de l'équipe
    def addToTeam(self):
        # l'équipe ne dépasse pas 5 pokémons
        if len(listEquipe) != 5:
            listEquipe.append(currentPokemon)
            self.label.setText("Pokémon ajouté à l'équipe !")
        else:
            self.label.setText("L'équipe ne peux pas contenir plus de 5 pokémon !")

    # cette fonction sert à switcher entre l'affichage de l'équipe et du pokédex
    def viewTeam(self):
        global isTeamList
        global currentPokemon
        # ne peux pas voir la liste de l'équipe si elle est vide
        if len(listEquipe) > 0:
            isTeamList = not isTeamList
            if isTeamList:
                # définit le premier pokémon de l'équipe comme pokémon courant
                currentPokemon = listEquipe[0]
                self.indexEquipe.setText("Pokémon de votre équipe : 1/" + str(len(listEquipe)))
                self.updateUI()
            else:
                self.indexEquipe.setText("")
            print(listEquipe)
        else:
            self.label.setText("L'équipe est vide !")
            
    # cette fonction sert à rechercher un pokémon via son nom
    def getSearchPokemon(self):
        global currentPokemon
        # récupère le text saisie
        search = self.search.text()

        r_api = getAllPokemon()
        
        # Boucle qui permet d'afficher le nom des pokemons de notre liste
        for result in r_api["results"]:
            # si le text saisie correspond à un nom, le current pokémon devient celui qui a correspondu
            if result['name'] == search:

                currentPokemon = result['url']
                self.updateUI()
                self.label.setText("")
                break
            else:
                self.label.setText("Ce pokemon n'existe pas")


def main():
    # requête API
    r_api = getAllPokemon()
    for result in r_api["results"]:
        # stock dans une liste l'url de chaque pokémon
        listPokemon.append(result['url'])
    global currentPokemon
    # le premier pokémon affiché sera le premier de la liste
    currentPokemon = listPokemon[0]

    app = QApplication([])
    w = WidgetPokemon()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
