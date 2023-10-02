#include <iostream>
#include <vector>
#include <fstream>
#include <algorithm>
#include <map>
#include <string>

using namespace std;

vector<int> maxClique = {};


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
void print_depth(int depth){
    for (int i = 0; i < depth; i++){
        cout << "    ";
    }
}

vector<int> findCliqueBruteForce(vector<int> clique, vector<int> candidates, vector<vector<int>> &graph, int depth){
    if (candidates.size() == 0){
        return clique;
    }

    #pragma omp parallel for
    for (int i = 0; i < candidates.size(); i++) {
        int v = candidates[i];
        vector<int> newCandidates = {};
        vector<int> newClique = {};
  
        newClique = clique;
        auto it = lower_bound(newClique.begin(), newClique.end(), v);
        newClique.insert(it, v);

        for (int j = 0; j < candidates.size(); j++) {
            bool adjacent_to_all = true;
            int u = candidates[j];

            
            if (u != v) {
                for (int k = 0; k < newClique.size(); k++) {
                    
                    if (graph[u][newClique[k]] != 1) {
                        adjacent_to_all = false;
                        break;
                    }
                }
                if (adjacent_to_all) {
                    newCandidates.push_back(u);
                }
            }
        }

        if (newClique.size() + newCandidates.size() > maxClique.size()) {
            newClique = findCliqueBruteForce(newClique, newCandidates, graph, depth + 1);

            #pragma omp critical (maxClique_update)
            {
                if (newClique.size() > maxClique.size()) {
                    maxClique = newClique;
                }
            }
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
    vector<int> candidates;


    string filename = argv[1];
    int numVertices;
    matrix = readGraph(filename, numVertices);
    
    for (int i = 0; i < numVertices; i++) {
        candidates.push_back(i);
    }

    maxClique = findCliqueBruteForce({}, candidates, matrix, 0);

    for (int node : maxClique) {
        cout << node + 1 << " ";
    }
    

    return 0;
}