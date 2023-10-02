#include <iostream>
#include <vector>
#include <fstream>
#include <algorithm>

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


vector<int> findMaxCliqueAdjacentHeuristic(vector<vector<int>> graph, int numVertices){
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

        canAdd = true;

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

    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <filename>" << std::endl;
        return 1;
    }

    vector<vector<int>> matrix;
    vector<int> maxClique;
    string filename = argv[1];
    int numVertices;

    matrix = readGraph(filename, numVertices);
    maxClique = findMaxCliqueAdjacentHeuristic(matrix, numVertices);

    sort(maxClique.begin(), maxClique.end());
    for (int node : maxClique) {
        cout << node + 1 << " ";
    }

    return 0;
}