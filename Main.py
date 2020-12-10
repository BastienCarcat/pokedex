import sys
import requests
from Api import *
from PyQt5.QtWidgets import qApp, QWidget, QPushButton, QLabel, QGridLayout, QApplication, QLineEdit
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

listPokemon = []
currentPokemon = "https://pokeapi.co/api/v2/pokemon/1/"


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

# Pensez a remettre les types Qlabel et tous le bordel gros chien

        self.name = QLabel(pokemon.name)
        self.name.setAlignment(Qt.AlignCenter)
        self.heightLabel = QLabel("Taille : ")
        self.height = QLabel(str(pokemon.height))
        self.weightLabel = QLabel("Poids : ")
        self.weight = QLabel(str(pokemon.weight))
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
        backBtn.clicked.connect(self.backPokemon)
        nextBtn.clicked.connect(self.nextPokemon)

        grid = QGridLayout()
        grid.addWidget(self.search, 1, 0)
        grid.addWidget(self.searchBtn, 2, 0)
        grid.addWidget(self.label, 0, 3)
        grid.addWidget(self.name, 1, 3)
        grid.addWidget(self.labelFrontImg, 2, 2)
        grid.addWidget(self.labelBackImg, 2, 4)
        grid.addWidget(self.heightLabel, 3, 0)
        grid.addWidget(self.height, 3, 1)
        grid.addWidget(self.weightLabel, 3, 5)
        grid.addWidget(self.weight, 3, 6)
        grid.addWidget(backBtn, 4, 0)
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
        self.frontImg = QPixmap('front.png')
        self.labelFrontImg.setPixmap(self.frontImg)
        self.backImg = QPixmap('back.png')
        self.labelBackImg.setPixmap(self.backImg)

    def backPokemon(self):
        global currentPokemon
        i = listPokemon.index(currentPokemon)
        if i == 0:
            i = len(listPokemon) - 1
        else:
            i -= 1
        currentPokemon = listPokemon[i]
        self.updateUI()

    def nextPokemon(self):
        global currentPokemon
        i = listPokemon.index(currentPokemon)
        if i == len(listPokemon) - 1:
            i = 0
        else:
            i += 1
        currentPokemon = listPokemon[i]
        self.updateUI()

    def getSearchPokemon(self):
        global currentPokemon
        search = self.search.text()

        url = ""

        r_search_pokemon = requests.get(
            'https://pokeapi.co/api/v2/pokemon?limit=151&offset=0')
    # verification que la requête est bien effectuée
        if r_search_pokemon.status_code == 200:
            # on integre le resultat de la requête dans une variable
            result_rsp = r_search_pokemon.json()

            # Boucle qui permet d'afficher le nom des pokemons de notre liste
            for result in result_rsp["results"]:
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
