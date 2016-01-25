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

    print "Initial substitution also written in file keyValueQuestion1.txt for initial substitution";
    initialReplaceinFile = open("keyValueQuestion1.txt","w");
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
        if((ord(inputString[i]) >=65 and ord(inputString[i])<=90)):
            decipher = decipher + replace[inputString[i]];
        elif (ord(inputString[i]) >=97 and ord(inputString[i])<=122):
            decipher = decipher + chr(ord(replace[chr(ord(inputString[i])-32)])+32);
        else:
            decipher = decipher + inputString[i];

    return decipher;

def ngram(inputString,n):
    ngramFrequency = {}
    inputString = inputString.replace("-\n","");
    inputString = inputString.replace("\n"," ");
    for i in range(0,len(inputString)-n+1):
        stringKey = inputString[i:i+n];
        flag = 0;

        for j in range(0,len(stringKey)):
            ch = stringKey[j];
            if(ch == " " or not(ord(ch)>=65 and ord(ch)<=90) and not(ord(ch)>=97 and ord(ch)<=122)):
                flag = 1;
                break;

        if (flag == 0):
            if(stringKey in ngramFrequency):
                ngramFrequency[stringKey] = ngramFrequency[stringKey] + 1;
            else:
                ngramFrequency[stringKey] = 1;

    return ngramFrequency;

def Caesar(filename):
    cipher = open(filename,"r+");
    a = ""
    for line in cipher:
        a = a + line;

    ans26 = [];
    ans = ""
    for j in range(0,26):
        ans = ""
        for i in range(0,len(a)):
            num = ord(a[i]);
            if((num>=65 and num<=90)):
                ans = ans + chr(65 + (ord(a[i])+j-65)%26);
            elif((num>=97 and num<=122)):
                ans = ans + chr(97 + (ord(a[i])+j-97)%26);
            else:
                ans = ans + a[i];
        ans26.append(ans);

    print("After examination of the deciphered text, we can see that the following plaintext makes sense:\n");
    print ans26[23]
    cipher.close();

def printToFile(fileName, lst):
    outputFile = open(fileName,"w");
    for i in range(0,len(lst)):
        outputFile.write(lst[i][0] + ":" +str(lst[i][1])+"\n");
    outputFile.close();

def main():
    filenameCipher = "Cipher1.txt";
    filenameFreq = "statFrequencyofCharacters.txt";
    filenameReplace = "Subscheme1.txt";

    inputCipher = readFromFileAsString(filenameCipher);
    statisticalFrequencyOfCharacters = readFromFileAsList(filenameFreq);

    '''
    Read initial cipher text
    '''
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

    '''
    Digram
    '''
    print("\nFrequencies of two successive characters is:");
    digramFreq = ngram(inputCipher,2);
    print sortFreqOnValue(digramFreq);
    print("\nOpen file diGramQuestion1.txt to see frequency of two successive characters in a better format.");
    printToFile("diGramQuestion1.txt",sortFreqOnValue(digramFreq));

    '''
    Trigram
    '''
    print("\nFrequencies of three successive characters is:");
    trigramFreq = ngram(inputCipher,3);
    print sortFreqOnValue(trigramFreq);
    print("\nOpen file triGramQuestion1.txt to see frequency of three successive characters in a better format.");
    printToFile("triGramQuestion1.txt",sortFreqOnValue(trigramFreq));

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
    After some iterations, it became clear that it is a Caesar cipher
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

    print "The cipher text is infact just a simple Caesar cipher"
    Caesar(filenameCipher)

if __name__ == "__main__":
    main();
