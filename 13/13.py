
from collections import defaultdict
import numpy as np

# parse input
with open('13_input.txt', encoding = 'utf-8-sig') as txt:
    lines = txt.readlines()
    lines = [x.strip() for x in lines]
    empty_line_index = lines.index('')
    coordinates = lines[:-(len(lines)-empty_line_index)]
    coordinates = [x.split(',') for x in coordinates]
    coordinates = [[int(x[0]), int(x[1])] for x in coordinates]
    fold_along = lines[-(len(lines)-empty_line_index-1):]
    fold_along = [x.replace('fold along ', '') for x in fold_along]
    fold_along = [x.split('=') for x in fold_along]
    print(coordinates)

def get_empty_matrix(coordinates_list):
    ys = [item[0] for item in coordinates_list]
    xs = [item[1] for item in coordinates_list]
    max_y = max(ys)
    max_x = max(xs)
    return np.zeros((max_x + 1, max_y + 1))

def fill_matrix_with_dots(matrix = get_empty_matrix(coordinates), coordinates_list = coordinates):
    for pair_of_coordinates in coordinates:
        matrix[pair_of_coordinates[1], pair_of_coordinates[0]] += 1
    return matrix
updated_matrix = fill_matrix_with_dots()
print(updated_matrix)

"""
# a
def first_fold(matrix = updated_matrix, axis = fold_along[0][0], only_fold = int(fold_along[0][1]), coordinates_list = coordinates):
    if axis == 'y':
        print(axis, only_fold)
        for pair_of_coordinates in coordinates:
            line = pair_of_coordinates[1]
            if line > only_fold:
                # print(pair_of_coordinates[1])
                # print(only_fold)
                complementary_line = matrix[(only_fold*2 - line)]
                # print(line)
                # print(matrix[line])  # tu
                # print(complementary_line)
                complementary_line += matrix[line]
                # print(complementary_line)
                # print('--')
        matrix = matrix[:only_fold, :]
    else:
        print(axis, only_fold)
        for pair_of_coordinates in coordinates:
            column = pair_of_coordinates[0]
            if column > only_fold:
                print(pair_of_coordinates)
                complementary_column = matrix[:, (only_fold*2 - column)]
                # print(complementary_column)
                # print(matrix[:, column])
                # print(complementary_column)
                complementary_column += matrix[:, column]
                # print(complementary_column)
                # print('--')
        matrix = matrix[:, :only_fold]
    not_zero = np.count_nonzero(matrix > 0)
    return not_zero
print(first_fold())

"""

# b
def all_folds(matrix = updated_matrix, coordinates_list = coordinates, instructions = fold_along):
    for fold_instruction in instructions:
        print(fold_instruction)
        where_to_fold = int(fold_instruction[1])
        axis = fold_instruction[0]
        if axis == 'y':
            print('y')
            for pair_of_coordinates in coordinates:
                line = pair_of_coordinates[1]
                if line > where_to_fold:
                    # print(pair_of_coordinates[1])
                    # print(only_fold)
                    complementary_line = matrix[(where_to_fold*2 - line)]
                    # print(line)
                    # print(matrix[line])  # tu
                    # print(complementary_line)
                    complementary_line += matrix[line]
                    # print(complementary_line)
                    # print('--')
            matrix = matrix[:where_to_fold, :]
            print(matrix)
        else:
            print('x')
            for pair_of_coordinates in coordinates:
                column = pair_of_coordinates[1]
                if column > where_to_fold:
                    # print(pair_of_coordinates[1])
                    # print(only_fold)
                    complementary_column = matrix[:, (where_to_fold*2 - column)]
                    # print(column)
                    # print(matrix[:, column])
                    # print(complementary_column)
                    complementary_column += matrix[:, column]
                    # print(complementary_column)
                    # print('--')
            matrix = matrix[:, :where_to_fold]
    not_zero = np.count_nonzero(matrix > 0)
    return not_zero
print(all_folds())
"""



