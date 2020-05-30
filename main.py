import sys
import datetime
from read_input import uaiReader
from classicalEncoder import classicalBayesianEncoder
from dependenceEncoder import dependenceBayesianEncoder
from probEncoder import probBayesianEncoder
if __name__ == "__main__":
    print("Usage: python main.py [EncoderType] [modelFilePath] [evidenceFilePath]")
    inputReader = uaiReader()
    if len(sys.argv) != 4:
        print("Please read the Usage")
    else:
        inputReader.readInput(sys.argv[2], "model")
        inputReader.readInput(sys.argv[3], "evidence")
        if sys.argv[1] == "classical":
            encoder = classicalBayesianEncoder()
        elif sys.argv[1] == "dependence":
            encoder = dependenceBayesianEncoder()
        elif sys.argv[1] == "prob":
            encoder = probBayesianEncoder()
        else:
            print("We didn't support this encoder type.")
            exit();
        startTime = datetime.datetime.now()
        encoder.encoding(inputReader.numVariables, inputReader.cliques, inputReader.queries)
        endTime = datetime.datetime.now()
        print("Running Time:", endTime-startTime)