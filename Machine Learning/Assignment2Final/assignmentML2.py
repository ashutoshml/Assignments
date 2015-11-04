import numpy as np
import matplotlib.pyplot as plt
import math
from scipy import stats

def generateDataPoints(n):
    x = []
    xi = np.zeros(5)
    xi[0] = 1
    for i in range(0,n):
        for j in range(1,5):
            xi[j] = math.floor(np.random.uniform(0,100))
        x.append(xi)
        xi = np.zeros(5)
        xi[0] = 1
    return np.asarray(x)

def generateConstants():
    c = np.zeros(5)
    for i in range(0,5):
        c[i] = math.floor(np.random.uniform(0,10))
    return np.asarray(c)

def generateErrors(n):
    e = np.zeros(n)
    for i in range(0,n):
        e[i] = np.random.random()
    return np.asarray(e)

def computeYi(x,c,e,n):
    y = np.zeros(n)
    for i in range(0,n): 
        k = np.atleast_2d(x[i])
        l = np.dot(c,k.T)
        y[i] = l[0] + e[i]
    return y

def BGD(alpha,x,y,iterate,n):
    cn = np.ones(5)
    x_transpose = x.T
    for i in range(0,iterate):
        h = np.dot(x,cn)
        loss = h - y
        tmp = np.atleast_2d(loss)
        #Jc = np.sum(np.dot(tmp,tmp.T)) / (2*n)
        gradient = np.dot(x_transpose, loss)/n
        cn = cn - alpha*gradient
    return cn

def closedForm(x,y):
    x_transpose = x.T
    ccf = np.dot(np.dot(np.linalg.inv(np.dot(x_transpose,x)),x_transpose),y)
    return ccf

print("Due to high amount of iterations the solution may take around 30 secs. to print. Please be patient")
# Generating 5 data sets, each comprising 102 sample points
xp = []
n = 102
for i in range(0,5):
    xp.append(generateDataPoints(n))

# Generating initial constants based on which y is calculated
c = generateConstants()

# Generating errors based on normal distribution
e = generateErrors(n)

# Computing y based on the above equations
yp = []
for i in range(0,5):
    yp.append(computeYi(xp[i],c,e,n))

# Running batch gradient on the data set
alpha = 0.0001
iteration = 200000
cn = []
for i in range(0,5):
    cn.append(BGD(alpha,xp[i],yp[i],iteration,n))

# Computing closed form solution
ccf = []
for i in range(0,5):
    ccf.append(closedForm(xp[i],yp[i]))

print("Initial assumption for constants is : " +str(c))
print("Closed form solution is : " + str(np.mean(ccf,axis = 0)))
print("Solution through batch gradient is : "+str(np.mean(cn,axis = 0)))
