# smartgrid lines monitoring (.mod file)

## sets and parameters
# set of buses
set V;
# type of bus: 0=generator, 1=consumer, 2=repeater (also reads V from .dat)
param bustype{V} symbolic;

# set of lines
set E within {V,V};
# line weight (also reads E from .dat)
param w{E};
# set of pairs of antiparallel arcs
set A := E union {u in V, v in V : (v,u) in E};

# set of monitoring devices
set D ordered;
# cost of monitoring device
param devcost{D};
# set of multiple-covering devices (assumes they are the first two in the set)
set DM := {member(1,D), member(2,D)};
# set of single-covering devices
set D1 := D diff DM;

# stars
set N{u in V} := {v in V : (u,v) in A};
param starsize{u in V} := card(N[u]);

## decision variables

# device at a bus
var x{D,V} binary;

# for d in D and (u,v) in A, v is covered by a device d installed at u 
var y{D,A} binary;

## objective function
minimize total_cost: sum{d in D} devcost[d] * sum{v in V} x[d,v];
 
## constraints

# device types
subject to consumer_repeater{v in V : bustype[v] = "gen"}: x["devB", v] = 0;
subject to generator{v in V : bustype[v] in {"con", "rep"}}: x["devC", v] == 0;
subject to repeater{v in V : bustype[v] in {"gen", "con"}}: x["devD", v] == 0;
subject to consumer{v in V : bustype[v] in {"gen", "rep"}}: x["devE", v] == 0;

# at most one device at each node
subject to assignment{v in V} : sum{d in D} x[d,v] <= 1;

# devA: every node adjacent to installed node is covered
subject to coverall{u in V, v in N[u]}: y[member(1,D),u,v] == x[member(1,D),u];

# devB: at most two nodes adjacent to installed node are covered
subject to covertwo{u in V} :
  sum{v in N[u]} y[member(2,D), u,v] ==
    (if starsize[u] == 1 then 1 else 2) * x[member(2,D), u];

# devC, devD, devE: exactly one node adjacent to installed node is covered
subject to coverone{d in D1, u in V} : sum{v in N[u]} y[d,u,v] == x[d, u];

# line is covered
subject to line_cover{(u,v) in E}:
  sum{d in D} y[d,u,v] + sum{e in D} y[e,v,u] >= 1;
