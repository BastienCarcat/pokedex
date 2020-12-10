class Pokemon:
    def __init__(self, name, height, weight, types):
        self.name = name
        self.height = height
        self.weight = weight
        self.types = types

    def getPokemon(self):
        print("Nom : " + self.name + "\nPoids : " + self.height + " Taille : " + self.height + "\nTypes : " + self.types)