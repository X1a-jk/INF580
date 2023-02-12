## code by Ziyad BENOMAR (210129)

## Parameters
# number of variables
param n integer, >=0;
set N := {1..n};
# number of clauses
param m integer, >=0;
set M := {1..m};
# Clauses :
# clauses[i,j] = 1 if x[i] is in the clause j
# clauses[i,j] = -1 if bar_x[i] is in the clause j
# clauses[i,j] = 0 otherwise
param clauses{N,M} integer;


## Variables
var x{N} binary;

## Constraints
subject to satisfy_clause{j in M}:
    sum{i in N : clauses[i,j] == 1} x[i] + sum{i in N : clauses[i,j] == -1} (1-x[i]) >= 1;
