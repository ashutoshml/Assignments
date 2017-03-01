import numpy as np
import re


def readTrainTxt(filename):
    f = open(filename, "r+")
    positive = []
    negative = []
    for line in f.readlines():
        lineContent = line.split("\t")
        if(len(lineContent) != 2):
            continue
        if lineContent[0] == "1":
            positive.append(lineContent[1])
        else:
            negative.append(lineContent[1])
    return positive, negative


def removeFancyCharacters(positive, negative):
    positiveLength = len(positive)
    negativeLength = len(negative)
    for i in range(positiveLength):
        positive[i] = re.sub(r'([^\s\w]|_)+', '', positive[i])
    for i in range(negativeLength):
        negative[i] = re.sub(r'([^\s\w]|_)+', '', negative[i])
    return positive, negative


def captureWordCount(phrases):
    length = len(phrases)
    wordDict = {}
    for i in range(length):
        statement = phrases[i]
        words = statement.split()
        for w in words:
            if not(w in wordDict):
                wordDict[w] = 1
            else:
                wordDict[w] += 1
    return wordDict


def totalWords()


def main():
    fileTrain = "ass1-train_data.txt"
    fileTest = "ass1-test_data-2.txt"
    positive, negative = readTrainTxt(fileTrain)
    positive, negative = removeFancyCharacters(positive, negative)
    posDict = captureWordCount(positive)
    negDict = captureWordCount(negative)
    print(posDict)
    print(negDict)


if __name__ == '__main__':
    main()
