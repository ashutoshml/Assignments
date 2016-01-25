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

    '''
    Initially calculated frequency of each characters,
    to match it with the statistical frequency of characters that appear in most
    English words.
    '''
    frequent = frequencyCalculator(inputCipher);
    print "Frequencies of various characters in the cipher is :";
    print frequent;

    sorted_freq = sortFreqOnValue(frequent);
    statFrequencyofCharacters = readFromFileAsList(filenameFreq);

    '''
    Sorted the character data based on frequency values and initialized it based on
    frequency of characters in english words(statistical data).
    '''
    print "\nInitial Substitution based on popularity of characters in a text:";
    initialSub = initialReplace(statFrequencyofCharacters,sorted_freq);
    print initialSub;

    '''
    After analyzing various words (assuming the letter E took the correct position)
    replaced each letter with a letter which made a sensible english letter (trial and error).
    Calculating a digram or trigram seemed like an overkill for this question.
    '''
    analyzedSub = analyzedReplace(filenameReplace);
    print "\nFinal Substitution:";
    print analyzedSub;

    '''
    Used the above substitution rule to replace each cipher character by the analyzed character
    '''
    decipher = decipheredText(analyzedSub, inputCipher);

    print "\nDeciphered Text:";
    print decipher;

    '''
    For text without spaces, the general idea would be to first calculate frequency, digram and trigram
    and analyze the cipher text after initial substitution. For certain words which when joined together
    form a new word itself, the word will/will not be separated based on the context.
    For eg., the deciphered word might look like "alphabeta" which may either mean "alpha beta" or "alphabet a"
    In science context, we may assume that it to be alpha beta.
    In case of normal english plaintext, we may assume it to be alphabet a.
    '''

if __name__ == "__main__":
    main();
