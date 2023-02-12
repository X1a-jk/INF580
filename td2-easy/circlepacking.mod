# circlepacking.mod

param large := 100;         # a large value

# parameters
param pi := 4.0*atan(1);
param a > 0, default 6;     # length of carrying area  
param b > 0, default 2.5;   # width of carrying area
param r > 0, default 0.2;   # radius of beer crate
param n := floor(a*b / (pi*r^2));

# index set
set N := 1..n;

# decision variables
var x{N} >= -large, <= large;  # horizontal component of crate center
var y{N} >= -large, <= large;  # vertical component of crate center
var z{N} binary;               # whether crate can be placed

# objective
maximize crates: sum{i in N} z[i];

# constraints
subject to horizontal_packing1{i in N}: x[i] >= r*z[i];
subject to horizontal_packing2{i in N}: x[i] <= (a-r)*z[i];
subject to vertical_packing1{i in N}: y[i] >= r*z[i];
subject to vertical_packing2{i in N}: y[i] <= (b-r)*z[i];

subject to non_overlapping{i in N, j in N : i<j}:
  (x[i]-x[j])^2 + (y[i]-y[j])^2 >= (2*r)^2*(z[i] + z[j] - 1);


