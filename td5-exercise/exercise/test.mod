# test.mod
param n integer, > 1;
param m integer, > 1;
set N := 1..n;
set M := 1..m;
param c{N};
param A{M,N};
param b{M};
var x{N} >= 0;
minimize objfun: sum{j in N} c[j]*x[j];
subject to lincon{i in M}: sum{j in N} A[i,j]*x[j] = b[i];

