#!/bin/sh

if [ "$1" = "" ]; then
    echo "syntax is $0 file.dat.bz2"
    exit 1
fi

bzcat $1 > diet.dat
time ampl diet.run
rm -f diet.dat

