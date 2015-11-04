import numpy as np
import matplotlib.pyplot as plt
import math
import pandas

# Batch Gradient Descent
def BGD(alpha,x,y,iterate,n):
    cn = np.ones(2)
    x_transpose = x.T
    iterationBGD = 0
    conv = False
    maxlim = np.asarray([1000000]*2)
    eps = np.asarray([0.00001]*2)
    for i in range(0,iterate):
        if conv == False:
            ci = cn
            h = np.dot(x,cn)
            loss = h - y
            iterationBGD = iterationBGD + 1
            tmp = np.atleast_2d(loss)
            #Jc = np.sum(np.dot(tmp,tmp.T)) / (2*n)
            gradient = np.dot(x_transpose, loss)/n
            cn = cn - alpha*gradient
            boolc = (abs(cn - ci) <= eps)
            boolmax = (abs(cn - cn) >= maxlim)
            boolmaxtemp = False;
            for i in range(0,len(boolmax)):
                boolmaxtemp = boolmaxtemp + boolmax[i]
            if boolmaxtemp == True:
                break
            conv = True
            for i in range(0,len(boolc)):
                conv = conv * boolc[i]
        else:
            break
    if conv == False:
        print("does not converge")
    return cn,iterationBGD

# Read data from file
def readData():
    filename = "ex3x.dat"
    c = 0
    sampleData = []
    k = pandas.read_csv(filename,sep= "   ",header=None)
    for i in range(0,len(k)):
        xtemp = []
        xtemp.append(1)
        xtemp.append(k[0][i])
        xtemp.append(k[1][i])
        sampleData.append(xtemp)
    return sampleData

# Separate x and y values
def sepValue(k):
    y = []
    x = []
    for i in range(0,len(k)):
        xtemp = []
        xtemp.append(k[i][0])
        xtemp.append(k[i][1])
        x.append(xtemp)
        y.append(k[i][2])
    return np.asarray(x),np.asarray(y)

# Find closed form solution
def closedForm(x,y):
    x_transpose = x.T
    ccf = np.dot(np.dot(np.linalg.inv(np.dot(x_transpose,x)),x_transpose),y)
    return ccf

# Normalize the given vector
def normalize(x):
    m = np.mean(x[:,1])
    std = np.std(x[:,1])
    x[:,1] = (x[:,1] - m)/std
    return x

# Stochastic Gradient Descent
def SGD(alpha,x,y,n):
    c = [1,1]
    eps = 0.0000001
    maxlim = 100000
    ctemp = []
    conv = False
    k = 0
    while (not conv) and k<=100000:
        for i in range(0,n):
            k = k + 1
            h = c[0]*x[i][0] + c[1]*x[i][1]
            ctemp = []
            ctemp.append(c[0])
            ctemp.append(c[1])
            c[0] = c[0] - alpha*(h - y[i])*x[i][0]
            c[1] = c[1] - alpha*(h - y[i])*x[i][1]
            if ((abs(c[0] - ctemp[0])<= eps) and (abs(c[1] - ctemp[1])<= eps)):
                conv = True
                break
            elif ((abs(c[1]-ctemp[1]) >= maxlim) or  (abs(c[1]-ctemp[1]) >= maxlim)):
                print("Does not converge for alpha",alpha)
                break
    return c,k

print("Due to large number of iteration the process may take time. Please be patient")
# Reading values from file
samData = readData()
x,y = sepValue(samData)

# Running batch gradient for the given inputs alpha = 0.0001 and max iterations = 100000
print("For the initial input the function" ),
n, itr = BGD(0.001,x,y,100000,len(y))

# Calculating closed form values
m = closedForm(x,y)
print("Closed form values:" + str(m))

# Normalizing x
normalize(x)
alpha = [0.3,0.1,0.03,0.01,0.003,0.001,0.0003,0.0001,0.00003,0.00001]
n = [0]*len(alpha)
itr = [0]*len(alpha)
print("Normalizing Done. After normalizing x the function gives"),
for i in range(0, len(alpha)):
    n[i], itr[i] = BGD(alpha[i],x,y,100000,len(y))
print(n[i])

# Stochastic gradient descent 
ns,itrs = SGD(0.0001,x,y,len(y))
print("Running stochastic gradient descent on normalized input:"),
print(ns),
print("|| No. of iterations until convergence:"),
print(itrs)

# Permuting data
permData = np.random.permutation(samData)
x1,y1 = sepValue(permData)
normalize(x1)

# Stochastic gradient descent on normalized and permuted data
ns,itrs = SGD(0.0001,x1,y1,len(y))
print("Running stochastic gradient descent on normalized and permuted data:"),
print(ns),
print("|| No. of iterations until convergence:"),
print(itrs)

# Plotting iterations vs alpha (For scaling using -log alpha)
plt.figure(1)
plt.plot((-1*np.log10(alpha)),itr, 'r')
plt.xlabel("-log alpha -> ")
plt.ylabel("Iterations")
plt.title("Iteration vs alpha")
plt.show()


