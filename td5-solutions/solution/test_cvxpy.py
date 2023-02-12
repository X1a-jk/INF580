#!/usr/bin/env python3
import sys
import cvxpy as cp
import math
import time
import numpy as np
n = 5
X = cp.Variable((n,n), PSD=True)
A = np.random.rand(n,n)
objfun = cp.trace(A.T*X)
constr1 = [X[i,i+1] + X[i,i+2] <= -1 for i in range(n-2)]
constr2 = [cp.diag(X) == 1]
objective = cp.Minimize(objfun)
constraints = constr1 + constr2
prob = cp.Problem(objective, constraints)
prob.solve(cp.SCS, verbose=True)
Xv = X.value
print(Xv)
