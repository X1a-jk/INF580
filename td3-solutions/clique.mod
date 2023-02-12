# clique.mod

param n integer, > 0;
set V := 1..n;
set E within {V,V};

var x{V} binary;
maximize clique_card: sum{j in V} x[j];
subject to notstable{i in V, j in V : i<j and (i,j) not in E}: x[i] + x[j] <= 1;

