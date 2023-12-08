#!/bin/bash
#SBATCH --job-name=mpi_clique
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4


echo Output do job $SLURM_JOB_ID
./executables_linux/clique_brute_without_mem ./grafos_mpi/grafo_35.txt
