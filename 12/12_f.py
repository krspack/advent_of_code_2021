
from collections import defaultdict

with open('12_input.txt', encoding = 'utf-8-sig') as txt:
    edges = txt.readlines()
    edges = [x.strip('\n') for x in edges]
    edges = [x.split('-') for x in edges]
    edges = edges[:-1]

def get_vertices(edges = edges):
    vertices = set()
    for edge in edges:
        vertices.add(edge[0])
        vertices.add(edge[1])
    return vertices

def wildcard_into_edges(one_vertex, all_edges):
    new_edges = []
    for edge in all_edges:
        edge = [x+'_Wildcard' if x == one_vertex else x for x in edge]
        new_edges.append(edge)
    return new_edges


class Graph:

    def __init__(self):
        self.graph = defaultdict(list)

    def addEdge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def printAllPathsUtil(self, u, d, visited, path, all_paths):
        counter = 0
        visited[u][0] += 1
        path.append(u)
        if u == d:
            counter += 1
            all_paths.add(tuple(path))
        else:
            for i in self.graph[u]:
                if visited[i][0] < visited[i][1]:
                    counter += self.printAllPathsUtil(i, d, visited, path, all_paths)[0]
        path.pop()
        visited[u][0] -= 1
        return counter, all_paths

    def printAllPaths(self, s, d):
        all_paths = set()
        visited = {}
        for k in self.graph.keys():
            if 'Wildcard' in k:
                visited[k] = [0, 2]
            else:
                if k == k.upper():
                    visited[k] = [0, 1000000]
                else:
                    visited[k] = [0, 1]
        path = []
        return self.printAllPathsUtil(s, d, visited, path, all_paths)


all_results = []
for vertex in get_vertices():
    if (vertex not in ['start', 'end'] and vertex == vertex.lower()):
        modified_edges = wildcard_into_edges(vertex, edges)
        g = Graph()
        for edge in modified_edges:
            g.addEdge(*edge)
        results_per_wildcard = g.printAllPaths('start', 'end')
        all_results.append(results_per_wildcard)

final_set = set()
for result in all_results:
    set_of_lists = result[1]
    for one_list in set_of_lists:
        new_list = [(x.replace('_Wildcard', '') if 'Wildcard' in x else x) for x in one_list]
        final_set.add(tuple(new_list))
print(len(final_set))






