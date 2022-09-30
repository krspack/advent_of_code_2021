
import csv


with open('1_input.csv') as inputfile:
    reader = csv.reader(inputfile)
    newlist = [int(item) for [item] in list(reader)]

# a
def count_increased_measurements(inputlist):
    diff_counter = 0
    for i in range(1, len(inputlist)):
        diff = inputlist[i] - inputlist[i-1]
        if diff > 0:
            diff_counter += 1
    return diff_counter
print(count_increased_measurements(newlist))


# b
sums = []
for i in range(len(newlist) - len(newlist)%3):
    a = sum(newlist[i: i+3])
    sums.append(a)
print(count_increased_measurements(sums))






