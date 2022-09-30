import csv
import numpy as np

def get_data(csv_file):
    l = []
    with open(csv_file, newline = '') as inputfile:
        input_reader = csv.DictReader(inputfile, fieldnames = ['x_start', 2, 'y_end'])
        for line in input_reader:
            l.append(line)
    for d in l:
        d[2] = d[2].split()
        d[2] = [d[2][0], d[2][2]]
        d['y_start'] = d[2][0]
        d['x_end'] = d[2][1]
        d.pop(2)
    return l
data = get_data('5_input.csv')

def get_matrix(coordinates_list):
    max_value = 0
    min_value = 1000000

    for d in data:
        for value in d.values():
            value = int(value)
            if value > max_value:
                max_value = value
            if value < min_value:
                min_value = value
    return np.zeros((max_value + 1, max_value + 1))
m = get_matrix(data)


def get_coordinates(start_end_list):
    coordinates_integers = []
    for d in start_end_list:
        dd = {}
        for k, v in d.items():
           new_k, new_v = k, int(v)
           dd.update({new_k: new_v})
        coordinates_integers.append(dd)

    points_to_update = []

    for coordinates in coordinates_integers:
        x_start = coordinates['x_start']
        y_start = coordinates['y_start']
        x_end = coordinates['x_end']
        y_end = coordinates['y_end']

        # vertical lines
        if x_start == x_end:
            if y_start > y_end:
                while y_start != y_end:
                    points_to_update.append([x_start, y_start])
                    y_start -= 1
                points_to_update.append([x_end, y_end])
            if y_start < y_end:
                while y_start != y_end:
                    points_to_update.append([x_start, y_start])
                    y_start += 1
                points_to_update.append([x_end, y_end])

        # horizontal lines:
        if y_start == y_end:
            if x_start > x_end:
                while x_start != x_end:
                    points_to_update.append([x_start, y_start])
                    x_start -= 1
                points_to_update.append([x_end, y_end])
            if x_start < x_end:
                while x_start != x_end:
                    points_to_update.append([x_start, y_start])
                    x_start += 1
                points_to_update.append([x_end, y_end])

        # diagonal lines:
        if (abs(x_start - x_end) == abs(y_start - y_end)):
            if x_start < x_end and y_start < y_end:
                while (x_start != x_end and y_start != y_end):
                    points_to_update.append([x_start, y_start])
                    x_start += 1
                    y_start += 1
                points_to_update.append([x_end, y_end])
            if x_start > x_end and y_start > y_end:
                while (x_start != x_end and y_start != y_end):
                    points_to_update.append([x_start, y_start])
                    x_start -= 1
                    y_start -= 1
                points_to_update.append([x_end, y_end])
            if x_start < x_end and y_start > y_end:
                while (x_start != x_end and y_start != y_end):
                    points_to_update.append([x_start, y_start])
                    x_start += 1
                    y_start -= 1
                points_to_update.append([x_end, y_end])
            if x_start > x_end and y_start < y_end:
                while (x_start != x_end and y_start != y_end):
                    points_to_update.append([x_start, y_start])
                    x_start -= 1
                    y_start += 1
                points_to_update.append([x_end, y_end])
    return points_to_update

points_to_update = get_coordinates(data)

def update_points(matrix, coordinates):
    for point in coordinates:
        matrix[point[0], point[1]] += 1
    return matrix

updated_matrix = update_points(m, points_to_update)

def count_overlaps(matrix):
    counter = 0
    for i in updated_matrix:
        for ii in i:
            if ii > 1:
                counter += 1
    return(counter)

print(count_overlaps(updated_matrix))


