
from collections import defaultdict

with open('12_input.txt', encoding = 'utf-8-sig') as txt:
    edges = txt.readlines()
    edges = [x.strip('\n') for x in edges]
    edges = [x.split('-') for x in edges]
    edges = edges[:-1]

class Graph:

    def __init__(self):
        self.graph = defaultdict(list)

    def addEdge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def printAllPathsUtil(self, u, d, visited, path):
        counter = 0
        if u != u.upper():
            visited[u]= True
        path.append(u)
        if u == d:
            print(path)
            counter += 1
        else:
            for i in self.graph[u]:
                if visited[i]== False:
                    counter += self.printAllPathsUtil(i, d, visited, path)
        path.pop()
        visited[u]= False
        return counter

    def printAllPaths(self, s, d):
        visited = {k:False for k, v in self.graph.items()}
        path = []
        return self.printAllPathsUtil(s, d, visited, path)

# Create a graph given in the above diagram
g = Graph()
for edge in edges:
    g.addEdge(*edge)

print(g.printAllPaths('start', 'end'))