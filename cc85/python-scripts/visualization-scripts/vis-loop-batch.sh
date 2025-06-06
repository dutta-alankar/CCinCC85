#!/bin/bash
module purge
module load paraview
for i in $(seq 0 8)  # First loop.
do
    for j in $(seq 0 100)
    do

        pvbatch $1 $i $j

    done
    echo
done
