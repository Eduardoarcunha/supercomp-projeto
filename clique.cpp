#include <iostream>
#include <vector>
#include <fstream>

using namespace std;

vector<vector<int>> readGraph(const string& filename, int& numVertices) {
    ifstream file(filename);
    int numEdges;
    file >> numVertices >> numEdges;

    vector<vector<int>> graph(numVertices, vector<int>(numVertices, 0));

    for (int i = 0; i < numEdges; ++i) {
        int u, v;
        file >> u >> v;
        graph[u - 1][v - 1] = 1;
        graph[v - 1][u - 1] = 1;  // O grafo é não direcionado
    }

    file.close();

    return graph;
}

int getVertexIndexWithMostAdjacents(vector<vector<int>> graph, vector<int> candidates){
    int maxAdj = 0;
    int maxAdjVertex = 0;
    int adjacents = 0;
    int v;

    for (int i = 0; i < candidates.size(); i++){
        v = candidates[i];
        adjacents = 0;

        for (int j = 0; j < graph[v].size(); j++){
            if (graph[v][j] == 1){
                adjacents++;
            }
        }

        if (adjacents > maxAdj){
            maxAdj = adjacents;
            maxAdjVertex = i;
        }
    }

    return maxAdjVertex;
    
}


vector<int> findMaxClique(vector<vector<int>> graph, int numVertices){
    vector<int> maxClique;
    vector<int> candidates;
    int v, u, c;
    int maxAdjVertex = 0;
    bool canAdd, adjacentToAll;

    for (int i = 0; i < numVertices; i++){
        candidates.push_back(i);
    }

    while (candidates.size() > 0){

        // heuristica: escolher o vértice com maior adjacencia
        maxAdjVertex = getVertexIndexWithMostAdjacents(graph, candidates);
        v = candidates[maxAdjVertex];
        candidates.erase(candidates.begin() + maxAdjVertex);

        // adiciona o primeiro candidato ao clique
        // v = candidates.back();
        // candidates.pop_back();

        canAdd = true;

        // verifica todos os vértices da clique, e ve se eles são adjacentes a v
        // é necessario, pois como arbitrariamente escolheu-se o ultimo, talvez os demais não sejam vizinhos!  
        
        // for (int n = 0; n < maxClique.size(); n++){
        //     u = maxClique[n];
        //     if (graph[u][v] == 0){
        //         canAdd = false;
        //         break;
        //     }
        // }

        if (canAdd){
            
            // adiciona v e cria novos candidatos
            maxClique.push_back(v);
            vector<int> newCandidates;

            // adiciona todos os novos candidatos, isto é, os que são adjacentes
            for (int n = 0; n < candidates.size(); n++){
                u = candidates[n];
                adjacentToAll = true;

                for (int m = 0; m < maxClique.size(); m++){
                    c = maxClique[m];
                    if (graph[u][c] == 0){
                        adjacentToAll = false;
                        break;
                    }
                }

                if (adjacentToAll){
                    newCandidates.push_back(u);
                }
            }
            // atualiza candidatos
            candidates = newCandidates;
        }
    }

    return maxClique;
}


int main(int argc, char* argv[]){

    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <filename>" << std::endl;
        return 1;
    }

    vector<vector<int>> matrix;
    vector<int> maxClique;
    string filename = argv[1];
    int numVertices = atoi(argv[2]);

    matrix = readGraph(filename, numVertices);
    maxClique = findMaxClique(matrix, numVertices);

    for (int node : maxClique) {
        cout << node + 1 << " ";
    }

    return 0;
}