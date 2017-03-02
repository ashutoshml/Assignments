import re
import time


def readTrainTxt(filename):
    f = open(filename, "r+")
    positive = []
    negative = []
    for line in f.readlines():
        lineContent = line.split("\t")
        if(len(lineContent) != 2):
            continue
        if lineContent[0] == "1":
            positive.append(lineContent[1].lower())
        else:
            negative.append(lineContent[1].lower())
    return positive, negative


def readTestTxt(filename):
    f = open(filename, "r+")
    labels = []
    text = []
    for line in f.readlines():
        lineContent = line.split("\t")
        if(len(lineContent) != 2):
            continue
        labels.append(int(lineContent[0]))
        text.append(lineContent[1].lower())
    return labels, text


def removeFancyChars(phrases):
    lengthPhrase = len(phrases)
    for i in range(lengthPhrase):
        phrases[i] = re.sub(r'([^\s\w]|_)+', '', phrases[i])
    return phrases


def removeFancyCharacters(positive, negative):
    positive = removeFancyChars(positive)
    negative = removeFancyChars(negative)
    return positive, negative


def listDef(wordList, length, phrases):
    for i in range(length):
        statement = phrases[i]
        words = statement.split()
        for w in words:
            wordList.append(w)
    return list(set(wordList))


def captureWordList(positive, negative):
    lengthPos = len(positive)
    lengthNeg = len(negative)
    wordList = []
    wordList = listDef(wordList, lengthPos, positive)
    wordList = listDef(wordList, lengthNeg, negative)
    return wordList


def wordCountLabel(wordList, phrases):
    probWord = {}
    length = len(phrases) + 2.0
    for key in wordList:
        count = 1.0
        for p in phrases:
            words = list(set(p.split()))
            if key in words:
                count += 1.0
        probWord[key] = count / length
    return probWord


def train(fileTrain):
    positive, negative = readTrainTxt(fileTrain)
    positive, negative = removeFancyCharacters(positive, negative)
    wordList = captureWordList(positive, negative)

    ccd1 = wordCountLabel(wordList, positive)
    ccd0 = wordCountLabel(wordList, negative)

    return ccd0, ccd1


def getAccuracy(predictedLabels, actualLabels):
    acc = 0.0
    total = len(predictedLabels)
    for i in range(total):
        if predictedLabels[i] == actualLabels[i]:
            acc += 1
    return ((acc * 100.0) / total + 0.0)


def posterior0(text, ccd0):
    words = list(set(text.split()))
    posteriorVal = 1.0
    for w in words:
        if w in ccd0:
            posteriorVal *= ccd0[w]
    return posteriorVal


def posterior1(text, ccd1):
    words = list(set(text.split()))
    posteriorVal = 1.0
    for w in words:
        if w in ccd1:
            posteriorVal *= ccd1[w]
    return posteriorVal


def predict(text, ccd0, ccd1):
    if posterior0(text, ccd0) > posterior1(text, ccd1):
        return 0
    return 1


def test(fileTest, ccd0, ccd1):
    actualLabels, text = readTestTxt(fileTest)
    text = removeFancyChars(text)
    predictedLabels = []
    for t in text:
        predictedLabels.append(predict(t, ccd0, ccd1))
    accuracy = getAccuracy(predictedLabels, actualLabels)
    return predictedLabels, accuracy


def main():
    t = time.time()
    fileTrain = "ass1-train_data.txt"
    fileTest = "ass1-test_data-2.txt"
    ccd0, ccd1 = train(fileTrain)
    predictLabelsTrain, accuracyTrain = test(fileTrain, ccd0, ccd1)
    predictLabelsTest, accuracyTest = test(fileTest, ccd0, ccd1)
    print "Prediction Accuracy on train set: " + str(accuracyTrain)
    print "Prediction Accuracy on test set: " + str(accuracyTest)
    print "Total time taken: " + str(time.time() - t)


if __name__ == '__main__':
    main()
