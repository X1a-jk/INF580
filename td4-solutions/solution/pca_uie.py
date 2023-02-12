#!/usr/bin/env python3

## perform PCA on a square symmetric matrix 
##   representing an embedding in n dimensions
##   of a graph with n vertices -- read .uie
##   files produced with univ_isom_emb.run

import sys
import numpy as np
import math
import types
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

myZero = 1e-9

## return the distance matrix of a realization
def distanceMatrix(x, p=2):
    n = len(x[:,0])
    D = np.zeros((n,n))
    for u in range(n-1):
        for v in range(u+1,n):
            D[u,v] = np.linalg.norm(np.subtract(x[u,:],x[v,:]), ord=p)
            D[v,u] = D[u,v]
    return D

## convert a distance matrix to a Gram matrix
def dist2Gram(D):
    n = D.shape[0]
    J = np.identity(n) - (1.0/n)*np.ones((n,n))
    G = -0.5 * np.dot(J,np.dot(np.square(D), J))
    return G

## factor a square matrix
def factor(A):
    n = A.shape[0]
    (evals,evecs) = np.linalg.eigh(A)
    evals[evals < 0] = 0  # closest SDP matrix
    X = evecs #np.transpose(evecs)
    sqrootdiag = np.eye(n)
    for i in range(n):
        sqrootdiag[i,i] = math.sqrt(evals[i])
    X = X.dot(sqrootdiag)
    return np.fliplr(X)

## classic Multidimensional scaling
def MDS(B, eps = myZero):
    n = B.shape[0]
    x = factor(B)
    (evals,evecs) = np.linalg.eigh(x)
    K = len(evals[evals > eps])
    if K < n:
        # only first K columns
        x = x[:,0:K]
    return x

## principal component analysis
def PCA(B, K = "None"):
    x = factor(B)
    n = B.shape[0]
    if isinstance(K, str):
        K = n
    if K < n:
        # only first K columns
        x = x[:,0:K]
    return x

## main

if len(sys.argv) < 2:
    exit('need .uie file in input')

# read input file
lines = [line.rstrip('\n').split()[2:] for line in open(sys.argv[1]) if line[0] == 'x']
n = len(lines)

# turn into float array
X = np.array([[float(lines[i][j]) for j in range(n)] for i in range(n)])

# make distance matrix
#D = distanceMatrix(X) # Euclidean distance
D = X # if using UIE, realization = DM
# derive Gram matrix
G = dist2Gram(D)

x = MDS(G)
n = x.shape[0]
K = x.shape[1]
print("dimension can be reduced from", n, "to", K)

# PCA
if K > 3:
    K = 3
elif K < 2:
    K = 2
print("representing in", K, "dimensions")

x = PCA(G,K)
    
if K == 2:
    plt.scatter(x[:,0], x[:,1])
elif K == 3:
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x[:,0], x[:,1], x[:,2])
    ax.plot(x[:,0], x[:,1], x[:,2])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    
plt.show()
