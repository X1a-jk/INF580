# demands.mod

# index sets
param Tmax integer, >0; # months
param Lmax integer, >0; # loan lengths
set T := 1..Tmax;
set L := 1..Lmax;

# parameters
param d{T} >= 0;        # demand in month
param c{L} >= 0;        # cost of loan length

# decision variables
var x{T,L} integer, >= 0; # number of servers loaned in month T for length L

# objective
minimize cost: sum{l in L, t in T} c[l]*x[t,l];

# constraints
subject to demand_satisfaction{t in T}: 
  sum{h in L : h <= t} sum{l in L : l >= h} x[t-h+1,l] >= d[t];

