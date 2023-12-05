#include <iostream>
#include <vector>
#include <fstream>
#include <algorithm>
#include <map>
#include <string>
#include <mpi.h>

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

vector<int> findCliqueBruteForce(vector<int> clique, vector<int> candidates, vector<vector<int>> &graph, int depth, int world_rank, int world_size, MPI_Status status){
    
    if (candidates.size() == 0){
        return clique;
    }

    int chunk_size, start, end;
    if (depth == 0){
        chunk_size = candidates.size() / world_size;
        start = world_rank * chunk_size;
        end = start + chunk_size;

        if (world_rank == world_size - 1){
            end = candidates.size();
        }
    } else {
        start = 0;
        end = candidates.size();
    }

    for (int i = start; i < end; i++) {
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
            newClique = findCliqueBruteForce(newClique, newCandidates, graph, depth + 1, world_rank, world_size, status);

            if (newClique.size() > maxClique.size()) {
                maxClique = newClique;
            }
        }
    }

    if (depth == 0){
        int size_tag = 12;
        int vector_tag = 13;
        if (world_rank != 0) {
            int size = maxClique.size();
            MPI_Send(&size, 1, MPI_INT, 0, size_tag, MPI_COMM_WORLD);
            MPI_Send(maxClique.data(), size, MPI_INT, 0, vector_tag, MPI_COMM_WORLD);
        } else {
            for (int i = 1; i < world_size; i++) {
                int size;
                MPI_Recv(&size, 1, MPI_INT, i, size_tag, MPI_COMM_WORLD, &status);
                vector<int> recvClique(size);
                MPI_Recv(recvClique.data(), size, MPI_INT, i, vector_tag, MPI_COMM_WORLD, &status);

                if (recvClique.size() > maxClique.size()) {
                    maxClique = recvClique;
                }
            }
        }
    }
    
    return maxClique;
}


int main(int argc, char* argv[]){

    MPI_Init(&argc, &argv);

    MPI_Status status;

    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <filename>" << std::endl;
        return 1;
    }

    double start_time = MPI_Wtime();

    vector<vector<int>> matrix;
    vector<int> maxClique;
    vector<int> candidates;


    string filename = argv[1];
    int numVertices;
    matrix = readGraph(filename, numVertices);
    
    for (int i = 0; i < numVertices; i++) {
        candidates.push_back(i);
    }

    maxClique = findCliqueBruteForce({}, candidates, matrix, 0, world_rank, world_size, status);

    if (world_rank == 0){
        cout << "Max clique size: " << maxClique.size() << endl;

        for (int node : maxClique) {
            cout << node + 1 << " ";
        }
    }

    double end_time = MPI_Wtime();

/*     if (world_rank == 0){
        cout << endl << "Time: " << end_time - start_time << endl;
    } */

    MPI_Finalize();

    return 0;
}