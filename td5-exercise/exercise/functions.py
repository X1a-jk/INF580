import sys
import os.path
from amplpy import AMPL
import time
import math
import types
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

######### CONFIGURABLE PARAMETERS ############

myZero = 1e-8
LPsolver = "cplex"
NLPsolver = "ipopt"

################ FUNCTIONS ###################

## read data file written in AMPL .dat format
## (after line "param : E", list of edges formatted as i j w_{ij} I_{ij})
def readDat(filename):
    edgeflag = False # true while reading edges
    Kdim = 3
    n = 0
    E = list()
    with open(filename) as f:
        for line in f:
            # look at file line by line
            line = line.strip()
            if len(line) > 0:       
                if line[0] != '#':
                    # line non-empty and non-comment
                    if edgeflag:
                        if line[0] == ';':
                            # if only a ';' then we're closing the edge section
                            edgeflag = False
                        else:
                            # reading uncommented edge data
                            cols = [c for c in line.split() if not '#' in c]
                            if len(cols) >= 6:
                                e = (int(cols[0]), int(cols[1]), float(cols[4]), float(cols[5]))
                            elif len(cols) >= 4:
                                e = (int(cols[0]), int(cols[1]), float(cols[2]), float(cols[2]))
                                if e[2] > e[3]:
                                    print("readDat: WARNING: interval weight[", e[2], ",", e[3], "] empty, setting to"+str(e[2]))
                                    e[3] = e[2]
                            else:
                                print("readDat: ERROR: line"+str(linecount)+"has < 4 columns")
                                exit('abort')
                            E.append(e)
                    else:
                        if line.replace(" ","")[0:7] == 'param:E':
                            # we're in the edge section now
                            edgeflag = True
                        elif line.replace(" ","")[0:9] == 'paramKdim':
                            # parse line defining Kdim
                            Kdimstr = line.split()[3]
                            if Kdimstr[-1] == ';':
                                Kdimstr = Kdimstr[0:-1]
                            Kdim = int(Kdimstr)
                        elif line.replace(" ","")[0:6] == 'paramn':
                            # parse line defining n
                            nstr = line.split()[3]
                            if nstr[-1] == ';':
                                nstr = nstr[0:-1]
                            n = int(nstr)
    return (Kdim, n, E)

## write realization file to a _rlz.dat file
def writeRlz(x,n,K, rlzfn):
    rlz = open(rlzfn, "w")
    print("# realization for " + str(rlzfn),rlz)
    print("param xbar :=",rlz)
    for i in range(n):
        for k in range(K):
            print(" " + str(i+1) + " " + str(k+1) + "  " + str(x[i,k]),rlz)
    print(";",rlz)
    rlz.close()
    return

# factor a square matrix, neglecting negative eigenspace
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

# multidimensional scaling
def MDS(B, eps = myZero):
    n = B.shape[0]
    x = factor(B)
    (evals,evecs) = np.linalg.eigh(B) # ascertain n. large eigs of B
    K = len(evals[evals > eps])
    if K < n:
        # only first K columns
        x = x[:,0:K]
    return x

# principal component analysis
def PCA(B, K = "None"):
    x = factor(B)
    n = B.shape[0]
    if isinstance(K, str):
        K = n
    if K < n:
        # only first K columns
        x = x[:,0:K]
    return x

# mean distance error
def mde(x, G):
    n,K = x.shape
    m = sum(len(G[i]) for i in range(n))
    ret = sum(abs(np.linalg.norm(np.subtract(x[i],x[j])) - G[i][j]) for i in range(n) for j in G[i])
    ret = ret / float(m)
    return ret

# largest distance error
def lde(x, G):
    n,K = x.shape
    m = sum(len(G[i]) for i in range(n))
    ret = max(abs(np.linalg.norm(np.subtract(x[i],x[j])) - G[i][j]) for i in range(n) for j in G[i])
    return ret
    
