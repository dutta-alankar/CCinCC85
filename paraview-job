#!/bin/sh
#
#SBATCH --job-name="visualization"
#SBATCH --mail-type=NONE         # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=alankardutta@iisc.ac.in    # Where to send mail.  Set this to your email address
#SBATCH -p debug
#SBATCH -t 5-20:00:00 #dd-hh:mm:ss
#SBATCH -n 1
#SBATCH --output=%x-%j.log

if [ X"$SLURM_STEP_ID" = "X" -a X"$SLURM_PROCID" = "X"0 ]
then
  echo "=========================================="
  echo "Date            = $(date)"
  echo "SLURM_JOB_ID    = $SLURM_JOB_ID"
  echo "Nodes Allocated = $SLURM_JOB_NUM_NODES"
  echo "=========================================="
fi

echo "Working Directory = $(pwd)"

cd $SLURM_SUBMIT_DIR

export PROG="pvserver"

module purge
module load paraview/5.11.0
srun $PROG
