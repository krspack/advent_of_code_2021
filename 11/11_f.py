
import numpy as np

with open('11_input.txt', encoding='utf-8-sig') as txt:
    lines = txt.readlines()
    lines = [x.strip() for x in lines]
    lines = [list(i) for i in lines]

lines = np.array(lines)
lines = lines.astype('int64')

class Octopus:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.energy_level = lines[self.coordinates]
        self.flashed = False

    def __repr__(self):
        return str(self.energy_level)

    def get_adjacent(self):
        self.row = self.coordinates[0]
        self.col = self.coordinates[1]
        adjacent_coordinates = [(self.row - 1, self.col), (self.row + 1, self.col), (self.row, self.col + 1), (self.row, self.col - 1),
        (self.row - 1, self.col - 1), (self.row - 1, self.col + 1), (self.row + 1, self.col - 1), (self.row + 1, self.col + 1)]
        adjacent_coordinates = [row_col_tuple for row_col_tuple in adjacent_coordinates if (row_col_tuple[0] in range(10) and row_col_tuple[1] in range(10))]
        return adjacent_coordinates

    def flash(self):
            # print('flash ', self.energy_level, self.coordinates, self.flashed)
            assert self.energy_level > 9
            self.energy_level = 0
            assert self.flashed == False
            self.flashed = True

def instantiate_octopuses(input_lines = lines):
    coordinates_combinations = []
    for i in range(len(input_lines)):
        for ii in range(len(input_lines[0])):
            coordinates_combinations.append((i, ii))
    all_octopuses = {pair: Octopus(pair) for pair in coordinates_combinations}
    return all_octopuses
all_octopuses = instantiate_octopuses()

# a
def one_step(octopuses = all_octopuses):
    # first:
    for octopus in octopuses.values():
        octopus.energy_level += 1
    # second:
    octopuses_to_flash = []
    flashes = 0
    for octopus in octopuses.values():
        if (octopus.energy_level > 9 and octopus.flashed == False):
            octopuses_to_flash.append(octopus)
    while len(octopuses_to_flash) > 0:
        for octopus in octopuses_to_flash:
            octopus.flash()
            flashes += 1
            octopuses_to_flash.remove(octopus)
            adjacent = octopus.get_adjacent()
            adjacent = [octopuses[x] for x in adjacent]
            for a in adjacent:
                a.energy_level += 1
                if (a.energy_level > 9 and a.flashed == False and a not in octopuses_to_flash):
                    octopuses_to_flash.append(a)
    # third:
    for octopus in octopuses.values():
        if octopus.flashed == True:
            octopus.energy_level = 0
            octopus.flashed = False
    return flashes

def repeat_steps(number_of_steps = 100):
    fleshes_sum = 0
    for i in range(number_of_steps):
        fleshes_sum += one_step()
    return fleshes_sum

print(repeat_steps())

# b
def one_step_b(octopuses = all_octopuses):
    # first:
    for octopus in octopuses.values():
        octopus.energy_level += 1
    # second:
    octopuses_to_flash = []
    for octopus in octopuses.values():
        if (octopus.energy_level > 9 and octopus.flashed == False):
            octopuses_to_flash.append(octopus)
    while len(octopuses_to_flash) > 0:
        for octopus in octopuses_to_flash:
            octopus.flash()
            octopuses_to_flash.remove(octopus)
            adjacent = octopus.get_adjacent()
            adjacent = [octopuses[x] for x in adjacent]
            for a in adjacent:
                a.energy_level += 1
                if (a.energy_level > 9 and a.flashed == False and a not in octopuses_to_flash):
                    octopuses_to_flash.append(a)
    # third:
    energy_levels = set()
    for octopus in octopuses.values():
        if octopus.flashed == True:
            octopus.energy_level = 0
            octopus.flashed = False
        energy_levels.add(octopus.energy_level)
    if len(energy_levels) > 1:
        return False
    return True


def flash_simultaneously(octopuses = all_octopuses):
    zeros = False
    result = 0
    while zeros == False:
        zeros = one_step_b()
        result += 1
    return result
print(flash_simultaneously())



