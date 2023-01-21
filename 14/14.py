
# parse input
with open('14_input.txt', encoding = 'utf-8-sig') as txt:
    lines = txt.readlines()
    lines = [x.strip() for x in lines]
    empty_line_index = lines.index('')
    initial_substance = lines[:-(len(lines)-empty_line_index)]
    insertions = lines[-(len(lines)-empty_line_index-1):]
    insertions = [x.split(' -> ') for x in insertions]
    insertions = {x[0]: x[1] for x in insertions}

def get_couples(formula = initial_substance, insertions = insertions):
    couples = []
    for i, letter in enumerate(formula[0]):
        try:
            couples.append([formula[0][i], formula[0][i+1]])
        except IndexError:
            continue
    couples = [''.join(x[:]) for x in couples]
    return couples
first_couples = get_couples()

def insert(couples, n, insertions = insertions):
    new_couples = []
    # print('x', n, couples, new_couples)
    if n == 0:
        couples = [couples[0][0]]+[x[1] for x in couples]
        return ''.join(couples[:])
    else:
        for couple in couples:
            new_couples.append([couple[0], insertions.get(couple)])
            new_couples.append([insertions.get(couple), couple[1]])
        new_couples = [''.join(x[:]) for x in new_couples]
        # print('y', n, couples, new_couples)
        return insert(new_couples, n-1)
new_formula = insert(first_couples, 10)

def count_result(formula = new_formula):
    frequencies = {x: new_formula.count(x) for x in new_formula}
    most_frequent = max(frequencies.values())
    least_frequent = min(frequencies.values())
    return most_frequent - least_frequent
print(count_result())







