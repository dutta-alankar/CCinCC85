#!/bin/bash
# Usage: time bash ./cloud-analysis_paraview.sh c100,m1.496,T4e4,t8.00,r2826.838 1 100:q
module purge
# conda deactivate && module load paraview && 
cd /freya/ptmp/mpa/adutt/CCinCC85/cc85/python-scripts/analysis-scripts/
module load paraview

for i in $(seq $2 $3); do
    echo -ne "Working on file $i\r"
    # time pvbatch ./cloud-analysis_paraview-filters.py /freya/ptmp/mpa/adutt/CCinCC85/cc85/output-vanl-$1 $i $1
    time pvbatch ./cloud-analysis_paraview-filters.py /freya/ptmp/mpa/adutt/CCinCC85/cc85/output-$1 $i $1
    # time pvbatch ./cloud-analysis_paraview-filters.py /freya/ptmp/mpa/adutt/CCinCC85/cc85/output-$1 $i $1
    # rm core.$(hostname).*
done
