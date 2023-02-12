# hamiltonian_exp.mod
# example of exponential cardinality constraint family

param n integer, > 0;
set V ordered;
set E within {V,V};
set A := E union {i in V, j in V : (j,i) in E};
# index set for nontrivial subsets of V
set PV := 1..2**n-2;  
# nontrivial subsets of V
set S{k in PV} := {i in V: (k div 2**(ord(i)-1)) mod 2 = 1};

var x{A} binary;

maximize feasibility_only: 0;

subject to successor{i in V} :
  sum{j in V : (i,j) in A} x[i,j] = 1;
subject to predecessor{j in V} :
  sum{i in V : (i,j) in A} x[i,j] = 1;

# breaking non-hamiltonian cycles
subject to break_cycles{k in PV}:
  sum{i in S[k], j in V diff S[k]: (i,j) in A} x[i,j] >= 1;

