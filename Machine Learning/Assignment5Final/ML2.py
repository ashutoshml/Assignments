import numpy as np
import matplotlib.pyplot as plt
import Image

# load the images
def loadImage(image):
    im = Image.open(image).convert('L');
    mat = np.asarray(im);
    matf = []
    for i in range(0,len(mat)):
        matf = matf + list(mat[i]);
    return matf;

# Perform SVD of matrix
def svdImage(mat):
    U,s,V = np.linalg.svd(mat,full_matrices=True);
    matDim = mat.shape;
    dim = (s.shape)[0];
    S = np.zeros((matDim),dtype=np.int)
    S[:dim,:dim] = np.diag(s);
    return U,S,V,s

def loadPics(fold,numImages):
    picMat = []
    for i in range(1,numImages+1):
        picMat.append(loadImage(fold + str(i) + '.thumbnail'));
    picMata = np.asarray(picMat);
    picMata = picMata.T;
    return picMata;

def takeRowsUSV(U,s,V,rows):
    Unew = U[:,:rows];
    Vnew = V[:rows,:];
    snew = s[:rows];
    Snew = np.zeros((rows,rows));
    Snew[:rows,:rows] = np.diag(snew);
    return Unew,Snew,Vnew;

def projectionPoint(point,subspace):
    subspace = np.asarray(subspace);
    inver = np.linalg.inv(np.dot(subspace.T,subspace));
    proj = np.dot(subspace,np.dot(inver,np.dot(subspace.T,point)));
    return proj;

def dotPr(U,S,V):
    newMat = np.dot(U,np.dot(S,V));
    return newMat;

def normComp(picMat,projPoint):
    minim = 10000000;
    for i in range(0,len(picMat)):
        if(abs(np.linalg.norm(picMat[i] - projPoint))<minim):
            minim = abs(np.linalg.norm(picMat[i] - projPoint));
    return minim;

numImages = 50; #Specify number of photos in the training set
fold = "ML2Images/Training_Set/"; # Specify name of the folder containing training set
picMat = loadPics(fold,numImages)

print("Please wait while the SVD runs..");
U,S,V,s = svdImage(picMat);

eigenFace = [1,2,5,10,15,20,25];
Uef = []
compMat = []
for i in range(0,len(eigenFace)):
    Ue,Se,Ve = takeRowsUSV(U,s,V,eigenFace[i]);
    Uef.append(Ue);
    compMat.append(dotPr(Ue,Se,Ve));

fold = "ML2Images/Test_Set/"; # Specify the name of folder containing test set
numTest = 10; # Specify the number of photos in the test set
testImg = []
for i in range(1,numTest+1):
    testImg.append(loadImage(fold + str(i) + ".thumbnail"));

projPoints = []
for k in range(0,len(eigenFace)):
    projPoint = []
    for i in range(0,numTest):
        projPoint.append(projectionPoint(testImg[i],Uef[k]));
    projPoints.append(projPoint);

print("Open file Solution2.txt for solution");
filename = "Solution2.txt";
target = open(filename,'w');
sumb = 0;
sumd = 0;
# Test Data
target.write("The following is the result on the test data\n");
for k in range(0,len(eigenFace)):
    target.write("For eigenfaces " + str(eigenFace[k]) + " :\n");
    sumb = 0;
    sumd = 0;
    for i in range(0,numTest):
        minnorm = normComp(compMat[k].T,projPoints[k][i]);
        if(minnorm < 10):
            target.write("Image " + str(i+1) + " has the distance:" + str(minnorm) + " and thus belongs to the database\n");
            sumb = sumb + 1;
        else: 
            target.write("Image " + str(i+1) + " has the distance:" + str(minnorm) + " and thus does not belong to the database\n");
            sumd = sumd + 1;
    target.write("Belongs: " + str(sumb) + " || Does Not Belong: " + str(sumd)+ "\n");
    target.write("\n");
target.close();
