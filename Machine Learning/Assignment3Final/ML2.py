import numpy as np
import scipy
import matplotlib.pyplot as plt

# N points in d dimensions
def generatePoints(n,d):
    points = []
    for i in range(0,n):
        point = np.random.normal(0,1,d);
        p = point**2;
        den = np.sqrt(sum(p));
        point = list(point/den);
        points.append(point);
    return points;

def checkPoints(points,northpole,eps,n,d):
    count = 0;
    norm1 = 0;
    norm2 = np.linalg.norm(northpole);
    cosdel = 0;
    for i in range(0,n):
        norm1 = np.linalg.norm(points[i]);
        cosdel = np.dot(points[i],northpole)/(norm1*norm2);

        if(np.absolute(cosdel) <= eps):
            count = count+1;
    return count;

def plotPoints(x,y):
    plt.plot(x,y);

def pointCalculator(points,n,d,norths,norn,eps,k,band):
    count = [];
    npcount = [];
    temp = ();
    plt.figure();
    for i in range(0,norn):
        count = [];
        temp = ();
        for j in range(0,k):
            cpoints = checkPoints(points,norths[i],eps[j],n,d);
            count.append(cpoints);
            if(eps[j] == band):
                temp = (i+1,cpoints);
        npcount.append(temp);
        plotPoints(eps,count);
    plt.xlabel("Band width");
    plt.ylabel("Number of Points in band");
    plt.show();
    return npcount;

n = 500;
d = 50;
points500 = generatePoints(n,d);
points10 = generatePoints(10,d);

# We know from theoretical calculations that most of the points should occur between the narrow band of O(1/sqrt(d))
# Let us take bands of 0.01,0.05,0.1,0.15,0.20,0.25,0.30
xaxis = [0,0.01,0.05,0.1,0.14,0.20,0.25,0.30,0.40,0.45];
print("For dimension = 50 we observe the following:");
pointinband = pointCalculator(points500,n,d,points10,10,xaxis,10,0.14);
print("The following number of points occur in the epsilon band near the equator");
print("(Equator No., Number of Points)");
for i in range(0,10):
    print(pointinband[i]);

print;
print("For dimension = 100 we observe the following:");
# For 100 dimensions
d = 100;
points500 = generatePoints(n,d);
points10 = generatePoints(10,d);
xaxis = [0.0,0.03,0.06,0.09,0.10,0.12,0.15,0.18,0.21,0.24];
# For 100 dimensions
pointinband = pointCalculator(points500,n,d,points10,10,xaxis,10,0.1);
print("The following number of points occur in the epsilon band near the equator");
print("(Equator No., Number of Points)");
for i in range(0,10):
    print(pointinband[i]);


