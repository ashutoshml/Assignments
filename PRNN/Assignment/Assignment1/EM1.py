import numpy as np
import time
import scipy.stats as st


size = 4
muStart = 6
sigmaStart = 2
batchSize = None
iterations = 500


def initializeMu(size, muStart, sigmaStart):
    mu = np.random.normal(muStart, 6, size)
    sigma = np.random.normal(sigmaStart, 1, size)
    lambdaValue = np.random.dirichlet(np.ones(size), size=1)[0]
    # mu = np.asarray([0.0, 4.0, 8.0, 12.0])
    # sigma = np.asarray([2.0, 2.0, 2.0, 2.0])
    # lambdaValue = np.asarray([0.25, 0.25, 0.25, 0.25])
    return mu, sigma, lambdaValue


def readTrainTxt(filename):
    f = open(filename, "r+")
    data = []
    for datum in f.readlines():
        data.append(float(datum))
    return np.asarray(data), len(data)


def takeBatches(data, size):
    shuffledData = np.random.permutation(data)
    return shuffledData[:size]


def getDensityValue(data, mu, sigma):
    pdf = []
    for datum in data:
        pdf.append(st.norm(mu, sigma).pdf(datum))
    return np.asarray(pdf)


def getDensity(data, mu, sigma):
    return st.norm(mu, sigma).pdf(data)


def expectation(gamma, lambdaValue, mu, sigma, data):
    eVal = 0.0

    for i in range(len(data)):
        internal = 0.0
        for j in range(len(mu)):
            internal += gamma[i][j] * np.log(
                lambdaValue[j] * getDensity(data[i], mu[j], np.sqrt(sigma[j])))
        eVal += internal
    return eVal


def EM(data, size, mu, sigma, lambdaValue):
    dataSize = len(data)
    gamma = np.zeros((dataSize, size))

    for k in range(iterations):

        print "Iteration " + str(k + 1) + " in progress"
        startTime = time.time()

        denominatorGammai = np.dot(
            lambdaValue, getDensityValue(data, mu, np.sqrt(sigma)).T)

        for j in range(size):

            numeratorGammai = lambdaValue[
                j] * getDensityValue(data, mu[j], np.sqrt(sigma[j]))
            gamma[:, j] = numeratorGammai / denominatorGammai

        for j in range(size):

            numeratorMu = np.dot(data, gamma[:, j])
            denominatorMu = np.sum(gamma[:, j])
            numeratorSigma = np.dot(np.square(data - mu[j]), gamma[:, j])
            denominatorSigma = denominatorMu

            mu[j] = numeratorMu / denominatorMu
            lambdaValue[j] = np.mean(gamma[:, j])
            sigma[j] = numeratorSigma / denominatorSigma

        print expectation(gamma, lambdaValue, mu, sigma, data)
        print mu
        print sigma
        print lambdaValue
        print "Iteration " + str(k + 1) + " over in " + str(time.time() - startTime)

    return mu, sigma, lambdaValue


def main():
    startTime = time.time()
    folderName = "assignment-2-data-files/"
    fileName = "P1M1L1.txt"

    data, lengthData = readTrainTxt(folderName + fileName)
    data = takeBatches(data, 200)
    mu, sigma, lambdaValue = initializeMu(size, muStart, sigmaStart)
    mu, sigma, lambdaValue = EM(data, size, mu, sigma, lambdaValue)
    print str(mu)
    print str(sigma)
    print str(lambdaValue) + str(np.sum(lambdaValue))

    print "Final time consumed: " + str(time.time() - startTime)


if __name__ == '__main__':
    main()
