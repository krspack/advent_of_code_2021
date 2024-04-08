
import csv
import pandas as pd
import matplotlib.pyplot as plt





"""

postup:
1. upravit routes tak, aby se tam ukladaly vsechny cesty, ne jen ta nejkratsi
2. pak pridat dalsi podminku ohledne opakovaneho prochazeni
3. pak vyrobit funkci, co upravuje cave-vstup do tabulek
4. pak zjednodusit:
unvisited = jenom seznam
atd

ad 1:
Puvodne se neustale prepisoval jeden seznam stanic podle toho, jestli se naslo kratsi reseni.
Pro kazdou stanici mel Routes jenom jednu odpoved. End byla jen jedna ze stanic, skript to ale stejne musel vypocitat pro vsechny.
Jak to zmenit?
Routes bude promenna existujici mimo prochazeci funkci. Kazde zavolani prochazeci funkce vygeneruje jednu cestu a zapise ji do Routes.
Proto je mozne mit routes jako parametr instance tridy Vertex.
Z toho plune: Slovnik Visited se nebude v ramci prochazeci funkce vynulovavat, Unvisited taky ne.
Je mozne je mit jako parametry instance Graph:
    self.visited_vertices = []
    self.unvisited_vertices = []

"""


class Edge:  # connection between stations
    def __init__(self, edge_id, vertex1, vertex2, line, time = 1):
       self.edge_id = edge_id
       self.vertex1 = vertex1   # id-tuple of the vertex
       self.vertex2 = vertex2    # id-tuple of the vertex
       self.time = time    # in minutes
       self.line = line   # int
       self.coordinates = None

class Vertex:  # tube station
    def __init__(self, name, hub_id, station_id, lat, long):
        self.name = name  # not unique: there are often several stations under one roof, each defined by station-line tuple
        self.hub_id = hub_id
        self.station_id = station_id  # tuple(hub id, line id)
        self.lat = lat  # latitude
        self.long = long  # longitude
        self.visited = False
        self.neighbours = []  # station_id
        self.edges = []  # edge_id
        self.routes = []
        self.new_neighbours = []

    def __repr__(self):
        return str(self.station_id)

class Graph:    # tube network
  def __init__(self, directed = False):
    self.directed = directed
    self.all_vertices = all_vertices
    self.all_edges = all_edges
    self.visited_vertices = []
    self.unvisited_vertices = []

  def get_vertex(self, vertex_id):
      return self.all_vertices[vertex_id]

  def get_neighbours(self, vertex_id):
      vertex = self.all_vertices[vertex_id]
      return [self.all_vertices[id_number] for id_number in vertex.neighbours]

  def get_coordinates(self, edge, from_id):   # type Graph, type Edge, tuple representing vertex.station_id
      v1 = self.get_vertex(edge.vertex1)  # type Vertex
      v2 = self.get_vertex(edge.vertex2)  # type Vertex
      if from_id == v1.station_id:
          edge.coordinates = {'lat_from': v1.lat, 'long_from': v1.long, 'lat_to': v2.lat, 'long_to': v2.long}
      if from_id == v2.station_id:
          edge.coordinates = {'lat_from': v2.lat, 'long_from': v2.long, 'lat_to': v1.lat, 'long_to': v1.long}
      return edge.coordinates

  def get_edges_from(self, vertex):   # input: vertex > ids of corresponding edges. Output: type Edges
      edges_selected = [self.all_edges[edge_id] for edge_id in vertex.edges]
      return edges_selected

  def get_edge_between (self, vertex1, vertex2):
      if vertex1.station_id not in vertex2.neighbours:
        return 'no direct link between given stations'
      else:
        for edge_id in vertex1.edges:
            edge = self.all_edges[edge_id]
            if vertex2.station_id in [edge.vertex2, edge.vertex1] and vertex1.station_id in [edge.vertex2, edge.vertex1]:
                return edge


  def find_route(self):
        start = all_vertices[(1, 10)]
        end = all_vertices[(2, 10)]

        self.unvisited_vertices = dict([(vertex.station_id, 1000) for (id_n, vertex) in self.all_vertices.items()])
        self.unvisited_vertices[start.station_id] = 0

        def get_one_route():
            one_route = [start.station_id]
            current = start
            latest = None
            current_neighbours_visitable = current.neighbours   # pro prvni kolo
            while end.visited == False:
                for neighbour_id in current.neighbours:
                    if neighbour_id not in current_neighbours_visitable:
                        print('soused, co uz neni k dispozici: ', neighbour_id)

                    print('current: ', current, "(its neighbours ", current.neighbours, ')')
                    neighbour = self.get_vertex(neighbour_id)
                    print('neighbour ', neighbour)
                    edge_to_neighbour = self.get_edge_between(current, neighbour)  #[]
                    print(edge_to_neighbour)

                    # store the quickest path to each vertex in graph.unvisited = [[vertex.name: number], ...]
                    if neighbour.station_id in self.unvisited_vertices:
                        if self.unvisited_vertices[neighbour.station_id] > (self.unvisited_vertices[current.station_id] + edge_to_neighbour.time):
                            self.unvisited_vertices[neighbour.station_id] = self.unvisited_vertices[current.station_id] + edge_to_neighbour.time

                            # zapis tuto cestu do neighbour.routes, pokud tam jeste neni. Pokud tam je, tak nic, pokracuje se dal.
                            one_route.append(neighbour.station_id)
                            print('one route: ', one_route)
                            if one_route not in neighbour.routes:
                                neighbour.routes.append(one_route)
                                print('neighbour and its routes: ', neighbour, neighbour.routes)
                                print('------------')

                # make sure visited vertices will not be visited again. Close the loop by changing Current:
                current.visited = True
                print('end visited ', end.visited)
                self.visited_vertices.append(self.unvisited_vertices.pop(current.station_id))
                for station_id, overall_time in self.unvisited_vertices.items():
                    if overall_time == min(self.unvisited_vertices.values()):
                        next_key = station_id
                latest = current
                current = self.get_vertex(next_key)
                current_neighbours_visitable = [x for x in current.neighbours if x in self.unvisited_vertices]
            return [end.routes]
        return 'get one route to end: ', get_one_route()


