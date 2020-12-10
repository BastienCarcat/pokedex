import sys
from Api import *
from PyQt5.QtWidgets import qApp, QAction, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QApplication

listPokemon = []
currentPokemon = "https://pokeapi.co/api/v2/pokemon/1/"


class WidgetPokemon(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        pokemon = getPokemon(currentPokemon)
        self.name = QLabel(pokemon.name)
        self.heightLabel = QLabel("Taille : ")
        self.height = QLabel(str(pokemon.height))
        self.weightLabel = QLabel("Poids : ")
        self.weight = QLabel(str(pokemon.weight))
        self.typesLabel = QLabel("Types : ")
        self.types = QLabel(pokemon.types)

        grid = QGridLayout()
        grid.addWidget(self.name, 0, 2)
        grid.addWidget(self.heightLabel, 1, 0)
        grid.addWidget(self.height, 1, 1)
        grid.addWidget(self.weightLabel, 1, 3)
        grid.addWidget(self.weight, 1, 4)
        grid.addWidget(self.typesLabel, 2, 3)
        grid.addWidget(self.types, 2, 4)

        self.setLayout(grid)
        self.setGeometry(300, 300, 200, 200)
        self.show()


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
