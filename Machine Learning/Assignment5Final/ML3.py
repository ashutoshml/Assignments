import numpy as np
import random

def generatePoint(n,d,mean):
    covMat = np.eye(d);
    points = []
    for i in range(0,n):
        point = np.random.multivariate_normal(mean,covMat);
        points.append(point);
    return points;

def generateCenters(n,d):
    mean = np.zeros(d);
    covMat = np.multiply(3,np.eye(d));
    centers = []
    centers.append(np.random.multivariate_normal(mean,covMat));
    m = 0;
    while len(centers)<10:
        nk = np.random.multivariate_normal(mean,covMat);
        m = 0;
        for j in range(0,len(centers)):
            if(np.linalg.norm(nk-centers[j]) <=5 or np.linalg.norm(nk-centers[j])>=10):
                m = 1;
        if m != 1:
            centers.append(nk);
    return centers;
               
def SVD(mat):
    U,s,V = np.linalg.svd(mat,full_matrices=True);
    return U,s,V;

def centerCheck(point,subspace):
    subspace = np.asarray(subspace);
    inver = np.linalg.inv(np.dot(subspace.T,subspace));
    proj = np.dot(subspace,np.dot(inver,np.dot(subspace.T,point)));
    if(abs(np.linalg.norm(point-proj)) < 1):
        print "The center lies within acceptable limits of distance from subspace ie 1 | Distance : " + str(np.linalg.norm(point-proj));
    else:
        print "The center exceeds the acceptable limit of distance from subspace + Distance" + str(np.linalg.norm(point-proj));

def projectionPoint(point,subspace):
    subspace = np.asarray(subspace);
    inver = np.linalg.inv(np.dot(subspace.T,subspace));
    proj = np.dot(subspace,np.dot(inver,np.dot(subspace.T,point)));
    return proj;

def projectPoints(points,subspace):
    projPoints = []
    for i in range(0,len(points)):
        projPoints.append(projectionPoint(points[i],subspace));
    return projPoints;

# Applying kmeans clustering as a natural choice (k nearest neighbours being a classification algorithms)
def kMeansCluster(points,centers,oldcenters,k):
    clusters = []
    clusternum = []
    for i in range(0,k):
        clusters.append([]);
        clusternum.append([]);
    for i in range(0,len(points)):
        minim = 1000000000;
        cl = 0;
        for j in range(0,k):
            if(abs(np.linalg.norm(centers[j]-points[i]))<minim):
                minim = abs(np.linalg.norm(centers[j]-points[i]));
                cl = j;
        clusters[cl].append(points[i])
        clusternum[cl].append(i);
       
    newCenters = [];
    for i in range(0,k):
        c = np.zeros(len(centers[i]));
        for j in range(0,len(clusters[i])):
            c = np.add(c,clusters[i][j]);
        c = c/len(clusters[i]);
        newCenters.append(c);
    if(np.allclose(centers,oldcenters,rtol = 1e-18,atol=1e-18)):
        return centers, clusternum;
    return kMeansCluster(points,newCenters,centers,k);
    
def initCenter(points,k):
    randomIndex = random.sample(range(len(points)),k);
    centers = []
    for i in range(0,len(randomIndex)):
        centers.append(points[randomIndex[i]]);
    return centers;

def clusterPointsorig(points,clusters):
    clusterorig = []
    for i in range(0,len(clusters)):
        clusterorig.append([]);
    for i in range(0,len(clusters)):
        for j in range(0,len(clusters[i])):
            clusterorig[i].append(points[clusters[i][j]]);
    return clusterorig;

def meanVar(points,d):
    mean = []
    for i in range(0,d):
        meani = np.mean(points[i],axis = 0);
        mean.append(meani);
        cov = np.cov(points[i],rowvar = 0);
        return mean,cov;

nCenters = 10;
d = 25;
nPoints = 50;
centerstr = generateCenters(nCenters,d);
points = [];

for i in range(0,nCenters):
    points = points + generatePoint(nPoints,d,centerstr[i]);
points = np.asarray(points);

U,s,V = SVD(points);

V =  V[:10,:];
s = s[:10];
S = np.zeros((U.shape[1],V.shape[0]));
S[:10,:10] = np.diag(s);
U = U[:10,:];

# 10 Dimensional subspace generated
subspace10d = np.dot(U,np.dot(S,V));

subspace10d = subspace10d.T;
for i in range(0,10):
    centerCheck(centerstr[i],subspace10d);

projPoints = projectPoints(points,subspace10d);
nc = 10;
centers = []
for i in range(0,nc):
    centers.append(initCenter(projPoints,nc));

print("Please wait while the kmean centers are being generated:");

kmeanCenter,clusters = kMeansCluster(projPoints,centers[i],np.add(centers[i],10000),nc);
#for i in range(0,len(kmeanCenter)):
#    print kmeanCenter[i];

#for i in range(0,len(clusters)):
#    print clusters[i];

clusterorig = clusterPointsorig(points,clusters);

meancl = []
covarcl = []

for i in range(0,len(clusterorig)):
    mean,cov = meanVar([clusterorig[i]],d);
    meancl.append(mean);
    covarcl.append(cov);

print("Open file Solution3.txt for solution");
filename = "Solution3.txt";
target = open(filename,'w');
target.write("Note that original covariance matrix is an identity for each gaussian\n");
target.write("Original means are:\n")
for i in range(0,len(centerstr)):
    target.write(str(i+1) +" : "+ str(centerstr[i]) + "\n");

target.write("\n");
target.write("\n");
target.write("\n");

target.write("Note that the order of mean may change\n");
for i in range(0,len(covarcl)):
    target.write("Mean for " + str(i+1) +" cluster :\n");
    target.write(str(meancl[i]) + "\n");
    target.write("Covariance matrix for " + str(i+1) + " cluster :\n ");
    target.write(str(covarcl[i]) + "\n");
    target.write("\n");
    target.write("\n");
    target.write("\n");

target.close();