# 3. handling the input data'
# ==========================
# create DataFrames from csvs, create a codelist to map each station name to an ID
stations_df = pd.read_csv('stations.csv').set_index('id', drop = False, verify_integrity = True)
stations_df = stations_df.rename(columns = {'id': 'hub_id'})
stations_codelist = stations_df[['hub_id', 'name']].set_index('name', drop=True, append=False, inplace=False, verify_integrity=True)  # print(stations_codelist.loc['Bank']['id'])

connections_df = pd.read_csv('connections.csv')
bigtab = connections_df.merge(stations_df, how = 'left', left_on = 'station1', right_on = 'hub_id')
bigtab['edge_id'] = range(len(bigtab))

# initiate vertices and edges:
all_vertices = {}
all_edges = {}
for i in range(len(bigtab)):
    row = dict(bigtab.iloc[i])
    all_vertices[tuple([row['station1'], row['line']])] = Vertex(row['name'], row['station1'], tuple([row['station1'], row['line']]), row['latitude'], row['longitude'])
    all_vertices[tuple([row['station2'], row['line']])] = Vertex(stations_df.loc[row['station2']]['name'], row['station2'], tuple([row['station2'], row['line']]), stations_df.loc[row['station2']]['latitude'], stations_df.loc[row['station2']]['longitude'])
    all_edges[i] = Edge(row['edge_id'], tuple([row['station1'], row['line']]), tuple([row['station2'], row['line']]), row['time'], row['line'])

# connect class Vertex with class Edge by filling vertex.neighbours and vertex.edges:
for i in range(len(bigtab)):
    row = dict(bigtab.iloc[i])
    vertex_to_update = all_vertices[tuple([row['station1'], row['line']])]
    vertex_to_update2 = all_vertices[tuple([row['station2'], row['line']])]
    vertex_to_update.edges.append(i)
    vertex_to_update2.edges.append(i)
    vertex_to_update.neighbours.append(tuple([row['station2'], row['line']]))
    vertex_to_update2.neighbours.append(tuple([row['station1'], row['line']]))

# vylepseni jen pro ucely caves debugging
for v in all_vertices.values():
    v.new_neighbours = []
    for n in v.neighbours:
        new_n = all_vertices[n].name
        v.new_neighbours.append(new_n)
    # print(v.name, v.new_neighbours)


# create edges representing interchanges at hubs(= stations with more than one line):
keys = range(1, len(stations_codelist)+2)
values = [[] for i in keys]
hubs = dict(zip(keys, values))

for id_tuple, vertex in all_vertices.items():
    hubs[id_tuple[0]].append(id_tuple)

i = 1000
time_to_change_lines = 10  # educated guess :-)
for hub in hubs.values():   # hub example: 1: [[1, 10], [1, 6], [1, 9]]
    for station in hub:  # station example: [1, 10]
        for s in hub:
            if station != s:
                all_vertices[station].neighbours.append(s)
                all_vertices[station].edges.append(i)
                all_edges[i] = Edge(i, station, s, time_to_change_lines, None)
                i += 1

li_list = []
indices = []
with open('lines.csv') as li:
    li_reader = csv.DictReader(li)
    for row in li_reader:
        li_list.append(row)
        indices.append(row['line'])
        indices = [int(item) for item in indices]
lines = pd.DataFrame(dict(l = li_list), index = indices)

tube = Graph()

# call the find_route function
print(tube.find_route())










