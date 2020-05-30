import math
import copy
from read_input import Clique
class classicalBayesianEncoder():
    def __init__(self):
        self.endOfLine = "0\n"
        self.cnfFileName = "encodingBayesian.cnf"
        self.weightFileName = "weightFile.txt"

    def integer2Bits(self, numBits, value):
        bitArray = []
        for i in range(numBits-1, -1, -1):
            bitArray.append(value & (1 << i) != 0)
        return bitArray[::-1]
    
    def bits2Integer(self, bits):
        res = 0
        for i in range(len(bits)):
            if bits[i]:
                res += math.pow(2, i)
        return int(res)
    
    def locateWeightValue(self, integerBits, conditionalTable):
        if integerBits[0]:
            secondIdx = 1
        else:
            secondIdx = 0
        # print(integerBits)
        firstIdx = self.bits2Integer(integerBits[1:])
        # print(firstIdx)
        return conditionalTable[firstIdx][secondIdx]

    def CNFHeader(self, cnfFile, weightFile, numVariables, cliques, queries):
        totalNumVariables = 2 * numVariables
        totalNumClauses = 2 * numVariables
        for clique in cliques:
            totalNumVariables += int(math.pow(2, len(clique.variables)))
            totalNumClauses += int(math.pow(2, len(clique.variables))) * (len(clique.variables) + 1)
        totalNumClauses += len(queries)
        cnfFile.write("c CS4244 Encoding Bayesian Network to CNF formula\n")
        cnfFile.write("p cnf " + str(totalNumVariables) + " " + str(totalNumClauses) + "\n")
        weightFile.write("p " + str(totalNumVariables) + "\n")

    def TypeOneConstraints(self, cnfFile, weightFile, numVariables):
        for i in range(numVariables):
            cnfFile.write("-"+str(2*i)+" "+str(2*i+1)+" "+self.endOfLine)
            cnfFile.write("-"+str(2*i+1)+" "+str(2*i)+" "+self.endOfLine)
            weightFile.write("w -"+str(2*i)+" "+str(1.0)+" "+self.endOfLine)
            weightFile.write("w "+str(2*i)+" "+str(1.0)+" "+self.endOfLine)
            weightFile.write("w -"+str(2*i+1)+" "+str(1.0)+" "+self.endOfLine)
            weightFile.write("w "+str(2*i+1)+" "+str(1.0)+" "+self.endOfLine)
    
    def TypeTwoConstraints(self, cnfFile, weightFile, numVariables, cliques):
        parameterVariableID = 2 * numVariables
        for clique in cliques:
            variables = copy.deepcopy(clique.variables)
            totalNumCombinations = int(math.pow(2, len(variables)))
            for i in range(totalNumCombinations):
                integerBits = self.integer2Bits(len(variables), i)
                leftImplication = ""
                rightImplication = ""
                for j in range(len(integerBits)):
                    variableId = variables[len(integerBits) - 1 - j]
                    if integerBits[j]:
                        indicatorVariable = 2 * variableId
                    else:
                        indicatorVariable = 2 * variableId + 1
                    rightImplication = "-" + str(parameterVariableID) + " " + str(indicatorVariable) + " " + self.endOfLine
                    cnfFile.write(rightImplication)
                    leftImplication += "-" + str(indicatorVariable) + " "
                leftImplication += str(parameterVariableID) + " " + self.endOfLine
                cnfFile.write(leftImplication)

                positiveWeightValue = self.locateWeightValue(integerBits, clique.conditionalTable)
                weightFile.write("w -"+str(parameterVariableID)+" "+str(positiveWeightValue)+" "+self.endOfLine)
                weightFile.write("w "+str(parameterVariableID)+" "+str(1.0)+" "+self.endOfLine)
                parameterVariableID += 1

    def queriesProcessing(self, cnfFile, queries):
        for key, value in queries.items():
            if value:
                indicatorVariable = 2 * key
            else:
                indicatorVariable = 2 * key + 1
            cnfFile.write(str(indicatorVariable)+" "+self.endOfLine)

    def encoding(self, numVariables, cliques, queries):
        print("Processing CNF and WMC...")
        cnfFile = open(self.cnfFileName, "w")
        weightFile = open(self.weightFileName, "w")
        self.CNFHeader(cnfFile, weightFile, numVariables, cliques, queries)
        self.TypeOneConstraints(cnfFile, weightFile, numVariables)
        self.TypeTwoConstraints(cnfFile, weightFile, numVariables, cliques)
        self.queriesProcessing(cnfFile, queries)
        cnfFile.close()
        weightFile.close()
        print("Processed.")