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

# Function to plot point on the graph
def plotPoints(points,n, d):
    plt.figure();
    v = [x for x in range(1,n+1)];
    h = [];
    for i in range(0,d):
        h = [points[x][i] for x in range(0,n)];
        plt.plot(v,h,'ro');
        h = [];
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
		dist = [np.linalg.norm(projLine[i][j]) if np.dot(projLine[i][j],lines[i][0]) >=0 else -1*np.linalg.norm(projLine[i][j]) for j in range(0,n)];
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
    
n = 200;
d = 50;
points = generatePoints(n,d);

plotPoints(points,n,d);
alpha = findAlpha(points,n,d);
print("For subspace of dimension 1 we observe the following");
print("10 graphs will be opened. Please check and close each graph to see final output");
lines = []
for i in range(0,10):
    lines.append(np.asarray(generatePoints(1,d)));
projectionpts = plotProj(points,lines,n,10,d,1);
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
    subspace.append(np.asarray(generatePoints(5,d)));
projectionpts = plotProj(points,subspace,n,10,d,5);
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
