import random
#nr 11 in grupa

class SteepestAscentHillClimbing:

    def __init__(self, file_name):
        self.nrObiecte = 0
        self.listaValori = []
        self.listaGreutati = []
        self.capacitateRucsac = 0
        self.nrRepetari = 0
        self.nrMemeorie = 0
        self.readFromFile(file_name)

    def readFromFile(self, file_name):
        file = open(file_name, 'r')
        lines = file.readlines()

        self.nrObiecte = int(lines[0])
        self.listaGreutati = [0] * self.nrObiecte
        self.listaValori = [0] * self.nrObiecte
        for i in range(0, self.nrObiecte):
            valoriLinie = lines[i + 1].split()
            self.listaValori[int(valoriLinie[0]) - 1] = \
                int(valoriLinie[1])
            self.listaGreutati[int(valoriLinie[0]) - 1] = \
                int(valoriLinie[2])
        self.capacitateRucsac = int(lines[self.nrObiecte + 1])
        self.nrRepetari = int(lines[self.nrObiecte + 2])
        self.nrMemeorie = int(lines[self.nrObiecte + 3])

    def getRandomBitList(self, nrObiecte):
        list = []
        for i in range(0, nrObiecte):
            list.append(random.getrandbits(1))
        return list

    def getNeighbours(self, listaBinara):
        neighbours = []
        for i in range(0, self.nrObiecte):
            neighbour = listaBinara.copy()
            neighbour[i] = 1 if neighbour[i] == 0 else 0
            neighbours.append(neighbour)
        return neighbours

    def getSumOfList(self, listaBinara, lista, n):
        suma = 0
        for i in range(0, n):
            if listaBinara[i] != 0:
                suma += lista[i]
        return suma

    def getFitness(self, listaBinara):
        greutatea = self.getSumOfList(listaBinara, self.listaGreutati, self.nrObiecte)
        sumaValori = self.getSumOfList(listaBinara, self.listaValori, self.nrObiecte)
        return sumaValori if greutatea <= self.capacitateRucsac else 0

    def getBestNeighbourNonTabu(self, neighbours, memoria):
        solutiaOptima = 0
        neighbourX = []
        bit = -1

        for idx, neighbour in enumerate(neighbours):
            neighbourFitnes = self.getFitness(neighbour)
            if neighbourFitnes > solutiaOptima and memoria[idx] == 0:
                solutiaOptima = neighbourFitnes
                bit = idx
                neighbourX = neighbour

        return [neighbourX, solutiaOptima, bit]

    def updateMemory(self, memoria, bit):
        for i in range(0, self.nrObiecte):
            memoria[i] = memoria[i] - 1 if memoria[i] != 0 else 0

        memoria[bit] = self.nrMemeorie

        return memoria

    def getOptimalSolution(self):
        listBinara = self.getRandomBitList(self.nrObiecte)
        solutiaOptima = self.getFitness(listBinara)

        while solutiaOptima == 0:
            listBinara = self.getRandomBitList(self.nrObiecte)
            solutiaOptima = self.getFitness(listBinara)

        memoria = [0] * self.nrObiecte

        for i in range(0, self.nrRepetari):
            neighbours = self.getNeighbours(listBinara)
            bestNeighbour = self.getBestNeighbourNonTabu(neighbours, memoria)
            self.updateMemory(memoria, bestNeighbour[2])
            listBinara = bestNeighbour[0]
            if bestNeighbour[1] > solutiaOptima:
                solutiaOptima = bestNeighbour[1]

        return solutiaOptima

class Menu:
    def __init__(self, randomSearch):
        self.randomSearch = randomSearch

    def readK(self):
        self.randomSearch.nrRepetari = int(input('K= '))

    def optimalSolution(self):
        result = self.randomSearch.getOptimalSolution()
        if result == 0:
            print('Nu au existat solutii valide')
        else:
            print('Solutia este: ' + str(result))

    def print_menu(self):
        print('Alegeti o optiune: \n'
              '\t1. Citeste un nou k\n'
              '\t2. Determina solutia\n'
              '\tx. quit\n')

    def start(self):
        options = {
            1: self.readK,
            2: self.optimalSolution
        }

        while True:
            self.print_menu()
            option = input('Alegerea este: ')

            if option == 'x':
                print('Meersi!')
                quit()
            try:
                options[int(option)]()
            except KeyError as e:
                print("Alegeti o optiune valida! " + str(e) + " nu exista!")

if __name__ == '__main__':
    randomSearch = SteepestAscentHillClimbing('rucsac-20.txt')
    menu = Menu(randomSearch)
    menu.start()
