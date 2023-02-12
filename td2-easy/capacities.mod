# capacities.mod

# index sets
param n integer, >0;
param Lmax integer, >0;
set F := 1..n;
set L := 1..Lmax;

# parameters
param c{F} >= 0;    # capacity needed for flow
param k{L} >= 0;    # capacity of link
param p{L} >= 0;    # unit cost of routing on link

# decision variables
var x{L,F} binary;  #

# objective
minimize cost: sum{i in L, j in F} p[i]*c[j]*x[i,j];

# constraints
subject to assignment{j in F}: sum{i in L} x[i,j] = 1;
subject to link_capacity{i in L}: sum{j in F} c[j]*x[i,j] <= k[i];
