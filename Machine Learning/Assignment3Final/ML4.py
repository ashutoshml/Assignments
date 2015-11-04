import numpy as np
import scipy
import matplotlib.pyplot as plt
import random

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

def interPointDistance(points,n,d):
    distMat = []
    distance = 0;
    for i in range(0,n):
	disti = []
	for j in range(0,n):
	    distance = np.linalg.norm(list(np.asarray(points[i])-np.asarray(points[j])));
            disti.append(distance);
	distMat.append(disti);
    return distMat;

def projection(points,subspace,n):
    projPoint = []
    subspacet = np.asmatrix(subspace);
    subspace = subspacet.T;
    for i in range(0,n):
        inv = np.linalg.inv(np.dot(subspacet,subspace));
        proj = np.dot(np.dot(np.dot(subspace,inv),subspacet),points[i]);
        projPoint.append(proj);
    return projPoint;

def subspaceGen(n,d):
    subspace = [];
    subv = np.zeros(d);
    r = np.arange(0,d);
    k = list(random.sample(r,n));
    j = 0;
    for i in range(0,n):
        subv = np.zeros(d);
        subv[k[j]] = 1;
        j = j+1;
	subspace.append(subv);
    return subspace;

n = 50;
d = 200;
points50 = generatePoints(n,d);
distMat = interPointDistance(points50,n,d);

print("Please open file \"Solution4.txt\":");
filename = "Solution4.txt"
target = open(filename,'w');
target.write("The interpoint distance Matrix is as follows:\n");
for i in range(0,n):
    target.write(str(distMat[i]));
    target.write("\n");

target.write("\n");
target.write("\n");
target.write("\n");
subspaces1 = np.asmatrix(subspaceGen(1,d));
subspaces2 = np.asmatrix(subspaceGen(2,d));
subspaces3 = np.asmatrix(subspaceGen(3,d));
subspaces10 = np.asmatrix(subspaceGen(10,d));
subspaces50 = np.asmatrix(subspaceGen(50,d));

projPoint1 = projection(points50,subspaces1,n);
projPoint2 = projection(points50,subspaces2,n);
projPoint3 = projection(points50,subspaces3,n);
projPoint10 = projection(points50,subspaces10,n);
projPoint50 = projection(points50,subspaces50,n);

distMat1 = interPointDistance(projPoint1,n,d);
distMat2 = interPointDistance(projPoint2,n,d);
distMat3 = interPointDistance(projPoint3,n,d);
distMat10 = interPointDistance(projPoint10,n,d);
distMat50 = interPointDistance(projPoint50,n,d);

num = np.sqrt(1.0/200);
diff1 = list((num*np.asmatrix(distMat))-np.asmatrix(distMat1));
num = np.sqrt(2.0/200);
diff2 = list((num*np.asmatrix(distMat))-np.asmatrix(distMat2));
num = np.sqrt(3.0/200);
diff3 = list((num*np.asmatrix(distMat))-np.asmatrix(distMat3));
num = np.sqrt(10.0/200);
diff10 = list((num*np.asmatrix(distMat))-np.asmatrix(distMat10));
num = np.sqrt(50.0/200);
diff50 = list((num*np.asmatrix(distMat))-np.asmatrix(distMat50));

target.write("Difference matrix is as follows:\n");
target.write("For k = 1");
target.write("\n");
for i in range(0,n):
    target.write(str(diff1[i]));
    target.write("\n");
target.write("\n");
target.write("\n");
target.write("\n");
target.write("For k = 2");
target.write("\n");
for i in range(0,n):
    target.write(str(diff2[i]));
    target.write("\n");
target.write("\n");
target.write("\n");
target.write("\n");
target.write("For k = 3");
target.write("\n");
for i in range(0,n):
    target.write(str(diff3[i]));
    target.write("\n");
target.write("\n");
target.write("\n");
target.write("\n");
target.write("For k = 10");
target.write("\n");
for i in range(0,n):
    target.write(str(diff10[i]));
    target.write("\n");
target.write("\n");
target.write("\n");
target.write("\n");
target.write("For k = 50");
target.write("\n");
for i in range(0,n):
    target.write(str(diff50[i]));
    target.write("\n");

target.close();

