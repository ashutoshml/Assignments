from svmutil import *
import matplotlib.pyplot as plt
import numpy as np

# remove 'q' from variable 'string' if you wish to see the details regarding iterations, etc.
'''
PART I : Two Features
'''
# TwoFeatures
def twoFeature():
    ytf,xtf = svm_read_problem('twofeature.txt');
    x1 = [];
    x2 = [];
    colors = [];
    for i in range(0,len(xtf)):
        x1.append(xtf[i][1]);
        x2.append(xtf[i][2]);
        if (ytf[i] == -1.0):
            colors.append('g');
        else:
            colors.append('r');
    
    #Trying with various values of C
    cvalues = [1,5,10,20,50,100];
    for i in range(0,len(cvalues)):
        # plotting points
        plt.scatter(x1,x2,c=colors);
        string = '-s 0 -t 0 -q -c '+ str(cvalues[i]); #remove -q for non-quiet mode
        param = svm_parameter(string);
        prob = svm_problem(ytf,xtf);
        model = svm_train(prob,param);
        plotTwoF(model,x1,x2,cvalues[i]);
        plt.show();

# Plotting graphs for various C values
# 6 graphs will be opened for different C values.
def plotTwoF(model,x1,x2,c):
    svc = model.get_sv_coef();
    sv = model.get_SV();
    x = [];
    y = [];
    alpha = []
    for i in range(0,len(sv)):
        x.append(sv[i][1]);
        y.append(sv[i][2]);
        alpha.append(svc[i][0]);
    w1 = np.dot(x,alpha);
    w2 = np.dot(y,alpha);
    
    # w values
    w = [w1,w2];

    maxneg = -100;
    minpos = 10000000;
    for i in range(0,len(svc)):
        if(svc[i][0] < 0):
            if(maxneg < np.dot(w,[x[i],y[i]])):
                    maxneg = np.dot(w,[x[i],y[i]]);
        else:
            if(minpos > np.dot(w,[x[i],y[i]])):
                    minpos = np.dot(w,[x[i],y[i]]);
    # b value
    b = -1 * (maxneg + minpos)/2.0;
    
    pltx = []
    plty = []
    minx = min(x1);
    maxx = max(x1);
    yval = 0;diff = (maxx-minx)/10.0;
    for i in range(0,11):
        pltx.append(minx + diff*i);
        yval = (-1*(w1*(minx+diff*i) + b-1))/w2;
        plty.append(yval);
   
    # line plot
    plt.plot(pltx,plty);
    plt.title("C value = " + str(c));
    plt.xlabel("x1");
    plt.ylabel("x2");


'''
PART II: Email Classification
'''
# Email Classification
def email_class():
    y50,x50 = svm_read_problem('email_train-50.txt');
    y100,x100 = svm_read_problem('email_train-100.txt');
    y400,x400 = svm_read_problem('email_train-400.txt');
    yall,xall = svm_read_problem('email_train-all.txt');
    
    # c = 1
    model50 = svm_train(y50,x50, '-s 0 -t 0 -q -c 1');
    model100 = svm_train(y100,x100,'-s 0 -t 0 -q -c 1');
    model400 = svm_train(y400,x400,'-s 0 -t 0 -q -c 1');
    modelall = svm_train(yall,xall,'-s 0 -t 0 -q -c 1');
    
    y,x = svm_read_problem('email_test.txt');
    p_labs50, p_acc50, p_vals50 = svm_predict(y, x, model50);
    p_labs100, p_acc100, p_vals100 = svm_predict(y, x, model100);
    p_labs400, p_acc400, p_vals400 = svm_predict(y, x, model400);
    p_labsall, p_accall, p_valsall = svm_predict(y, x, modelall);
    
    return p_acc50[0], p_acc100[0], p_acc400[0], p_accall[0];

# Print solution to file
def printAccuracy(p1,p2,p3,p4):
    print("The solution can be seen above. If you wish, you may open Solution.txt for solution");
    filename = "Solution.txt";
    target = open(filename,'w');
    target.write("The following is the accuracy on the test data for the various training data: \n");
    target.write("For 50 documents, Accuracy = " + str(p1) + "%\n");
    target.write("For 100 documents, Accuracy = " + str(p2) + "%\n");
    target.write("For 400 documents, Accuracy = " + str(p3) + "%\n");
    target.write("For all documents, Accuracy = " + str(p4) + "%\n");
    target.write("Please note that there was no previous assignment on Naive Bayes classification so printed just accuracy through SVM on test data");
    target.close();

def main():
    print("Two features:");
    print("6 graphs will be opened for various values of C(mentioned in the title). Please check and close each graph.\n");
    twoFeature();
    print("Email Classification(Linear model):"); # to change model change the -t value in svm_train in email_class. 1 for polynomial, 2 for radial, etc.
    p1,p2,p3,p4 = email_class();
    printAccuracy(p1,p2,p3,p4);

if __name__ == "__main__":
    main();


