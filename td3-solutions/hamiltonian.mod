# hamiltonian.mod
# not so easy to write second order statement "for all subsets"
# proceed by fixed cardinality subsets

param n integer, > 0;
set V := 1..n;
set E within {V,V};
set A := E union {i in V, j in V : (j,i) in E};

var x{A} binary;

maximize feasibility_only: 0;

subject to successor{i in V} :
  sum{j in V : (i,j) in A} x[i,j] = 1;
subject to predecessor{j in V} :
  sum{i in V : (i,j) in A} x[i,j] = 1;

## invalid syntax
# subject to break_cycles{S subseteq V}:  
#   sum{i in S, j not in S : (i,j) in A} x[i,j] >= 1;

subject to singleton{i in V} :
  sum{j in V : i not in {j} and (i,j) in A} x[i,j] >= 1;

subject to pairs{i in V, j in V : i<j} :
  sum{k in V : k not in {i,j} and (i,k) in A} x[i,k] +
  sum{k in V : k not in {i,j} and (j,k) in A} x[j,k] >= 1;

subject to triplets{i in V, j in V, k in V : i<j and j<k} :
  sum{h in V : h not in {i,j,k} and (i,h) in A} x[i,h] + 
  sum{h in V : h not in {i,j,k} and (j,h) in A} x[j,h] + 
  sum{h in V : h not in {i,j,k} and (k,h) in A} x[k,h] >= 1;

# etc...
  

