#!/usr/bin/env python3
# test.py

from amplpy import AMPL
import numpy as np
lp = AMPL()
lp.read("test.mod")
lp.readData("test.dat")
lp.setOption("solver", "cplex")
lp.solve()
ndata = lp.getData("n")
n = int(ndata.getRowByIndex(0)[0])
solveres = lp.getData("solve_result")
solve_result = solveres.getRowByIndex(0)[0]
objfun = lp.getObjective("objfun")
objfunval = objfun.value()
xvar = lp.getVariable("x")
x = np.zeros(n)
for j in range(n):
    x[j] = xvar[j+1].value()
print("solution norm is", np.linalg.norm(x))
print("optimal objective function value is", objfunval)
print("solver status is", solve_result)

