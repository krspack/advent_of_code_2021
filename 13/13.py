
"""
pracovat s matrixem, ktery neni tvoren sourarnicemi jako doposud, ale nulami nebo False-True
do nej se pak zapisuji tecky (nula se zvetsi o jednu atd)
"""





from collections import defaultdict
import numpy as np

# parse input
with open('13_test_input.txt', encoding = 'utf-8-sig') as txt:
    lines = txt.readlines()
    lines = [x.strip() for x in lines]
    print(lines)
    coordinates = lines[:-3]
    coordinates = [x.split(',') for x in coordinates]
    coordinates = [[int(x[0]), int(x[1])] for x in coordinates]
    fold_along = lines[-2:]
    fold_along = [x.replace('fold along ', '') for x in fold_along]
    fold_along = [x.split('=') for x in fold_along]
    fold = defaultdict(list)
    for item in fold_along:
        fold[item[0]].append(item[1])    # toto neni nutne, mozna lepsi by bylo nechat to ve tvaru [x, 8]

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

# a
def first_fold(matrix = updated_matrix, only_fold = int(fold['y'][0]), coordinates_list = coordinates):
    for pair_of_coordinates in coordinates:
        line = pair_of_coordinates[1]
        if line > only_fold:
            # print(pair_of_coordinates[1])
            # print(only_fold)
            complementary_line = matrix[(only_fold*2 - line)]
            print(line)
            print(matrix[line])
            print(complementary_line)
            complementary_line += matrix[line]
            print(complementary_line)
            print('--')
    matrix = matrix[:only_fold, :]
    not_zero = np.count_nonzero(matrix > 0)
    return not_zero
print(first_fold())



