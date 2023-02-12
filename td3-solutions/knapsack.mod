# knapsack.mod

param n integer, > 0;
set N := 1..n;
param c{N} integer; # capacity occupied by object in knapsack
param w{N} integer; # worth of object
param K integer, >= 0;

var x{N} binary;

maximize value: sum{j in N} w[j]*x[j];
subject to knapsack: sum{j in N} c[j]*x[j] <= K;

