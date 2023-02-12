set datafile separator comma
set term png
set output "clique.png"
plot "clique.csv" using 1:2:xtic(1) with lines title "omega(G)", "clique.csv" using 1:3:xtic(1) with lines title "CPU"
