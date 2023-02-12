# DDP formulation for DGP
				 
## the protein graph format
param Kdim integer, > 0;
param n integer, > 0;
set V := 1..n;
set E within {V,V};
param c{E};
param I{E};

# set of dimensions
set K := 1..Kdim;

# decision variables

var X{V,V};
var T{V,V};

minimize push: sum{(i,j) in E} (X[i,i] + X[j,j] - 2*X[i,j]);

subject to pull{(i,j) in E}: X[i,i] + X[j,j] - 2*X[i,j] >= c[i,j]^2;

subject to diagdom{i in V}: sum{j in V : j!=i} T[i,j] <= X[i,i];

subject to sandwich1{i in V, j in V} : -T[i,j] <= X[i,j];
subject to sandwich2{i in V, j in V} : X[i,j] <= T[i,j];

subject to symmetric{i in V, j in V : i < j} : X[i,j] == X[j,i];
subject to symmetricT{i in V, j in V : i < j} : T[i,j] == T[j,i];

