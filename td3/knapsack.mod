# knapsack.mod

param n integer, >0;
set V:= 1..n;
param c{V} integer;
param w{V} integer;

param K integer, >0;

var x{V} binary;

maximize weight: sum{i in V} w[i]*x[i];

subject to cons: sum{i in V} c[i]*x[i]<=K;