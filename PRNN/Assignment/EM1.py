import numpy as np
import time
import mixem


size = 4
muStart = 5
sigmaStart = 2
batchSize = None


def initializeMu(size, muStart, sigmaStart):
    mu = np.random.normal(muStart, 5, size)
    sigma = np.random.normal(sigmaStart, 5, size)
    lambdaValue = np.random.dirichlet(np.ones(size), size=1)
    return mu, sigma, lambdaValue


def readTrainTxt(filename):
    f = open(filename, "r+")
    data = []
    for datum in f.readlines():
        data.append(float(datum))
    return data, len(data)


def EM():
    return 1


def calculatelikelihood(data):
    return 1


def takeBatches(data, size):
    return data[:size]


def main():
    folderName = "assignment-2-data-files"
    fileName = "P1M1L1.txt"
    data, lengthData = readTrainTxt(folderName + fileName)
    mu, sigma, lambdaValue = initializeMu(size, muStart, sigmaStart)
    


if __name__ == '__main__':
    main()
