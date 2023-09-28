import networkx as nx

# Nome do arquivo de entrada
nome_arquivo = "grafo.txt"

# Abrir o arquivo e pular a primeira linha
with open(nome_arquivo, 'r') as arquivo:
    next(arquivo)  # Pula a primeira linha

    # Lê o grafo a partir das linhas restantes
    G = nx.parse_adjlist(arquivo)

# Encontrar todas as cliques maximais
cliques_maximais = list(nx.find_cliques(G))

# Encontrar a clique máxima (a maior)
clique_maxima = max(cliques_maximais, key=len)


print("Cliques maximais encontradas:")
for clique in cliques_maximais:
    for n in range(len(clique)):
        clique[n] = int(clique[n])
    clique = sorted(clique)
    print(clique)

for n in range(len(clique_maxima)):
    clique_maxima[n] = int(clique_maxima[n])

clique_maxima = sorted(clique_maxima)

print("Clique máxima encontrada:", clique_maxima)