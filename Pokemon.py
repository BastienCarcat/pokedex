class Pokemon:
    def __init__(self, name, height, weight, frontImg, backImg):
        self.name = name
        self.height = height
        self.weight = weight
        self.frontImg = frontImg
        self.backImg = backImg
        # self.types = types

    # def getName():
    #     return self.name
    # def getHeight():
    #     return str(self.height)
    # def getWeight():
    #     return str(self.weight)

    def getInfo(self):
        print("Nom : " + self.name + "\nPoids : " + str(self.weight) + " Taille : " + str(self.height))