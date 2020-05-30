import math
import copy
from read_input import Clique
class CNFFormula():
    def __init__(self):
        self.formula = []
    def getNumOfClauses(self):
        return len(self.formula)
    def addOneClause(self, clause):
        self.formula.append(clause)
    def addOneFormula(self, newFormula):
        for clause in newFormula.formula:
            self.formula.append(clause)
    def or1Var(self, variable):
        size = self.getNumOfClauses()
        if size == 0:
            self.formula.append([variable])
        else:
            for clause in self.formula:
                clause.append(variable)
    def and1Var(self,variable):
        self.addOneClause([variable])


class probBayesianEncoder():
    def __init__(self):
        self.endOfLine = "0\n"
        self.cnfFileName = "encodingBayesian.cnf"
        self.weightFileName = "weightFile.txt"
        self.clauses = 1
        self.hmap = {}
        self.probs = {}
    
    def CNFEncoderBasic(self, numVariables):
        res = CNFFormula()
        for i in range(numVariables):
            clause = []
            for j in range(2):
                key = str(i) + " " + str(j)
                self.hmap[key] = self.clauses
                self.probs[self.clauses] = 1
                self.probs[-self.clauses] = 1
                clause.append(self.clauses)
                # print("seed:", self.clauses)
                self.clauses += 1

            res.addOneClause(clause)

            for j in range(1, 2):
                for k in range(0, 1):
                    singleClause = []
                    key1 = str(i) + " " + str(j)
                    key2 = str(i) + " " + str(k)
                    singleClause.append(-self.hmap[key1])
                    singleClause.append(-self.hmap[key2])
                    res.addOneClause(singleClause)
        return res

    def CNFEncoderMain(self, numVariables, cliques):
        # for clique in cliques:
        #     print(clique.conditionalTable)
        res = CNFFormula()
        for i in range(numVariables):
            variables = cliques[i].variables
            # variables.append(i)
            pos = len(variables) - 1
            arr = [0 for x in range(pos+1)]
            idx1 = idx2 = 0
            while pos >= 0:
                paramClause = CNFFormula()
                for j in range(len(variables)):
                    if j != len(variables) - 1:
                        key = str(cliques[i].variables[j]) + " " + str(arr[j])
                        paramClause.or1Var(-self.hmap[key])
                paramClause.or1Var(self.hmap[str(i)+" "+str(arr[len(variables) - 1])])
                # print(idx2, idx1, pos)
                # print(cliques[i].conditionalTable)
                tempProb = cliques[i].conditionalTable[idx2][idx1]
                tempProb2 = 1.0
                for j in range(arr[len(variables) - 1]):
                    tempProb2 -= cliques[i].conditionalTable[idx2][int(not idx1)]
                    paramClause.or1Var(self.clauses - j - 1)
                if arr[len(variables) - 1] != 1:
                    tempProb = tempProb / tempProb2
                    paramClause.or1Var(-self.clauses)
                    self.probs[self.clauses] = tempProb
                    self.probs[-self.clauses] = 1 - tempProb
                    self.clauses += 1
                res.addOneFormula(paramClause)
                flag = False
                while pos >= 0 and arr[pos] == 1:
                    pos -= 1
                    flag = True
                idx1 += 1
                if idx1 == 2:
                    idx2 += 1
                    idx1 = 0
                if pos >= 0:
                    arr[pos] += 1
                    if flag:
                        for j in range(pos+1, len(variables)):
                            arr[j] = 0
                        pos = len(variables) - 1
        return res

    def CNFEncoderEvidence(self, queries):
        evidence = CNFFormula()
        for key, value in queries.items():
            evidence.and1Var(self.hmap[str(key-1)+" "+str(int(value))])
        return evidence
    
    def resOutput(self, finalFormula):
        cnfFile = open(self.cnfFileName, "w")
        weightFile = open(self.weightFileName, "w")
        cnfFile.write("c CS4244 Encoding Bayesian Network to CNF formula\n")
        cnfFile.write("p cnf "+str(self.clauses-1)+" "+str(finalFormula.getNumOfClauses())+"\n")
        for clause in finalFormula.formula:
            for variable in clause:
                if variable > 0:
                    variable -= 1
                else:
                    variable += 1
                cnfFile.write(str(variable)+" ")
            cnfFile.write(self.endOfLine)
        
        weightFile.write("p "+str(self.clauses-1)+"\n")
        for key, value in self.probs.items():
            weightFile.write("w "+str(key)+" "+str(float(value))+" "+self.endOfLine)
        
        cnfFile.close()
        weightFile.close()
        
    
    def encoding(self, numVariables, cliques, queries):
        firstFormula = self.CNFEncoderBasic(numVariables)
        secondFormula = self.CNFEncoderMain(numVariables, cliques)
        thirdFormula = self.CNFEncoderEvidence(queries)
        finalFormula = CNFFormula()
        finalFormula.addOneFormula(firstFormula)
        finalFormula.addOneFormula(secondFormula)
        finalFormula.addOneFormula(thirdFormula)
        self.resOutput(finalFormula)
