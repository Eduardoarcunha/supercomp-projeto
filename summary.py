import subprocess
import time
import matplotlib.pyplot as plt
from clique import Clique
import pickle

input_file = "grafo.txt" 


class Summary():
    def __init__(self, vertices=range(5, 31, 1), linux=True, with_mem=True, without_mem=True):
        self.input = "grafo.txt"
        self.vertices = vertices
        self.with_mem = with_mem
        self.without_mem = without_mem
        self.directory = "./lin_executables"

        self.executables_dict = {
            "heuristic": {"executable": "/clique_heuristic", "color": "#1f77b4"}
        }

        if self.without_mem:
            self.executables_dict["brute_force_without_mem"] = {"executable": "/clique_brute_without_mem", "color": "#ff7f0e"}
            self.executables_dict["parallel_without_mem"] = {"executable": "/clique_parallel_without_mem", "color": "#2ca02c"}

        if self.with_mem:
            self.executables_dict["brute_force_with_mem"] = {"executable": "/clique_brute_with_mem", "color": "#d62728"}
            self.executables_dict["parallel_with_mem"] = {"executable": "/clique_parallel_with_mem", "color": "#9467bd"}

        if not linux:
            for name in self.executables_dict:
                self.executables_dict[name]["executable"] += ".exe"
            self.directory = "./win_executables"

        self.data = {
            "solver": [],
        }

        for executable in self.executables_dict.keys():
            self.data[executable] = []

        self.output = {
            "vertices": self.vertices,
            "data": self.data
        }

        self.max0, self.max1, self.max2 = 0, 0, 0

    def save_pickle_data(self):
        with open('data.pickle', 'wb') as handle:
            pickle.dump(self.output, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def plot_data(self):
        if self.without_mem and self.with_mem:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 15))
            memo_ax = ax4
            no_memo_ax = ax3
        elif self.with_mem:
            fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 15))
            memo_ax = ax3
            no_memo_ax = None
        elif self.without_mem:
            fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 15))
            no_memo_ax = ax3
            memo_ax = None
        else:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 15))
            no_memo_ax = None
            memo_ax = None

        ax1.set_title("Tamanho da maior clique")
        ax1.set_xlabel("Número de vértices")
        ax1.set_ylabel("Tamanho da maior clique")

        ax2.set_title("Tempo de execução")
        ax2.set_xlabel("Número de vértices")
        ax2.set_ylabel("Tempo (s)")

        if no_memo_ax:
            no_memo_ax.set_title("Tempo de Execução Sem Memoization")
            no_memo_ax.set_xlabel("Número de vértices")
            no_memo_ax.set_ylabel("Tempo (s)")

        if memo_ax:
            memo_ax.set_title("Tempo de Execução Com Memoization")
            memo_ax.set_xlabel("Número de vértices")
            memo_ax.set_ylabel("Tempo (s)")


        for name in self.data.keys():
            times = []
            maximum_cliques = []

            for graph_res in self.data[name]:
                times.append(graph_res["time"])
                maximum_cliques.append(graph_res["maximum_clique"])


            if name == "solver":
                lw = 5
                color = "#1f77b4"
            else:
                lw = 2
                color = self.executables_dict[name]["color"]

            ax1.plot(self.vertices, maximum_cliques, label=name, linewidth=lw, color=color)
            ax2.plot(self.vertices, times, label=name, color=color)

            self.max0 = max(max(times), self.max0)

            if name in ["brute_force_without_mem", "parallel_without_mem"] and no_memo_ax:
                no_memo_ax.plot(self.vertices, times, label=name, color=color)
                self.max1 = max(max(times), self.max1)

            if name in ["brute_force_with_mem", "parallel_with_mem"] and memo_ax:
                memo_ax.plot(self.vertices, times, label=name, color=color)
                self.max2 = max(max(times), self.max2)

        ax2.set_ylim([0, self.max0 * 1.1])

        if no_memo_ax:
            no_memo_ax.set_ylim([0, self.max1 * 1.1])
            no_memo_ax.legend()

        if memo_ax:
            memo_ax.set_ylim([0, self.max2 * 1.1])
            memo_ax.legend()

        ax1.legend()
        ax2.legend()
        plt.savefig("summary.png")
        plt.show()

    def calculate_times(self):
        for m in self.vertices:
            print(f'Calculating for {m} vertices...')
            Clique.generate_graph(num_vertices=m, connection_probability=0.7)

            res = {}
            start = time.perf_counter()
            maximal_cliques, maximum_clique = Clique.find_max_clique(self.input)
            end = time.perf_counter()

            res["time"] = end - start
            res["maximum_clique"] = len(maximum_clique)
            self.data["solver"].append(res)

            for name, details in self.executables_dict.items():
                executable = self.directory + details["executable"]
                print(f"Running {name}...")
                start = time.perf_counter()
                proc = subprocess.run([executable, self.input], text=True, capture_output=True)
                end = time.perf_counter()

                res = {}
                res["time"] = end - start
                res["maximum_clique"] = len(proc.stdout.split())
                self.data[name].append(res)

    def run(self):
        self.calculate_times()
        self.save_pickle_data()
        self.plot_data()


summary = Summary(vertices=range(5, 31, 1), linux=True, with_mem=True, without_mem=True)
summary.run()