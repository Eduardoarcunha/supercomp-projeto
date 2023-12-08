import matplotlib.pyplot as plt
import pickle


vertices = range(30, 36, 1)
mpi_times = [50, 280, 4, 11, 18, 39]
brute_times = [74, 558, 6, 18, 30, 56]
parallel_times = [44, 276, 3, 9, 17, 28]

plt.figure(figsize=(10, 6))
plt.title("Tempo de Execução Comparando com MPI")
plt.xlabel("Número de vértices")
plt.ylabel("Tempo (s)")
plt.plot(vertices, mpi_times, label="MPI", color="#25283D")
plt.plot(vertices, brute_times, label="Brute Force", color="#ff7f0e")
plt.plot(vertices, parallel_times, label="Parallel", color="#2ca02c")
plt.legend()
plt.savefig(f'mpi/mpi_plots.png')
