# subsetsum.mod

param n integer, >0;
set N:=1..n;
param a{N} integer, >=0;
param b integer, >=0;

var x{N} binary;

subject to setsum: sum{j in N} a[j]*x[j]=b;