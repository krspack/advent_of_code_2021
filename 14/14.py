
# parse input
with open('14_test_input.txt', encoding = 'utf-8-sig') as txt:
    lines = txt.readlines()
    lines = [x.strip() for x in lines]
    empty_line_index = lines.index('')
    initial_substance = lines[:-(len(lines)-empty_line_index)]
    insertions = lines[-(len(lines)-empty_line_index-1):]
    insertions = [x.split(' -> ') for x in insertions]
    insertions = {x[0]: x[1] for x in insertions}
    print(insertions)
    print(initial_substance)

def get_couples(formula = initial_substance, insertions = insertions):
    couples = []
    for i, letter in enumerate(formula[0]):
        try:
            couples.append([formula[0][i], formula[0][i+1]])
        except IndexError:
            continue
    couples = [''.join(x[:]) for x in couples]
    return couples
print(get_couples())

def insert(insertions = insertions, couples = get_couples()):
    new_couples = []
    for couple in couples:
        new_couples.append([couple[0], insertions.get(couple)])
        new_couples.append([insertions.get(couple), couple[1]])
    new_couples = [''.join(x[:]) for x in new_couples]
    return new_couples
print(insert())

def repeat(times):
    pass


