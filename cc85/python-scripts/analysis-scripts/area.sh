#!/bin/bash
module purge
module load paraview

export data_dir="/freya/ptmp/mpa/adutt/CCinCC85/cc85"
for i in {0..100}; do
    pvpython ./area-calculator_paraview.py $data_dir/output-$1 $i $1
    rm core.$(hostname).*
done
