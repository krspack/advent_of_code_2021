
from collections import defaultdict
import numpy as np
import csv

# parse input
with open('13_input.txt', encoding = 'utf-8-sig') as txt:
    lines = txt.readlines()
    lines = [x.strip() for x in lines]
    empty_line_index = lines.index('')
    coordinates = lines[:-(len(lines)-empty_line_index)]
    coordinates = [x.split(',') for x in coordinates]
    coordinates = [[int(x[1]), int(x[0])] for x in coordinates]
    fold_along = lines[-(len(lines)-empty_line_index-1):]
    fold_along = [x.replace('fold along ', '') for x in fold_along]
    fold_along = [x.split('=') for x in fold_along]

def get_empty_matrix(coordinates_list):
    xs = [item[0] for item in coordinates_list]
    ys = [item[1] for item in coordinates_list]
    max_y = max(ys)
    max_x = max(xs)
    return np.zeros((max_x + 1, max_y + 1))

def fill_matrix_with_dots(matrix = get_empty_matrix(coordinates), coordinates_list = coordinates):
    for pair_of_coordinates in coordinates_list:
        matrix[pair_of_coordinates[0], pair_of_coordinates[1]] += 1
    return matrix
updated_matrix = fill_matrix_with_dots()

"""

# a
def first_fold(matrix = updated_matrix, axis = fold_along[0][0], only_fold = int(fold_along[0][1]), coordinates_list = coordinates):
    if axis == 'x':
        for pair_of_coordinates in coordinates:
            col = pair_of_coordinates[1]
            if col > only_fold:
                complementary_col = matrix[:, (only_fold*2 - col)]
                complementary_col += matrix[:, col]
        matrix = matrix[:, :only_fold]
    else:
        for pair_of_coordinates in coordinates:
            row = pair_of_coordinates[0]
            if row > only_fold:
                complementary_column = matrix[(only_fold*2 - row)]
                complementary_column += matrix[row]
        matrix = matrix[:only_fold]
    not_zero = np.count_nonzero(matrix > 0)
    return not_zero
# print(first_fold())

"""

# b
def all_folds(matrix = updated_matrix, coordinates_list = coordinates, instructions = fold_along):
    for fold_instruction in instructions:
        where_to_fold = int(fold_instruction[1])
        axis = fold_instruction[0]
        new_coordinates = []
        if axis == 'x':
            for pair_of_coordinates in coordinates_list:
                col = pair_of_coordinates[1]
                if col > where_to_fold:
                    complementary_col = where_to_fold*2 - col
                    new_pair_of_coordinates = [pair_of_coordinates[0], complementary_col]
                    new_coordinates.append(new_pair_of_coordinates)
                    complementary_col = matrix[:, (where_to_fold*2 - col)]
                    col = matrix[:, col]
                    complementary_col += col
                else:
                    new_coordinates.append(pair_of_coordinates)
            matrix = matrix[:, :where_to_fold]
            coordinates_list = new_coordinates
        else:
            for pair_of_coordinates in coordinates_list:
                row = pair_of_coordinates[0]
                if row > where_to_fold:
                    complementary_row = where_to_fold*2 - row
                    new_pair_of_coordinates = [complementary_row, pair_of_coordinates[1]]
                    new_coordinates.append(new_pair_of_coordinates)
                    complementary_row = matrix[complementary_row]
                    row = matrix[row]
                    complementary_row += row
                else:
                    new_coordinates.append(pair_of_coordinates)
            matrix = matrix[:where_to_fold]
            coordinates_list = new_coordinates
    not_zero = np.count_nonzero(matrix > 0)
    return new_coordinates
coordinates_after_folding = all_folds()

final_array = fill_matrix_with_dots(matrix = get_empty_matrix(coordinates_after_folding), coordinates_list = coordinates_after_folding)

with open('final_array.csv', 'w', newline = '') as file:
    output_writer = csv.writer(file)
    for item in final_array:
        output_writer.writerow(item)

# >>>> open the csv file in an excel-like sheet and use conditional formatting to highlight all that is greater than zero












