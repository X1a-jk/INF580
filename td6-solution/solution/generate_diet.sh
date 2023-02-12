#!/bin/sh

if [ "$1" = "" ]; then
    echo "syntax is $0 m n"
    exit 1
fi

m=$1
n=$2

echo "param m := $m;\n" > generate_diet.dat
echo "param n := $n;\n" >> generate_diet.dat

ampl generate_diet.run

mv -f diet.dat diet-${m}_${n}.dat

test -f diet-${m}_${n}.dat && echo "feasible $m x $n random diet problem instance saved in diet-${m}_${n}.dat.bz2" || echo "can't find diet-${m}_${n}.dat, something wrong"
bzip2 diet-${m}_${n}.dat

rm -f generate_diet.dat
