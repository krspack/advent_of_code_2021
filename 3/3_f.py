import csv
import copy

def parse_test_input():
    with open('3_test_input.csv') as f:
        numbers = csv.reader(f)
        numbers = list(numbers)
        numbers[0][0] = numbers[0][0].replace("\ufeff","")
        numbers = numbers[:-1]
        numbers = [item for [item] in numbers]
        number_true = {i: True for i in numbers}
    return numbers, number_true

def parse_input():
    with open('3_input.csv') as f:
        numbers = csv.reader(f)
        numbers = list(numbers)
        numbers = [item for [item] in numbers]
        number_true = {i: True for i in numbers}
    return numbers, number_true

numbers = parse_input()[0]
number_true = parse_input()[1]



# a
def gamma_epsilon(list_numbers):
    mostcommon = ''
    leastcommon = ''
    for i in range(len(list_numbers[0])):
        ones = 0
        for item in numbers:
            if item[i] == '1':
                ones += 1
        if ones > len(numbers)/2:
            mostcommon = mostcommon + '1'
            leastcommon = leastcommon + '0'
        else:
            mostcommon = mostcommon + '0'
            leastcommon = leastcommon + '1'
    mostcommon = int(mostcommon, 2)
    leastcommon = int(leastcommon, 2)
    return mostcommon*leastcommon
print(gamma_epsilon(numbers))


# b

def get_oxygen_rating(countdown_dict):

    remaining_numbers = list(countdown_dict.values()).count(True)

    for i in range(len(list(countdown_dict.keys())[0]) + 1):
        if remaining_numbers > 1:
            def get_winning_number():
                ones = 0
                zeros = 0
                for k, v in countdown_dict.items():
                    if k[i] == '1' and v == True:
                        ones += 1
                    if k[i] == '0' and v == True:
                        zeros += 1
                assert ones + zeros > 0
                if ones >= zeros:
                    return 1
                if zeros > ones:
                    return 0

            def update_countdown_dict(winning_number):
                if winning_number == 1:
                    for key in countdown_dict.keys():
                        if key[i] == '0':
                            countdown_dict[key] = False
                if winning_number == 0:
                    for key in countdown_dict.keys():
                        if key[i] == '1':
                            countdown_dict[key] = False
                return countdown_dict

            countdown_dict = update_countdown_dict(winning_number = get_winning_number())
            remaining_numbers = list(countdown_dict.values()).count(True)

        else:
            for key, value in countdown_dict.items():
                if value:
                    key = ''.join(key)
                    key = int(key, 2)
                    return key

oxygen_rating = get_oxygen_rating(copy.deepcopy(number_true))



def get_CO2_scrubber_rating(countdown_dict2):

    remaining_numbers2 = list(countdown_dict2.values()).count(True)

    for i in range(len(list(countdown_dict2.keys())[0]) + 1):
        if remaining_numbers2 > 1:
            def get_winning_number2():
                ones = 0
                zeros = 0
                for key, value in countdown_dict2.items():
                    if key[i] == '1' and value == True:
                        ones += 1
                    if key[i] == '0' and value == True:
                        zeros += 1
                if ones >= zeros:
                    return 1
                if zeros > ones:
                    return 0

            def update_countdown_dict2(winning_number2):
                if winning_number2 == 1:
                    for key in countdown_dict2.keys():
                        if key[i] == '1':
                            countdown_dict2[key] = False
                if winning_number2 == 0:
                    for key in countdown_dict2.keys():
                        if key[i] == '0':
                            countdown_dict2[key] = False
                return countdown_dict2

            countdown_dict2 = update_countdown_dict2(winning_number2 = get_winning_number2())
            remaining_numbers2 = list(countdown_dict2.values()).count(True)

        else:
            for key, value in countdown_dict2.items():
                if value:
                    key = ''.join(key)
                    key = int(key, 2)
                    return key

CO2_scrubber_rating = get_CO2_scrubber_rating(copy.deepcopy(number_true))


def get_life_support_rating(oxygen = oxygen_rating, co2 = CO2_scrubber_rating):
    return oxygen*co2
print(get_life_support_rating())







