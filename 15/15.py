
from dijkstar import Graph, find_path
import numpy as np

with open('15_input.txt', encoding = 'utf-8-sig') as txt:
    lines = txt.readlines()
    lines = [x.strip() for x in lines]
    lines = [list(i) for i in lines]
    lines = np.array(lines)
    lines = lines.astype('int64')
    lines_width = np.shape(lines)[0]
    lines_length = np.shape(lines)[1]

# UNCOMMENT THIS TO GET SOLUTION OF PART B
"""
def b_multiply_array(current_array = lines):
    vstacked = lines.copy()
    for i in range(4):
        new_array = current_array.copy() + 1
        new_array[new_array == 10] = 1
        vstacked = np.vstack((vstacked, new_array))
        current_array = new_array

    hstacked = vstacked.copy()
    current_array = vstacked
    for i in range(4):
        new_array = current_array.copy() + 1
        new_array[new_array == 10] = 1
        hstacked = np.hstack((hstacked, new_array))
        current_array = new_array
    return hstacked
lines = b_multiply_array()
lines_width = np.shape(lines)[0]
lines_length = np.shape(lines)[1]
"""

class Position:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.risk_level = lines[self.coordinates]

    def __repr__(self):
        return str(self.risk_level)

    def get_adjacent(self):
        self.row = self.coordinates[0]
        self.col = self.coordinates[1]
        adjacent_coordinates = [(self.row - 1, self.col), (self.row + 1, self.col), (self.row, self.col + 1), (self.row, self.col - 1)]
        adjacent_coordinates = [row_col_tuple for row_col_tuple in adjacent_coordinates if (row_col_tuple[0] in range(lines_width) and row_col_tuple[1] in range(lines_length))]
        return adjacent_coordinates

def instantiate_positions(input_lines = lines):
    coordinates_combinations = []
    for i in range(len(input_lines)):
        for ii in range(len(input_lines[0])):
            coordinates_combinations.append((i, ii))
    all_positions = {coordinates: Position(coordinates) for coordinates in coordinates_combinations}
    return all_positions
all_positions = instantiate_positions()


graph = Graph()
for coordinates, position in all_positions.items():
    for adjacent in position.get_adjacent():
        adjacent = all_positions[adjacent]
        graph.add_edge(coordinates, adjacent.coordinates, adjacent.risk_level)
print(find_path(graph, (0,0), (lines_width - 1,lines_length - 1)))


