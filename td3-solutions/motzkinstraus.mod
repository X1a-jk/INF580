# Motzkin-Straus max clique formulation
param n integer, > 0;
set V := 1..n;
set E within {V,V};

var x{V} >= 0;

maximize msobj: sum{(i,j) in E} x[i]*x[j];
subject to simplex: sum{j in V} x[j] = 1;

