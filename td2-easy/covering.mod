# covering.mod

param Inf := 1e30;      # a large value meaning "infinity"

# index sets
param n integer, > 0;
param m integer, > 0;
set N := 1..n;
set M := 1..m;

# parameters
param b{N} >= 0;       # capacity of candidate depot i
param f{N} >= 0;       # cost of building depot i
param d{M} >= 0;       # min demand for store j

# cost of transporting one unit from i to j
#   if not given, it defaults to "infinity" (i.e. depot can't ship to store)
param c{N,M} >= 0, default Inf;

# decision variables
var x{N,M} >= 0;       # units transported from i to j
var y{N} binary;       # =1 iff depot i is opened, 0 othw

# objective
minimize cost: sum{i in N, j in M} c[i,j]*x[i,j] + sum{i in N} f[i]*y[i];

# constraints
subject to capacity{i in N}: sum{j in M} x[i,j] <= b[i];
subject to choice{i in N, j in M}: x[i,j] <= b[i]*y[i];
subject to demand_satisfaction{j in M}: sum{i in N} x[i,j] >= d[j];
