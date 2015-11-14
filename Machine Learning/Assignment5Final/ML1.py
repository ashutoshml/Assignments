import numpy as np
import Image
import scipy
import os

# RGB Images
def loadImage(image):
    im = Image.open(image);
    mat = np.asarray(im);
    imageMatR = [];
    imageMatG = [];
    imageMatB = [];
    for i in range(0,mat.shape[0]):
        arrayr = [];
        arrayg = [];
        arrayb = [];
        for j in range(0,mat.shape[1]):
            arrayr.append(mat[i][j][0]);
            arrayg.append(mat[i][j][1]);
            arrayb.append(mat[i][j][2]);
        imageMatR.append(arrayr);
        imageMatG.append(arrayg);
        imageMatB.append(arrayb);
    return np.asarray(imageMatR),np.asarray(imageMatG),np.asarray(imageMatB);

# Perform SVD of matrix
def svdImage(mat):
    U,s,V = np.linalg.svd(mat,full_matrices=True);
    matDim = mat.shape;
    dim = (s.shape)[0];
    S = np.zeros((matDim),dtype=np.int)
    S[:dim,:dim] = np.diag(s);
    return U,S,V,s

# Takes only certain percentage of S
def newUSV(U,S,V,s,perc):
    n = int(round(perc*s.shape[0]));
    Unew = U[:,0:n];
    Snew = np.zeros((n,n),dtype=np.int);
    news = s[0:n]
    Snew[:n,:n] = np.diag(news);
    Vnew = V[0:n,:]
    return Unew,Snew,Vnew;

# Calculate dot Products
def dotPr(U,S,V):
    newMat = np.dot(U,np.dot(S,V));
    newMat = np.around(newMat);
    newMat = np.uint8(newMat);
    return newMat;

# Reconstructs images based on R G B
def reconstImage(R,G,B,num):
    imageMat = [];
    for i in range(0,R.shape[0]):
        imrow = [];
        for j in range(0,R.shape[1]):
            imrow.append((R[i][j],G[i][j],B[i][j]));
        imageMat.append(imrow);
    directory = 'ML1images';
    if not os.path.exists(directory):
            os.makedirs(directory)
    name = 'ML1images/'+num +'.jpeg';
    img = Image.fromarray(np.asarray(imageMat));
    img.save(name)
    return imageMat;

# Finds frobenius norm
def frobNorm(mat):
    return np.linalg.norm(mat);
    
print("Choose which Image to perform SVD on: ");
print("1. cartoon.jpg - Small Image");
print("2. scenery.jpg - Large Image");
n = input("Enter your Choice:");
if n == 1:
	img = "cartoon.jpg";
else:
	img = "scenery.jpg";

imageMatR,imageMatG,imageMatB = loadImage(img);

# SVD for R G B
Ur,Sr,Vr,sr = svdImage(imageMatR);
Ug,Sg,Vg,sg = svdImage(imageMatG);
Ub,Sb,Vb,sb = svdImage(imageMatB);

# Image matrix for 10 percent 
U10r,S10r,V10r = newUSV(Ur,Sr,Vr,sr,0.1);
U10g,S10g,V10g = newUSV(Ug,Sg,Vg,sg,0.1);
U10b,S10b,V10b = newUSV(Ub,Sb,Vb,sb,0.1);
imageMat10R = dotPr(U10r,S10r,V10r);
imageMat10G = dotPr(U10g,S10g,V10g);
imageMat10B = dotPr(U10b,S10b,V10b);

# Image matrix for 25 percent
U25r,S25r,V25r = newUSV(Ur,Sr,Vr,sr,0.25);
U25g,S25g,V25g = newUSV(Ug,Sg,Vg,sg,0.25);
U25b,S25b,V25b = newUSV(Ub,Sb,Vb,sb,0.25);
imageMat25R = dotPr(U25r,S25r,V25r);
imageMat25G = dotPr(U25g,S25g,V25g);
imageMat25B = dotPr(U25b,S25b,V25b);

# Image matrix for 50 percent
U50r,S50r,V50r = newUSV(Ur,Sr,Vr,sr,0.50);
U50g,S50g,V50g = newUSV(Ug,Sg,Vg,sg,0.50);
U50b,S50b,V50b = newUSV(Ub,Sb,Vb,sb,0.50);
imageMat50R = dotPr(U50r,S50r,V50r);
imageMat50G = dotPr(U50g,S50g,V50g);
imageMat50B = dotPr(U50b,S50b,V50b);


# For 10percent
imagemat10 = reconstImage(imageMat10R,imageMat10G,imageMat10B,'10Percent');
# For 25percent
imagemat25 = reconstImage(imageMat25R,imageMat25G,imageMat25B,'25Percent');
# For 50percent
imagemat50 = reconstImage(imageMat50R,imageMat50G,imageMat50B,'50Percent');

print("Please open folder ML1images to see reconstructed images");
print("Frobenius norm of RGB of original image: (" + str(frobNorm(imageMatR)) + "," + str(frobNorm(imageMatG)) + ","+ str(frobNorm(imageMatB)) +")");
print("Frobenius norm of RGB of 10 percent image: (" + str(frobNorm(imageMat10R)) + "," + str(frobNorm(imageMat10G)) + ","+ str(frobNorm(imageMat10B)) +")");
print("Frobenius norm of RGB of 25 percent image: (" + str(frobNorm(imageMat25R)) + "," + str(frobNorm(imageMat25G)) + ","+ str(frobNorm(imageMat25B)) +")");
print("Frobenius norm of RGB of 50 percent image: (" + str(frobNorm(imageMat50R)) + "," + str(frobNorm(imageMat50G)) + ","+ str(frobNorm(imageMat50B)) +")");


