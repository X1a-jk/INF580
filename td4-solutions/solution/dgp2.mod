# DGP formulation 2 (reformulate dgp1 using slacks)
				 
## the protein graph format
param Kdim integer, > 0;
param n integer, > 0;
set V := 1..n;
set E within {V,V};
param c{E};
param I{E};

# set of dimensions
set K := 1..Kdim;

## decision variables
# positions of vertices (k-th component of position of vertex v)
var x{V,K};

# slack/surplus variable
var s{E};

minimize slack: sum{(u,v) in E} s[u,v]^2;

subject to dgp{(u,v)in E}: sum{k in K} (x[u,k] - x[v,k])^2 = c[u,v]^2 + s[u,v];
