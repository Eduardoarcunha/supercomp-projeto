import networkx as nx
import random

class Clique:

    @staticmethod
    def generate_graph(filename="grafo.txt", num_vertices=30, connection_probability=0.7):
        """Generate a densely connected random graph and save to a file."""
        graph = nx.fast_gnp_random_graph(num_vertices, connection_probability)
        
        with open(filename, 'w') as file:
            file.write(f"{num_vertices} {graph.number_of_edges()}\n")
            for edge in graph.edges():
                file.write(f"{edge[0]+1} {edge[1]+1}\n")  # +1 to adjust indices (starting at 1)

        # print(f"Densely connected graph generated and saved in '{filename}'.")

    @staticmethod
    def find_max_clique(filename):
        with open(filename, 'r') as file:
            next(file)  # Skip the first line

            # Read the graph from the remaining lines
            G = nx.parse_adjlist(file)

        # Find all the maximal cliques
        maximal_cliques = list(nx.find_cliques(G))        
        maximum_clique = max(maximal_cliques, key=len)
        
        # Convert nodes to integers and sort them
        maximal_cliques = [sorted(map(int, clique)) for clique in maximal_cliques]
        maximum_clique = sorted(map(int, maximum_clique))
        
        return maximal_cliques, maximum_clique
    

Clique.generate_graph(num_vertices=40, connection_probability=0.7)
print(Clique.find_max_clique("grafo.txt")[1])