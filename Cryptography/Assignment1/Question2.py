import operator

def readFromFileAsString(fileName):
    fileInput = open(fileName,"r");
    inputAsAString = "";
    for line in fileInput:
        inputAsAString = inputAsAString + line;

    fileInput.close();
    return inputAsAString;

def readFromFileAsList(filename):
    fileInput = open(filename,"r");
    inputAsAList = []

    for line in fileInput:
        inputAsAList.append(line[0]);

    fileInput.close();
    return inputAsAList;

# Calculate frequency of letters in the given cipher text
def frequencyCalculator(inputCipher):
    frequent = {};

    # Assigns zero to the frequency of each letter (initialization)
    for i in range(65,91):
        frequent[chr(i)] = 0;

    for i in range(0,len(inputCipher)):
        if(ord(inputCipher[i])>=65 and ord(inputCipher[i])<=90):
            frequent[inputCipher[i]] = frequent[inputCipher[i]] + 1;
        elif(ord(inputCipher[i])>=97 and ord(inputCipher[i])<=122):
            frequent[chr(ord(inputCipher[i])-32)] = frequent[chr(ord(inputCipher[i])-32)] + 1;

    return frequent;

def sortFreqOnValue(frequent):
    sorted_freq = sorted(frequent.items(), key=operator.itemgetter(1),reverse=True);
    return sorted_freq;

def initialReplace(statisticalFrequencyOfCharacters, sorted_freq):
    replace = {}
    for i in range(0,len(sorted_freq)):
        replace[sorted_freq[i][0]]= statisticalFrequencyOfCharacters[i];

    print "Initial substitution also written in file keyValueQuestion2.txt for initial substitution";
    initialReplaceinFile = open("keyValueQuestion2.txt","w");
    lst = replace.items();
    for i in range(0,len(lst)):
        initialReplaceinFile.write(lst[i][0] + ":" +lst[i][1]+"\n");
    initialReplaceinFile.close();

    return replace;

def analyzedReplace(filename):
    replace = {}
    filereadFreq = open(filename,"r");

    for line in filereadFreq:
        line = line.replace("\n","");
        ba = line.split(":");
        replace[ba[0]] = ba[1];
    filereadFreq.close();

    return replace;

def decipheredText(replace, inputString):
    decipher = ""
    for i in range(0,len(inputString)):
        if((ord(inputString[i]) >=65 and ord(inputString[i])<=90) or (ord(inputString[i]) >=97 and ord(inputString[i])<=122)):
            decipher = decipher + replace[inputString[i]];
        else:
            decipher = decipher + inputString[i];

    return decipher;

def main():
    filenameCipher = "Cipher2.txt";
    filenameFreq = "statFrequencyofCharacters.txt";
    filenameReplace = "Subscheme2.txt";

    inputCipher = readFromFileAsString(filenameCipher);
    statisticalFrequencyOfCharacters = readFromFileAsList(filenameFreq);

    print "Initial Text:";
    print(inputCipher);

    frequent = frequencyCalculator(inputCipher);
    print "Frequencies of various characters in the cipher is :";
    print frequent;

    sorted_freq = sortFreqOnValue(frequent);
    statFrequencyofCharacters = readFromFileAsList(filenameFreq);

    print "\nInitial Substitution based on popularity of characters in a text:";
    initialSub = initialReplace(statFrequencyofCharacters,sorted_freq);
    print initialSub;

    analyzedSub = analyzedReplace(filenameReplace);
    print "\nFinal Substitution:";
    print analyzedSub;

    decipher = decipheredText(analyzedSub, inputCipher);

    print "\nDeciphered Text:";
    print decipher;

if __name__ == "__main__":
    main();
