
import numpy as np

# b
# parse input data
with open('9_input.txt') as file:
    lines = [line.rstrip() for line in file]

lines[0] = lines[0].replace('\ufeff', '')
lines = lines[:-1]
lines = [list(i) for i in lines]
lines = np.array(lines)
lines = lines.astype('int64')


# add a "frame of nines" to the array as a border
lines = np.insert(lines, 0, np.repeat(9, len(lines[0])), axis = 0)
lines = np.vstack((lines, [np.repeat(9, len(lines[0]))]))
lines = np.insert(lines, 0, 9, axis = 1)
nines = np.repeat(9, 102)
nines = nines[:, None]
lines = np.hstack((lines, nines))

# find all low points
low_points_coordinates = []
for row in range(len(lines)):
    for col in range(len(lines[0])):
        item = lines[row][col]
        if item != 9:
            neighbour_north = lines[row-1][col]
            neighbour_west = lines[row][col-1]
            neighbour_east = lines[row][col+1]
            neighbour_south = lines[row+1][col]
            if (neighbour_north > item and neighbour_west > item and neighbour_east > item and neighbour_south > item):
                low_points_coordinates.append((row, col))

class Point:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.explored = False
        self.in_queue = False
        self.follower = None
        self.basin_size = 1

    def get_value(self):
        return lines[self.coordinates[0], self.coordinates[1]]

    def get_neighbours(self):
        self.row = self.coordinates[0]
        self.col = self.coordinates[1]
        neighbours_coordinates = [(self.row - 1, self.col), (self.row + 1, self.col), (self.row, self.col + 1), (self.row, self.col - 1)]
        neighbours = [all_points[x] for x in neighbours_coordinates]
        return neighbours

    def set_follower(self, other_point):
        self.follower = other_point


class Queue:   # fifo queue with points to be explored
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def enqueue(self, point):
        if self.size == 0:
            self.head = point
            self.tail = point
        else:
            self.tail.set_follower(point)
            self.tail = point
        point.in_queue = True
        self.size += 1

    def dequeue(self):
        self.head.in_queue = False
        self.head.explored = True
        second_to_head = self.head.follower
        self.head = second_to_head
        self.size -= 1

def explore_basin(low_point):
    exploration = Queue()
    exploration.enqueue(low_point)
    low_point.basin_size = 1
    while exploration.size > 0:
        neighbours_inside_basin = []
        for neighbour in exploration.head.get_neighbours():
            if ((neighbour.explored == False) and (neighbour.get_value() != 9) and (neighbour.in_queue == False)):
                neighbours_inside_basin.append(neighbour)
        if len(neighbours_inside_basin) > 0:
            for neighbour in neighbours_inside_basin:
                exploration.enqueue(neighbour)
                low_point.basin_size += 1
            exploration.dequeue()
        else:
            exploration.dequeue()
    return low_point.basin_size

def instantiate_points():
    coordinates_combinations = []
    for i in range(len(lines)):
        for ii in range(len(lines[0])):
            coordinates_combinations.append((i, ii))
    all_points = {pair: Point(pair) for pair in coordinates_combinations}
    low_points = [all_points[coordinates] for coordinates in low_points_coordinates]
    return all_points, low_points
all_points, low_points = instantiate_points()

def get_result():
    all_basins = []
    for low_point in low_points:
        all_basins.append(explore_basin(low_point))
    all_basins.sort()
    three_largest = all_basins[-3:]
    return all_basins[-1]*all_basins[-2]*all_basins[-3]
print(get_result())






















