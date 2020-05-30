import math
import copy
from read_input import Clique
class dependenceBayesianEncoder():
    def __init__(self):
        self.endOfLine = "0\n"
        self.cnfFileName = "encodingBayesian.cnf"
        self.weightFileName = "weightFile.txt"
        self.sourceNode = []

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
    
    def getSourceNode(self, cliques):
        for clique in cliques:
            if len(clique.variables) == 1:
                self.sourceNode.append(clique.variables[0])
    
    def CNFHeader(self, cnfFile, weightFile, numVariables, cliques, queries):
        totalNumVariables = numVariables
        totalNumClauses = 0
        for clique in cliques:
            sizeOfClique = len(clique.variables)
            if sizeOfClique > 1:
                totalNumVariables += int(math.pow(2, sizeOfClique-1))
                totalNumClauses += 2 * int(math.pow(2, sizeOfClique-1))
        totalNumClauses += len(queries)
        cnfFile.write("c CS4244 Encoding Bayesian Network to CNF formula\n")
        cnfFile.write("p cnf " + str(totalNumVariables) + " " + str(totalNumClauses) + "\n")
        weightFile.write("p " + str(totalNumVariables) + "\n")
    
    def nodeEncoder(self, cnfFile, weightFile, numVariables, cliques):
        literalId = numVariables
        stateNodeEncoded = []
        for clique in cliques:
            variables = clique.variables
            if len(variables) == 1:
                weightFile.write("w -"+str(variables[0])+" "+str(clique.conditionalTable[0][1])+" "+self.endOfLine)
                weightFile.write("w "+str(variables[0])+" "+str(clique.conditionalTable[0][0])+" "+self.endOfLine)
                stateNodeEncoded.append(variables[0])
            else:
                for var in variables:
                    if (var not in self.sourceNode) and (var not in stateNodeEncoded):
                        weightFile.write("w -"+str(var)+" "+str(1.0)+" "+self.endOfLine)
                        weightFile.write("w "+str(var)+" "+str(1.0)+" "+self.endOfLine)
                        stateNodeEncoded.append(var)
                impliedBayesianNodeStateVarId = variables[-1]
                numChanceNodes = int(math.pow(2, len(variables)-1))
                for i in range(numChanceNodes):
                    bits = self.integer2Bits(len(variables)-1, i)
                    leftSideImplication = ""
                    for j in range(len(bits)):
                        if bits[j]:
                            leftSideImplication += "-" + str(variables[j]) + " "
                        else:
                            leftSideImplication += str(variables[j]) + " "
                    literalIdOfChanceNode = literalId + i
                    cnfFile.write(leftSideImplication + "-" + str(impliedBayesianNodeStateVarId) + " " + str(literalIdOfChanceNode) + " " + self.endOfLine)
                    cnfFile.write(leftSideImplication + "-" + str(literalIdOfChanceNode) + " " + str(impliedBayesianNodeStateVarId) + " " + self.endOfLine)
                    weightFile.write("w -"+str(literalIdOfChanceNode)+" "+str(clique.conditionalTable[i][1])+" "+self.endOfLine)
                    weightFile.write("w "+str(literalIdOfChanceNode)+" "+str(clique.conditionalTable[i][0])+" "+self.endOfLine)
                literalId += numChanceNodes
    
    def queriesProcessing(self, cnfFile, queries):
        for key, value in queries.items():
            if value:
                indicatorVariable = "-" + str(key)
            else:
                indicatorVariable = str(key)
            cnfFile.write(indicatorVariable+" "+self.endOfLine)

    def encoding(self, numVariables, cliques, queries):
        print("Processing CNF and WMC...")
        cnfFile = open(self.cnfFileName, "w")
        weightFile = open(self.weightFileName, "w")
        self.CNFHeader(cnfFile, weightFile, numVariables, cliques, queries)
        self.getSourceNode(cliques)
        self.nodeEncoder(cnfFile, weightFile, numVariables, cliques)
        self.queriesProcessing(cnfFile, queries)
        cnfFile.close()
        weightFile.close()
        print("Processed.")