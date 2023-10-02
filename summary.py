import subprocess
import time
import matplotlib.pyplot as plt
from clique import Clique
import pickle

vertices = range(5, 11, 1)
max0, max1, max2 = 0,0,0
executables_list = [
    {
        "name": "brute_force_with_mem",
        "executable": "./clique_brute.exe",
    },
    {
        "name": "brute_force_without_mem",
        "executable": "./clique_brute_no_mem.exe",
    },
    {
        "name": "heuristic",
        "executable": "./clique_heuristic.exe",
    },
    {
        "name": "parallel_with_mem",
        "executable": "./clique_parallel.exe",
    },
    {
        "name": "parallel_without_mem",
        "executable": "./clique_parallel_no_mem.exe",
    }
]

input = "grafo.txt"

data = {
    "solver": [],
    "brute_force_with_mem": [],
    "brute_force_without_mem": [],
    "heuristic": [],
    "parallel_with_mem": [],
    "parallel_without_mem": []
}

for m in vertices:
    print(f'Calculating for {m} vertices...')
    Clique.generate_graph(num_vertices=m, connection_probability=0.7)

    res = {}
    start = time.perf_counter()
    maximal_cliques, maximum_clique = Clique.find_max_clique(input)
    end = time.perf_counter()

    res["time"] = end - start
    res["maximum_clique"] = len(maximum_clique)
    data["solver"].append(res)


    for n in range(len(executables_list)):
        executable = './win_executables' +  executables_list[n]["executable"]
        name = executables_list[n]["name"]

        print(f"Running {name}...")
        start = time.perf_counter()
        proc = subprocess.run([executable, input], text=True, capture_output=True)
        end = time.perf_counter()

        # print(f"Tempo de execução do {name}: {end - start:0.4f} segundos")
        # print(f"Output from {name}:")
        # print(proc.stdout)  # This line will print the output from the executable
        # print("----------")

        res = {}
        res["time"] = end - start
        res["maximum_clique"] = len(proc.stdout.split())
        data[name].append(res)


output = {
    "vertices": vertices,
    "data": data
}

with open('data.pickle', 'wb') as handle:
    pickle.dump(output, handle, protocol=pickle.HIGHEST_PROTOCOL)
    

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 15))

ax1.set_title("Tamanho da maior clique")
ax1.set_xlabel("Número de vértices")
ax1.set_ylabel("Tamanho da maior clique")

ax2.set_title("Tempo de execução")
ax2.set_xlabel("Número de vértices")
ax2.set_ylabel("Tempo (s)")

ax3.set_title("Tempo de Execução Sem Memoization")
ax3.set_xlabel("Número de vértices")
ax3.set_ylabel("Tempo (s)")

ax4.set_title("Tempo de Execução Com Memoization")
ax4.set_xlabel("Número de vértices")
ax4.set_ylabel("Tempo (s)")


for name in data.keys():
    time = []
    maximum_cliques = []

    for graph_res in data[name]:
        time.append(graph_res["time"])
        maximum_cliques.append(graph_res["maximum_clique"])

    lw = 5 if name == "solver" else 2

    ax1.plot(vertices, maximum_cliques, label=name, linewidth=lw)
    ax2.plot(vertices, time, label=name)

    max0 = max(max(time), max0)

    if name in ["brute_force_without_mem", "parallel_without_mem"]:
        ax3.plot(vertices, time, label=name)
        max1 = max(max(time), max1)

    if name in ["brute_force_with_mem", "parallel_with_mem"]:
        ax4.plot(vertices, time, label=name)
        max2 = max(max(time), max2)

ax2.set_ylim([0, max0 * 1.1])
ax3.set_ylim([0, max1 * 1.1])
ax4.set_ylim([0, max2 * 1.1])

ax1.legend()
ax2.legend()
ax3.legend()
ax4.legend()
plt.savefig("summary.png")