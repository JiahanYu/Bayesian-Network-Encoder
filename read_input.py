import copy
import math
class Clique():
    def __init__(self, variables):
        self.variables = copy.deepcopy(variables)
        entries = int(math.pow(2, len(variables)))
        self.conditionalTable = []
    def setConditionalTable(self, conditionalTable):
        self.conditionalTable = copy.deepcopy(conditionalTable)

class uaiReader():
    def __init__(self):
        self.cliques = []
        self.queries = {}
        self.numVariables = 0
        self.maxAri = -1
        self.numOfTuples = 0
    def readInput(self, filePath, fileType):
        if fileType == "model":
            print("Loading model file...")
            file = open(filePath,"r")
            firstLine = file.readline().rstrip()
            if firstLine != "BAYES": 
                print("The model file is not correct.")
                file.close()
                exit();
            secondLine = file.readline().rstrip()
            self.numVariables = int(secondLine)
            thirdLine = file.readline().rstrip()
            for card in thirdLine.split(" "):
                if int(card) != 2:
                    print("Now this encoder can only support Bayesian Network with cardinality equals to 2.")
                    file.close()
                    exit();
            fourthLine = file.readline().rstrip()
            numCliques = int(fourthLine)
            for i in range(numCliques):
                line = file.readline().rstrip()
                lineInformation = line.split(" ")
                numVariablesInClique = int(lineInformation[0])
                self.maxAri = max(self.maxAri, numVariablesInClique)
                variablesInClique = []
                for j in range(numVariablesInClique):
                    variablesInClique.append(int(lineInformation[j+1]))
                self.cliques.append(Clique(variablesInClique))

            emptyLine = file.readline()

            for i in range(numCliques):
                line = file.readline().rstrip()
                numEntries = int(line)
                self.numOfTuples += numEntries
                conditionalTable = [[0 for y in range(2)] for x in range(numEntries//2)]
                for j in range(numEntries//2):
                    informationLine = file.readline().strip()
                    probability = informationLine.split(" ")
                    if len(probability) != 2:
                        print("The conditional probability table length should be 2 for Bayesian Network.")
                        file.close()
                        exit();
                    for k in range(2):
                        conditionalTable[j][k] = float(probability[k])
                self.cliques[i].setConditionalTable(conditionalTable)
                # emptyLine = file.readline()
            file.close()
            print("maxAri:", self.maxAri)
            print("tuple:", self.numOfTuples)
            print("Model file loaded.")
        elif fileType == "evidence":
            print("Loading evidence file...")
            file = open(filePath, "r")
            onlyOneLine = file.readline().rstrip()
            lineInformation = onlyOneLine.split(" ")
            numObservedVariables = int(lineInformation[0])
            if len(lineInformation) != 2 * numObservedVariables + 1:
                print("Evidence file has wrong number of observed variables.")
                file.close()
                exit();
            for i in range(numObservedVariables):
                if lineInformation[2*i + 2] == "0":
                    self.queries[int(lineInformation[2*i + 1])] = False
                else:
                    self.queries[int(lineInformation[2*i + 1])] = True
            file.close()
            print("Evidence file loaded.")
        else:
            print("We don't support this kind of file type.")
            exit();