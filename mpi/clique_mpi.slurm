#!/bin/bash
#SBATCH --job-name=mpi_clique
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=4


echo Output do job $SLURM_JOB_ID
mpirun ./executables_linux/clique_mpi ./grafos_mpi/grafo_35.txt
