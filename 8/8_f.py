"""
# a
with open('8_input.txt') as file:
    lines = [line.rstrip() for line in file]   # nebo # lines = [line.rstrip('\n') for line in file] pro smazani "\n"

ends = [i.split('|') for i in lines]
ends = ends[:-1]
ends = [i[1] for i in ends]
ends = [i.strip() for i in ends]
ends = [i.split(' ') for i in ends]
ends = [[len(i[0]), len(i[1]), len(i[2]), len(i[3])] for i in ends]
ends2 = []
for i in ends:
    for element in i:
            ends2.append(element)

ones = ends2.count(2)
fours = ends2.count(4)
sevens = ends2.count(3)
eights = ends2.count(7)
result = ones+fours+sevens+eights
print(result)
"""

# b
seven_segment_digits = {0: {'a', 'b', 'c', 'e', 'f', 'g'}, 1: {'c', 'f'}, 2: {'a', 'c', 'd', 'e', 'g'}, 3: {'a', 'c', 'd', 'f', 'g'}}
seven_segment_digits.update({4: {'b', 'c', 'd', 'f'}, 5: {'a', 'b', 'd', 'f', 'g'}, 6: {'a', 'b', 'd', 'e', 'f', 'g'}, 7:{'a', 'c', 'f'}})
seven_segment_digits.update({8: {'a', 'b', 'c', 'd', 'e', 'f', 'g'}, 9: {'a', 'b', 'c', 'd', 'f', 'g'}})

def solve_seven_segments(input_txt_file, seven_segment_dict = seven_segment_digits):

    with open(input_txt_file) as file:
        lines = [line.rstrip() for line in file]

    ends = [i.split('|') for i in lines]
    ends = ends[:-1]
    ends = [i[1] for i in ends]
    ends = [i.strip() for i in ends]
    ends = [i.split(' ') for i in ends]
    ends_deciphered = []

    beginnings = [i.split('|') for i in lines]
    beginnings = beginnings[:-1]
    beginnings = [i[0] for i in beginnings]
    beginnings = [i.strip() for i in beginnings]
    beginnings = [i.split(' ') for i in beginnings]

    positions_to_ciphers = []
    ciphers_to_positions = []

    for item in range(len(beginnings)):
        # find the difference between seven-segment 7 and seven-segment 1 (= upper horizontal bar):
        selected = [i for i in beginnings[item] if (len(i) == 2 or len(i) == 3)]
        assert len(selected) == 2
        selected = ''.join(selected)
        selected_count = {selected.count(i):i for i in selected}
        fin_a = selected_count[1]

        selected5 = [i for i in beginnings[item] if len(i) == 5]
        # find the difference between seven-segment 4 and seven-segment 2,5,3 (= central horizontal bar)
        assert len(selected5) == 3
        selected5_joined = ''.join(selected5)
        selected5_count = {i:selected5_joined.count(i) for i in selected5_joined}
        selected5_horizontal = {k:v for k, v in selected5_count.items() if v == 3}
        assert fin_a in selected5_horizontal.keys()

        selected4 = [i for i in beginnings[item] if len(i) == 4]
        assert len(selected4) == 1
        for i in selected5_horizontal.keys():
            if i in selected4[0]:
                fin_d = i
            if (i != fin_a and i not in selected4[0]):
                fin_g = i

        # find the difference between seven-segment 4 and even-segment 7
        for i in selected4[0]:
            if (i not in selected and i != fin_d):
                fin_b = i

        # find the value that is not in the set of known letters and not seven-digit in 4 either
        for word in selected5:
            for letter in word:
                if (letter not in selected4[0] and letter not in [fin_a, fin_d, fin_b, fin_g]):
                    fin_e = letter
                    # print(fin_e, item)

            # find the unknown value contained in seven-segment 5 (bottom right vertical bar)
            if (fin_a in word and fin_d in word and fin_g in word and fin_b in word):
                word_replaced = word.replace(fin_a, '_')
                word_replaced = word_replaced.replace(fin_d, '_')
                word_replaced = word_replaced.replace(fin_g, '_')
                word_replaced = word_replaced.replace(fin_b, '_')
                word_replaced = word_replaced.replace('_', '')
                fin_f = word_replaced

        # find the only missing value
        for word in selected5:
            for letter in word:
                if letter not in [fin_a, fin_b, fin_d, fin_e, fin_f, fin_g]:
                    fin_c = letter

        encrypted = {'a': fin_a, 'b': fin_b, 'c': fin_c, 'd': fin_d, 'e': fin_e, 'f': fin_f, 'g': fin_g}
        positions_to_ciphers.append(encrypted)
        ciphers_to_positions.append({v:k for k,v in encrypted.items()})

        end_deciphered = []
        for word in ends[item]:
            word_deciphered = set()
            for letter in word:
                word_deciphered.add(str(ciphers_to_positions[item][letter]))
            end_deciphered.append(word_deciphered)
        ends_deciphered.append(end_deciphered)

    result = 0
    for end in ends_deciphered:
        wordset_to_number = ''
        for word_set in end:
            for k, v in seven_segment_dict.items():
                if word_set == v:
                    wordset_to_number += str(k)
        result += int(wordset_to_number)
    return result


print(solve_seven_segments('8_input.txt'))


























