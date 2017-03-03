import mixem
import numpy as np
import time
from mixem.distribution import NormalDistribution


def readTrainTxt(filename):
    f = open(filename, "r+")
    data = []
    for datum in f.readlines():
        data.append(float(datum))
    return np.asarray(data), len(data)


def takeBatches(data, size):
    shuffledData = np.random.permutation(data)
    return shuffledData[:size]


def main():
    startTime = time.time()
    folderName = "assignment-2-data-files/"
    fileName = "P1M1L1.txt"

    data, lengthData = readTrainTxt(folderName + fileName)
    data = takeBatches(data, 1000)

    init_params = [
        (0, 2),
        (4, 2),
        (8, 2),
        (12, 2)
    ]

    weight, distributions, ll = mixem.em(
        data, [NormalDistribution(mu, sigma) for (mu, sigma) in init_params])

    print(weight, distributions, ll)
    print(time.time() - startTime)


if __name__ == '__main__':
    main()
