from colorama import Fore, Style, init
init()
class Couleur:
    ROUGE = Fore.RED
    VERT = Fore.GREEN
    ORANGE = Fore.YELLOW
    FIN = Style.RESET_ALL


class Order:
    ASCEND = True
    DESCENTE = False


class Voiture:
    def __init__(self, marque, modele, cv, immat):
        self.marque = marque
        self.modele = modele
        self.cv = cv
        self.immat = immat

    def showMarque(self):
        print(self.marque)

    @staticmethod    # Une méthode statique n'a pas besoin d'être initialisé avec le construteur (self)
    def demarrer():
        print("...La voiture démarre")
