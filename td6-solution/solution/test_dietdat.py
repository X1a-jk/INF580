#!/usr/bin/env python

import sys
import os
import math
import numpy as np
import scipy
from blis.py import einsum, gemv, gemm
from math import sqrt
#from scipy.sparse import dok_matrix
from amplpy import AMPL
import time

## read diet problem data file written in AMPL .dat format
def readDat(filename):
    readparam = "[None]"
    m = 0
    n = 0
    c = {}
    xv = {}
    b = {}
    A = {}
    with open(filename) as f:
        for line in f:
            # look at file line by line
            line = line.strip()
            if len(line) == 0:
                continue
            if line[0] == '#':
                continue
            L = line.split()
            if L[0] == "param":
                readparam = L[1]
                if readparam == "m":
                    m = int(L[3][0:-1])
                elif readparam == "n":
                    n = int(L[3][0:-1])
                continue
            elif L[0] == ';':
                readparam = "[None]"
                continue
            elif readparam == "c":
                j = int(L[0])
                cj = float(L[1])
                c[j] = cj
            elif readparam == "xv":
                j = int(L[0])
                xvj = float(L[1])
                xv[j] = xvj
            elif readparam == "b":
                i = int(L[0])
                bi = float(L[1])
                b[i] = bi
            elif readparam == "A":
                i = int(L[0])
                j = int(L[1])
                Aij = float(L[2])
                A[(i,j)] = Aij
    return (m,n,A,b,c, xv)

(m,n,Ad,bd,cd,xvd) = readDat("projdiet.dat")

c = np.zeros(n)
b = np.zeros(m)
A = np.zeros((m,n))
xv = np.zeros(n)

for (i,j) in Ad:
    A[i-1,j-1] = Ad[(i,j)]

for j in cd:
    c[j-1] = cd[j]

for i in bd:
    b[i-1] = bd[i]

for j in xvd:
    xv[j-1] = xvd[j]

error = np.linalg.norm(np.subtract(np.dot(A,xv), b))
print error
