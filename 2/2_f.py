import csv

with open('2_input.csv') as inputfile:
    coordinates = csv.reader(inputfile)
    coordinates = list(coordinates)
    coordinates = [item for [item] in coordinates]

# a
def get_distance_depth(list_coordinates):
    distance = 0
    depth = 0
    for item in list_coordinates:
        if item.split()[0] == 'forward':
            distance += int(item.split()[1])
        if item.split()[0] == 'up':
            depth -= int(item.split()[1])
        if item.split()[0] == 'down':
            depth += int(item.split()[1])
    return distance*depth
print(get_distance_depth(coordinates))


# b
def get_distance_depth_2(list_coordinates):
    distance = 0
    depth = 0
    aim = 0
    for item in list_coordinates:
        if item.split()[0] == 'forward':
            distance += int(item.split()[1])
            depth += int(item.split()[1])*aim
        if item.split()[0] == 'up':
            aim -= int(item.split()[1])
        if item.split()[0] == 'down':
            aim += int(item.split()[1])
    return distance*depth
print(get_distance_depth_2(coordinates))

