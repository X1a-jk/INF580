#!/usr/bin/env python3

## test the JLL on random data

import sys
import math
import numpy as np
from blis.py import einsum, gemv, gemm
from scipy import sparse
from scipy.spatial.distance import pdist
from math import sqrt

myZero = 1e-10
RPtype = "dense"
#RPtype = "sparse"
#RPtype = "achlioptas"
invRPdens = 100

#################### FUNCTIONS #####################

# generate a componentwise Normal(0,1) matrix
def normalmatrix(m, n):
    return np.random.normal([0],[[1]],(m,n))

# generate a componentwise Uniform(0,1) matrix
def uniformmatrix(m, n):
    return np.random.rand(m,n)

# generate a componentwise Normal(0,1) matrix with inverse density s
def sparsenormalmatrix(m,n,s):
    p = 1.0/float(s)
    A = np.zeros((m,n))
    for i in range(m):
        for j in range(n):
            if np.random.uniform(0,1) <= p:
                A[i,j] = np.random.randn()
    return A

### generate a sample from an Achlioptas distribution
def achlioptas_sample(s=3):
    ret = 0
    p = 1.0/float(s)
    uniformsample = np.random.uniform(0,1)
    if uniformsample < p/2:
        ret = -1
    elif uniformsample > 1-p/2:
        ret = 1
    else:
        ret = 0
    return ret
    
### generate an Achlioptas m x n random projection matrix
def achlioptas(m, n, s=3):
    A = np.zeros((m,n))
    for i in range(m):
        for j in range(n):
            aij = achlioptas_sample(s)
            if aij != 0:
                A[i,j] = aij
    return A

####################### MAIN #######################

## read command line
if len(sys.argv) < 4:
    print("syntax: " + sys.argv[0] + " m n distr")
    print("  where m=|dimensions|, n=|points|")
    print("  distr in {U,N}")
    print("    U is Uniform(0,1), N is Normal(0,1)")
    sys.exit(1)

m = int(sys.argv[1])
n = int(sys.argv[2])
distr = sys.argv[3]

invRPdens = sqrt(m)

## generate random data matrix
if distr == "U":
    X = uniformmatrix(m,n)
elif distr == "N":
    X = normalmatrix(m,n)
else:
    sys.exit("error: distr must be either \"U\" or \"N\"")

## compute distance matrix
D = pdist(X.T)
nD = len(D)

## test epsilon and universal constant
print("m\tn\teps\tC\tk\tjllerr\tavgjll\tmaxjll\tmde\tlde")
for eps in [0.05, 0.1, 0.15, 0.2]:
    print(" --------------------------")
    for C in [0.5, 1.0, 1.5, 2.0]:
        k = int(round(C*(1/eps**2)*math.log(n)))
        if RPtype == "dense":
            T = normalmatrix(k,m)
        elif RPtype == "sparse":
            T = sparsenormalmatrix(k,m, invRPdens)
        elif RPtype == "achlioptas":
            T = achlioptas(k,m, invRPdens)
        try:
            TX = gemm(T,X)
        except:
            TX = np.dot(T,X)
        TX = (1/sqrt(k))*TX
        if RPtype == "sparse" or RPtype == "achlioptas":
            TX = (sqrt(invRPdens))*TX
        TD = pdist(TX.T)
        jllerr = [max(0, abs(TD[i]/D[i]-1)-eps) for i in range(nD)]
        jllerr = [jle for jle in jllerr if jle > myZero]
        jllerr = len(jllerr)
        avgjllerr = sum(abs(TD[i]/D[i]-1) for i in range(nD)) / nD
        maxjllerr = max(abs(TD[i]/D[i]-1) for i in range(nD))
        mde = sum(abs(D[i] - TD[i]) for i in range(nD)) / nD
        lde = max(abs(D[i] - TD[i]) for i in range(nD))
        avgjllerr = round(avgjllerr, 3)
        maxjllerr = round(maxjllerr, 3)
        mde = round(mde, 3)
        lde = round(lde, 3)
        print(str(m) + "\t" + str(n) + "\t" + str(eps) + "\t" + str(C) + "\t" + str(k) + "\t" + str(jllerr) + "\t" + str(avgjllerr) + "\t" + str(maxjllerr) + "\t" + str(mde) + "\t" + str(lde))
