# assignment.mod

# index sets
param n integer, >0; # number of jobs
param m integer, >0; # number of machines
set J := 1..n;
set M := 1..m;

# parameters
param p{J} >= 0;     # completion time of jobs

# decision variables
var x{J,M} binary;   # assignment of job to machine
var mu{M} >= 0;      # completion time of machine
var t >= 0;          # auxiliary variable used to reformulating "max_i mu_i"

# objective
minimize makespan: t;

# constraints
subject to maxreformulation{i in M}: t >= mu[i];
subject to mudef{i in M}: mu[i] = sum{j in J} p[j]*x[j,i];
subject to assignment{j in J}: sum{i in M} x[j,i] = 1;

