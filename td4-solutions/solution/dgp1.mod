# DGP formulation 1 (feasibility-only)

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

subject to dgp{(u,v)in E}: sum{k in K} (x[u,k] - x[v,k])^2 = c[u,v]^2;




