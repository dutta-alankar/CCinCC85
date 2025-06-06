#!/bin/bash
module purge
module load paraview

for i in {0..100}; do
    time pvbatch ./area+volume_paraview-filters.py /freya/ptmp/mpa/adutt/CCinCC85/cc85/output-$1 $i $1
    # rm core.$(hostname).*
done
