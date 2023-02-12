# diet.mod - formulation for the diet problem

param n integer > 0;
param m integer > 0;
set N := 1..n;
set M := 1..m;
param c{N} default 0;
param A{M,N} default 0;
param b{M} default 0;

var x{N} >= 0;

minimize cost: sum{j in N} c[j]*x[j];

subject to nutrients{i in M}: sum{j in N} A[i,j]*x[j] = b[i];
