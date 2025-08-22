#!/bin/bash
# Usage: time bash ./cloud-analysis_paraview.sh c100,m1.496,T4e4,t8.00,r2826.838 1 100 16
# works with paraview v5.11.2
# job on freya: srun --job-name="cloud" --nodes=1 --ntasks-per-node=1 --partition=p.24h --time=00-23:59:58 --constraint=mem384G --mail-type=BEGIN --mail-user=alankard@mpa-garching.mpg.de --pty bash -i
module purge
# conda deactivate && module load paraview && 
cd /freya/ptmp/mpa/adutt/CCinCC85/cc85/python-scripts/analysis-scripts/
module load paraview/5.11

for i in $(seq $2 $3); do
    echo -ne "Working on file $i\r"
    # time pvbatch ./cloud-analysis_paraview-filters.py /freya/ptmp/mpa/adutt/CCinCC85/cc85/output-vanl-$1 $i $1
    time pvbatch ./cloud-analysis_paraview-filters.py /freya/ptmp/mpa/adutt/CCinCC85/cc85/output-$1 $i $1 $4
    # time pvbatch ./cloud-analysis_paraview-filters.py /freya/ptmp/mpa/adutt/CCinCC85/cc85/output-$1 $i $1
    # rm core.$(hostname).*
done