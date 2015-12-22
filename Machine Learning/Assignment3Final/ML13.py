import numpy as np
import scipy
import math
import matplotlib.pyplot as plt

# N points on the surface in d dimensions
def generatePoints(n,d):
    points = [] # Points on the surface
    pointsG = [] # Gaussian points mean = 0 var = 1
    for i in range(0,n):
        point = np.random.normal(0,1,d);
        pointsG.append(point);
        p = point**2;
        den = np.sqrt(sum(p));
        point = list(point/den);
        points.append(point);
    return points,pointsG;

# N points in the sphere in d dimensions
def generateInternalPoints(n,d):
    points = []
    for i in range(0,n):
        point = np.random.normal(0,1,d);
        p = point**2;
        u = np.random.uniform(0,1);
        ust = pow(u,(1.0/d));
        den = np.sqrt(sum(p));
        point = point*ust;
        point = list(point/den);
        points.append(point);
    return points;

# Function to plot point on the graph
def plotPoints(points,n, d, title):
    plt.figure();
    v = [x for x in range(1,n+1)];
    h = [];
    for i in range(0,d):
        h = [points[x][i] for x in range(0,n)];
        plt.plot(v,h,'ro');
        h = [];
    plt.title(title);
    plt.xlabel("Dimension");
    plt.ylabel("Corresponding x(i)");
    plt.show();

# Calculates the bounds
def findAlpha(points,n,d):
    alpha = [];
    h = []
    for i in range(0,d):
        h = [points[x][i] if points[x][i] > 0 else -1*points[x][i]  for x in range(0,n)];
        ar = np.asarray(h);
        alpha.append(ar.max()*np.sqrt(50.0));
    return alpha;

def projection(points,subspace,n):
    projPoint = []
    subspacet = np.asarray(subspace);
    subspace = subspacet.T;
    for i in range(0,n):
        inv = np.linalg.inv(np.dot(subspacet,subspace));
        proj = np.dot(np.dot(np.dot(subspace,inv),subspacet),points[i]);
        projPoint.append(proj);
    return projPoint;

def projectionsub(points,subspace,n,n2):
    projsub = []
    for i in range(0,n2):
        projsub.append(projection(points,subspace[i],n));
    return projsub;

def plotProj(points,subspace,n,n2,d,k):
    projLine = projectionsub(points,subspace,n,n2);
    for i in range(0,n2):
        plt.figure();
        if (k!=1): 
		dist = [np.linalg.norm(projLine[i][j]) for j in range(0,n)];
	else:
		dist = [np.linalg.norm(projLine[i][j]) if np.dot(projLine[i][j],subspace[i][0]) >=0 else -1*np.linalg.norm(projLine[i][j]) for j in range(0,n)];
        plt.hist(dist,bins = 20);
        plt.xlabel("Distances from origin");
        plt.ylabel("Frequencies");
        plt.show();          
    return projLine;

def meanVar(points,d):
    mean = []
    for i in range(0,d):
        meani = np.mean(points[i],axis = 0);
        mean.append(meani);
        cov = np.cov(points[i],rowvar = 0);
    return mean,cov;

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

def pointCalculator(points,n,d,norths,norn,eps,k,band):
    count = [];
    npcount = [];
    temp = ();
    for i in range(0,norn):
        count = [];
        temp = ();
        for j in range(0,k):
            cpoints = checkPoints(points,norths[i],eps[j],n,d);
            count.append(cpoints);
            if(eps[j] == band):
                temp = (i+1,cpoints);
        npcount.append(temp);
    return npcount;
 
def main():
    n = 200;
    d = 50;
    # Generating 200 points on the surface of the ball
    points,pointsG = generatePoints(n,d);

    # Generating 200 points inside the ball
    pointsInternal = generateInternalPoints(n,d);
 
    plotPoints(points,n,d,"Surface Points");
    plotPoints(pointsInternal,n,d,"Internal Points");

    alpha = findAlpha(points,n,d);
    alpha2 = findAlpha(pointsInternal,n,d);

    northPole, northPoleG = generatePoints(1,d);

    xaxis = [0.15];
    print("For dimension = 50 and for surface points, we observe that the points inside the band:");
    pointinband = pointCalculator(points,n,d,northPole,1,xaxis,1,0.15);
    print(pointinband[0]);
    
    print("For dimension = 50 and for internal points, we observe that the points inside the band:");
    pointinband = pointCalculator(pointsInternal,n,d,northPole,1,xaxis,1,0.15);
    print(pointinband[0]);

    print("For subspace of dimension 1 we observe the following");
    print("10 graphs will be opened. Please check and close each graph to see final output");
    lines = []
    for i in range(0,10):
        pts,ptsG = generatePoints(1,d);
        lines.append(np.asarray(pts));
    projectionpts = plotProj(pointsG,lines,n,10,d,1); # Gaussian points
    mean,cov = meanVar(projectionpts,10);

    print("Open file Solution1.txt for solution");
                    
    filename = "Solution1.txt";
    target = open(filename,'w');
    target.write("The Following are the alpha values:\n");
    # Lists down all the bounds/alphas obtained.
    for i in range(0,d):
            target.write(str(alpha[i]));
            target.write("\n");

    target.write("\n");

    for i in range(0,10):
         target.write("Mean of projection for " + str(i+1));
         target.write("\n");
         target.write(str(mean[i]));
         target.write("\n");
         target.write("Covariance Matrix for " + str(i+1));
         target.write("\n");
         target.write(str(cov[i]));
         target.write("\n");
         target.write("\n");

    target.close();

    print("For subspace of dimension 5 we observe the following");
    print("10 graphs will be opened. Please check and close each graph to see final output");
    # Randomly generated 5 dimensional subspace
    subspace = []
    for i in range(0,10):
        pts,ptsG = generatePoints(5,d);
        subspace.append(np.asarray(pts));
    projectionpts = plotProj(pointsG,subspace,n,10,d,5); # Gaussian Points
    mean,cov = meanVar(projectionpts,10);

    print("Open file Solution3.txt for solution");

    filename = "Solution3.txt"
    target = open(filename,'w');
    for i in range(0,10):
         target.write("Mean of projection for " + str(i+1));
         target.write("\n");
         target.write(str(mean[i]));
         target.write("\n");
         target.write("Covariance Matrix for " + str(i+1));
         target.write("\n");
         target.write(str(cov[i]));
         target.write("\n");
         target.write("\n");

    target.close();

if __name__ == "__main__":
    main();
