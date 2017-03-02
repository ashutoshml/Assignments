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


def setDef(wordSet, length, phrases):
    for i in range(length):
        statement = phrases[i]
        words = statement.split()
        for w in words:
            wordSet.add(w)
    return wordSet


def capturewordSet(positive, negative):
    lengthPos = len(positive)
    lengthNeg = len(negative)
    wordSet = set()
    wordSet = setDef(wordSet, lengthPos, positive)
    wordSet = setDef(wordSet, lengthNeg, negative)
    return wordSet


def wordCountLabel(wordSet, phrases):
    probWord = {}
    length = len(phrases) + 2.0
    for key in wordSet:
        count = 1.0
        for p in phrases:
            words = set(p.split())
            if key in words:
                count += 1.0
        probWord[key] = count / length
    return probWord


def train(fileTrain):
    positive, negative = readTrainTxt(fileTrain)
    positive, negative = removeFancyCharacters(positive, negative)
    wordSet = capturewordSet(positive, negative)

    ccd1 = wordCountLabel(wordSet, positive)
    ccd0 = wordCountLabel(wordSet, negative)

    return ccd0, ccd1


def getAccuracy(predictedLabels, actualLabels):
    acc = 0.0
    total = len(predictedLabels)
    for i in range(total):
        if predictedLabels[i] == actualLabels[i]:
            acc += 1
    return ((acc * 100.0) / total + 0.0)


def posterior(text, ccd):
    words = set(text.split())
    posteriorVal = 1.0
    for w in words:
        if w in ccd:
            posteriorVal *= ccd[w]
    return posteriorVal


def predict(text, ccd0, ccd1):
    if posterior(text, ccd0) > posterior(text, ccd1):
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
