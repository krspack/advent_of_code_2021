
import csv
import pandas as pd
import matplotlib.pyplot as plt


class Edge:  # connection between stations
    def __init__(self, edge_id, vertex1, vertex2, time, line):
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

class Graph:    # tube network
  def __init__(self, directed = False):
    self.directed = directed
    self.all_vertices = all_vertices
    self.all_edges = all_edges

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


  def find_route(self, start, end):
        # Dijkstra algorithm implementation to navigate the London tube
        # input: names of tube stations in string format, case sensitive

        # 1. travese vertices
        # =========================
        # input turned into corresponding vertices:
        start_hub_id = int(stations_codelist.loc[start]['hub_id'])
        for station_id in self.all_vertices:
            if station_id[0] == start_hub_id:
                start = self.get_vertex(station_id)
                break
        end_hub_id = int(stations_codelist.loc[end]['hub_id'])
        for station_id in self.all_vertices:
            if station_id[0] == end_hub_id:
                end = self.get_vertex(station_id)
                break

        # variables outside the main for-loop
        unvisited = dict([(id_n, 1000) for (id_n, vertex) in self.all_vertices.items()])
        unvisited[start.station_id] = 0
        visited = []
        current = start
        routes = {current.station_id: [{'name': current.name, 'station_id': current.station_id}]}
        latest = None

        # traverse vertices:
        while end.visited == False:

            for neighbour_id in current.neighbours:
                neighbour = self.get_vertex(neighbour_id)
                edge_to_neighbour = self.get_edge_between(current, neighbour)  #[]
                if edge_to_neighbour.time == time_to_change_lines and (edge_to_neighbour.vertex1 == start.station_id or edge_to_neighbour.vertex2 == end.station_id):
                    edge_to_neighbour.time = 0

                # store the quickest path to each visited vertex in a dict called Routes:
                if neighbour.station_id in unvisited:
                    if unvisited[neighbour.station_id] > (unvisited[current.station_id] + edge_to_neighbour.time):
                        unvisited[neighbour.station_id] = unvisited[current.station_id] + edge_to_neighbour.time
                        routes[neighbour.station_id] = routes[current.station_id][:]
                        routes[neighbour.station_id].append({"name": neighbour.name, 'station_id': neighbour.station_id})

            # make sure visited vertices will not be visited again. Close the loop by changing Current:
            current.visited = True
            visited.append(unvisited.pop(current.station_id))
            for station_id, overall_time in unvisited.items():
                if overall_time == min(unvisited.values()):
                    next_key = station_id
            latest = current
            current = self.get_vertex(next_key)

        print(routes[end.station_id])

        return 'from: {} to: {}, duration: {} minutes'.format(start.name, end.name, visited[-1])


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
print(tube.find_route('start', 'end'))








