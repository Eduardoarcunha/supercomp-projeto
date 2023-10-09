import subprocess
import time
import matplotlib.pyplot as plt
from clique import Clique
import pickle
import uuid
import os

input_file = "grafo.txt" 


class MaxClique():
    def __init__(self, vertices=range(5, 31, 1), linux=True, with_mem=True, without_mem=True):
        self.input = "grafo.txt"
        self.vertices = vertices
        self.with_mem = with_mem
        self.without_mem = without_mem
        self.directory = "./executables_linux"
        self.id = f'verts_{len(vertices) + 4}_{str(uuid.uuid4())[:6]}'

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
            self.directory = "./executables_windows"

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

    def ensure_directory(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def save_pickle_data(self):
        directory = f'results/data'
        self.ensure_directory(directory)
        with open(f'{directory}/{self.id}.pickle', 'wb') as handle:
            pickle.dump(self.output, handle, protocol=pickle.HIGHEST_PROTOCOL)


    def plot_data(self):

        # Ensure the summary directory is created
        summary_dir = f'results/summaries/summary_{self.id}'
        self.ensure_directory(summary_dir)

        # Helper function to save and show plots
        def save_and_show_plot(fig, ax, name):
            ax.legend()
            fig.tight_layout()
            # Save plots in the desired directory structure
            plt.savefig(f'{summary_dir}/{name}.png')

        # 1. Plot for Maximum Clique Size
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        ax1.set_title("Tamanho da maior clique")
        ax1.set_xlabel("Número de vértices")
        ax1.set_ylabel("Tamanho da maior clique")
        for name in self.data.keys():
            maximum_cliques = [graph_res["maximum_clique"] for graph_res in self.data[name]]
            lw = 5 if name == "solver" else 2
            color = self.executables_dict[name]["color"] if name != "solver" else "#FF69B4"
            ax1.plot(self.vertices, maximum_cliques, label=name, linewidth=lw, color=color)
        save_and_show_plot(fig1, ax1, "max_clique_size_comparison")

        # 2. Plot for Execution Time
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        ax2.set_title("Tempo de execução")
        ax2.set_xlabel("Número de vértices")
        ax2.set_ylabel("Tempo (s)")
        for name in self.data.keys():
            times = [graph_res["time"] for graph_res in self.data[name]]
            lw = 5 if name == "solver" else 2
            color = self.executables_dict[name]["color"] if name != "solver" else "#FF69B4"
            ax2.plot(self.vertices, times, label=name, color=color)
            self.max0 = max(self.max0, max(times))
        ax2.set_ylim([0, self.max0 * 1.1])
        save_and_show_plot(fig2, ax2, "execution_time_all")

        # 3. Plot for Execution Time without Memoization
        if self.without_mem:
            fig3, no_memo_ax = plt.subplots(figsize=(10, 6))
            no_memo_ax.set_title("Tempo de Execução Sem Memoization")
            no_memo_ax.set_xlabel("Número de vértices")
            no_memo_ax.set_ylabel("Tempo (s)")
            for name in ["brute_force_without_mem", "parallel_without_mem"]:
                times = [graph_res["time"] for graph_res in self.data[name]]
                color = self.executables_dict[name]["color"]
                no_memo_ax.plot(self.vertices, times, label=name, color=color)
                self.max1 = max(self.max1, max(times))
            no_memo_ax.set_ylim([0, self.max1 * 1.1])
            save_and_show_plot(fig3, no_memo_ax, "execution_time_without_memoization")

        # 4. Plot for Execution Time with Memoization
        if self.with_mem:
            fig4, memo_ax = plt.subplots(figsize=(10, 6))
            memo_ax.set_title("Tempo de Execução Com Memoization")
            memo_ax.set_xlabel("Número de vértices")
            memo_ax.set_ylabel("Tempo (s)")
            for name in ["brute_force_with_mem", "parallel_with_mem"]:
                times = [graph_res["time"] for graph_res in self.data[name]]
                color = self.executables_dict[name]["color"]
                memo_ax.plot(self.vertices, times, label=name, color=color)
                self.max2 = max(self.max2, max(times))
            memo_ax.set_ylim([0, self.max2 * 1.1])
            save_and_show_plot(fig4, memo_ax, "execution_time_with_memoization")

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

max_clique = MaxClique(vertices=range(5, 31, 1), linux=False, with_mem=True, without_mem=True)
max_clique.run()