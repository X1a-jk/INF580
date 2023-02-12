#!/usr/bin/env python3

## use a DDP formulation to solve the DGP,
## then use PCA to project to K dimensions
## then use a local NLP solver to improve solution
## (this version uses the amplpy interface in order to solve DDP)

import sys
import os.path
from amplpy import AMPL
import time
import math
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

######### CONFIGURABLE PARAMETERS ############

myZero = 1e-8
LPsolver = "cplex"
NLPsolver = "ipopt"
#projmethod = "Barvinok"
projmethod = "PCA"
showplot = True

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
                                    print("readDat: WARNING: interval weight[", e[2], ",", e[3], "] empty, setting to", e[2])
                                    e[3] = e[2]
                            else:
                                print("readDat: ERROR: line", linecount, "has < 4 columns")
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
def writeRlz(n,K, rlzfn):
    rlz = open(rlzfn, "w")
    print("# realization for " + rlzbase, file=rlz)
    print("param xbar :=", file=rlz)
    for i in range(n):
        for k in range(K):
            print(" " + str(i+1) + " " + str(k+1) + "  " + str(x[i,k]), file=rlz)
    print(rlz, ";", file=rlz)
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
    if isinstance(K,str):
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
    
# Barvinok's naive algorithm
def Barvinok(B, K):
    n = B.shape[0]
    X = factor(B)
    y = (1/math.sqrt(K))*np.random.multivariate_normal(np.zeros(n*K), np.identity(n*K))
    y = np.reshape(y, (K, n))
    x = np.transpose(np.dot(y,X.T))
    return x

################### MAIN #####################

t0 = time.time()

## read command line
if len(sys.argv) < 2:
    exit('cmdline must be: filename.dat [noplot]')

# read instance
(Kdim, n, E) = readDat(sys.argv[1])

# see if we need to plot
if len(sys.argv) >= 3:
    if sys.argv[2] == "noplot":
        showplot = False

## construct weighted vertex neighbourhoods from edges
G = {i:dict() for i in range(n)}
for e in E:
    i = e[0]-1 # first vertex
    j = e[1]-1 # second vertex
    w = e[2] # edge weight
    if i > j:
        t = i
        i = j
        j = t
    G[i][j] = w 

## formulate and solve the dual DDP
ddp = AMPL()
ddp.read("dgp_ddp.mod")
ddp.readData(sys.argv[1])
ddp.setOption('solver', LPsolver)
ddp.solve()
objfun = ddp.getObjective('push')
objfunval = objfun.value()
print("optimal obj. fun. value =", objfunval)
Xvar = ddp.getVariable('X')
X = np.zeros((n,n))
for i in range(n):
    for j in range(n):
        X[i,j] = Xvar[i+1,j+1].value()

## retrieve realization in K dimensions
print("ambient dimension n =", n)
Y = MDS(X)
K = Y.shape[1]
print("found relaxed embedding in natural dimension K =", K)
if K not in {2,3}:
    if K < 2:
        K = 2
    elif K > 3:
        K = 3
print("now projecting to", K, "principal dimensions")
if projmethod == "PCA":
    xbar = PCA(X, K)
elif projmethod == "Barvinok":
    xbar = Barvinok(X, K)

## report dualDDP solution statistics
mderr1 = mde(xbar, G)
print("DDP mean distance error =", mderr1)
lderr1 = lde(xbar, G)
print("DDP largest distance error =", lderr1)
t1 = time.time()
cputime1 = t1-t0
print("DDP cpu time =", cputime1)

## refine solution with a local NLP solver
nlp = AMPL()
nlp.read("dgp.mod")
nlp.readData(sys.argv[1])
nlp.setOption('solver', NLPsolver)
xvar = nlp.getVariable('x')
for i in range(n):
    for k in range(K):
        xvar[i+1,k+1].setValue(xbar[i,k])
nlp.solve()
xvar = nlp.getVariable('x')
xval = xvar.getValues()
x = np.zeros((n,K))
for i in range(n):
    for k in range(K):
        x[i,k] = xvar[i+1,k+1].value()

# save solution to a file
rlzbase = '.'.join(os.path.basename(sys.argv[1]).split('.')[0:-1])
writeRlz(n,K, rlzbase + "-sol.dat")

# report NLP solution statistics
mderr2 = mde(x, G)
print("NLP mean distance error =", mderr2)
lderr2 = lde(x, G)
print("NLP largest distance error =", lderr2)
t2 = time.time()
cputime2 = t2-t1
print("NLP cpu time =", cputime2)

# report total statistics
cputime = t2 - t0
print("total cpu time=", cputime)
print("OUTLABELS:mp,projmethod,objX,mdeX,ldeX,cpuX,mdex,ldex,cpux,cputot")
print("OUT:ddp,{0:s},{1:.3f},{2:.3f},{3:.3f},{4:.2f},{5:.3f},{6:.3f},{7:.2f},{8:.2f}".format(projmethod,objfunval, mderr1, lderr1, cputime1, mderr2, lderr2, cputime2, cputime))

## plot results
if showplot:
    if K == 2:
        plt.scatter(x[:,0], x[:,1])
        plt.plot(x[:,0], x[:,1])
    elif K == 3:
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.scatter(x[:,0], x[:,1], x[:,2])
        ax.plot(x[:,0], x[:,1], x[:,2])
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')    
    plt.show()

####################### OBLIVION ############################

# ## choice of SDP solvers with CVXPY
# print(cp.installed_solvers())
# prob.solve(solver=cp.CVXOPT)
# prob.solve(solver=cp.SCS)
# prob.solve(solver=cp.MOSEK)

