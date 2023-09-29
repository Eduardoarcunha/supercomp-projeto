import subprocess
import time
import matplotlib.pyplot as plt
import pathlib
from clique import Clique


executables_list = [
    {
        "name": "brute_force",
        "executable": "./clique_exaustiva.exe",
    },
    {
        "name": "heuristic",
        "executable": "./clique_heuristica.exe",
    }
]

input = "grafo.txt"

data = {
    "solver": [],
    "brute_force": [],
    "heuristic": []
}

vertices = range(5, 101, 1)

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
        executable = './executables' +  executables_list[n]["executable"]
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



fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (15,9))
ax1.set_title("Tamanho da maior clique")
ax1.set_xlabel("Número de vértices")
ax1.set_ylabel("Tamanho da maior clique")

ax2.set_title("Tempo de execução")
ax2.set_xlabel("Número de vértices")
ax2.set_ylabel("Tempo (s)")


for name in data.keys():
    time = []
    maximum_cliques = []

    for graph_res in data[name]:
        time.append(graph_res["time"])
        maximum_cliques.append(graph_res["maximum_clique"])

    lw = 5 if name == "solver" else 2

    ax1.plot(vertices, maximum_cliques, label=name, linewidth=lw)
    ax2.plot(vertices, time, label=name)

ax1.legend()
ax2.legend()
plt.savefig("summary.png")