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

    def initUI(self):
        pokemon = getPokemon(currentPokemon)
        rFront = requests.get(pokemon.frontImg, allow_redirects=True)
        open('front.png', 'wb').write(rFront.content)
        rBack = requests.get(pokemon.backImg, allow_redirects=True)
        open('back.png', 'wb').write(rBack.content)

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
        backBtn = QPushButton("Précédent")
        nextBtn = QPushButton("Suivant")
        addBtn = QPushButton('Ajouter à l''équipe')
        viewTeamBtn = QPushButton('Voir l''équipe/pokédex')
        backBtn.clicked.connect(self.backPokemon)
        nextBtn.clicked.connect(self.nextPokemon)
        addBtn.clicked.connect(self.addToTeam)
        viewTeamBtn.clicked.connect(self.viewTeam)

        grid = QGridLayout()
        grid.addWidget(self.search, 1, 0)
        grid.addWidget(self.searchBtn, 2, 0)
        grid.addWidget(self.label, 0, 3)
        grid.addWidget(self.name, 1, 3)
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

    def updateUI(self):
        pokemon = getPokemon(currentPokemon)
        rFront = requests.get(pokemon.frontImg, allow_redirects=True)
        open('front.png', 'wb').write(rFront.content)
        rBack = requests.get(pokemon.backImg, allow_redirects=True)
        open('back.png', 'wb').write(rBack.content)

        self.name.setText(pokemon.name)
        self.height.setText(str(pokemon.height))
        self.weight.setText(str(pokemon.weight))
        self.types.setText(pokemon.types)
        self.frontImg = QPixmap('front.png')
        self.labelFrontImg.setPixmap(self.frontImg)
        self.backImg = QPixmap('back.png')
        self.labelBackImg.setPixmap(self.backImg)

    def backPokemon(self):
        global currentPokemon
        if isTeamList:
            i = listEquipe.index(currentPokemon)
            if i == 0:
                i = len(listEquipe) - 1
            else:
                i -= 1
            currentPokemon = listEquipe[i]
        else:
            i = listPokemon.index(currentPokemon)
            if i == 0:
                i = len(listPokemon) - 1
            else:
                i -= 1
            currentPokemon = listPokemon[i]
        self.updateUI()

    def nextPokemon(self):
        global currentPokemon
        if isTeamList:
            i = listEquipe.index(currentPokemon)
            if i == len(listEquipe) - 1:
                i = 0
            else:
                i += 1
            currentPokemon = listEquipe[i]
        else:
            i = listPokemon.index(currentPokemon)
            if i == len(listPokemon) - 1:
                i = 0
            else:
                i += 1
            currentPokemon = listPokemon[i]
        self.updateUI()

    def addToTeam(self):
        if len(listEquipe) != 5:
            listEquipe.append(currentPokemon)
        else:
            print("L'équipe ne peux pas contenir plus de 5 pokémon !")
    
    def viewTeam(self):
        global isTeamList
        global currentPokemon
        # ne peux pas voir la liste de l'équipe si elle est vide
        if len(listEquipe) > 0:
            isTeamList = not isTeamList
            print(isTeamList)
            if isTeamList:
                currentPokemon = listEquipe[0]
                self.updateUI()
            print(listEquipe)
        else:
            print("La liste est vide !")
            
    def getSearchPokemon(self):
        global currentPokemon
        search = self.search.text()

        url = ""

        r_api = getAllPokemon()
        
        # Boucle qui permet d'afficher le nom des pokemons de notre liste
        for result in r_api["results"]:
            if result['name'] == search:

                currentPokemon = result['url']
                self.updateUI()
                self.label.setText("")
                break
            else:
                self.label.setText("Ce pokemon n'existe pas")
        return url


def main():
    r_api = getAllPokemon()
    for result in r_api["results"]:
        listPokemon.append(result['url'])
    global currentPokemon
    currentPokemon = listPokemon[0]

    app = QApplication([])
    w = WidgetPokemon()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
