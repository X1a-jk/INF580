# transportation.mod
param Pmax integer;
param Qmax integer;
set P := 1..Pmax;
set Q := 1..Qmax;
param a{P};
param b{Q};
param c{P,Q};
var x{P,Q} >= 0;
minimize cost: sum{i in P, j in Q} c[i,j]*x[i,j];
subject to production{i in P}:
sum{j in Q} x[i,j] <= a[i];
subject to demand{j in Q}:
sum{i in P} x[i,j] >= b[j];