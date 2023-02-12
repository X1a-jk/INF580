# DGP formulation (unconstrained penalties)
				 
## the protein graph format
param Kdim integer, > 0;
param n integer, > 0;
set V := 1..n;
set E within {V,V};
param c{E};
param I{E};

# set of dimensions
set K := 1..Kdim;

# starting point
param xbar{V,K} default 0;

## decision variables
# positions of vertices (k-th component of position of vertex v)
var x{V,K};

minimize dgp: sum{(u,v) in E} ((sum{k in K} (x[u,k] - x[v,k])^2) - c[u,v]^2)^2;

#subject to centroid{k in K}: sum{v in V} x[v,k] = 0;
