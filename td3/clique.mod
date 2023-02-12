# clique.mod

# index sets
param n integer, >0;
var k integer;
set V := 1..n;
set E within {V,V};


# decision variables
var x{V} binary;

# objective
maximize max_clique: k;

# constraints
subject to equal_clique: k=sum{i in V} x[i];
subject to complement{i in V, j in V : i<j and (i,j) not in E}: x[i]+x[j]<=1;
