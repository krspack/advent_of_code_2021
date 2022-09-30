import pandas as pd
import numpy as np

# open, get data
with open('4_input.txt', 'r') as i:
    drawn = i.readline()
    tabs = i.readlines()

# clear the first line, i. e. numbers drawn in a lottery
drawn = drawn.split(",")
drawn[-1] = drawn[-1].strip()
drawn = [int(i) for i in drawn]

# split the tables, save them as individual lists, then as dataframes
start_table_list = [i for i, value in enumerate(tabs) if value == "\n"]
tables_list = []
for i in start_table_list:
    try:
        tables_list.append([tabs[i+1], tabs[i+2], tabs[i+3], tabs[i+4], tabs[i+5]])
    except:
        IndexError

list_dataframes = []
for table in tables_list:
    newtable = []
    for item in table:
        item = item.split()
        item[-1] = item[-1].strip()
        item = [int(i) for i in item]
        newtable.append(item)
    list_dataframes.append(newtable)
list_dataframes = [pd.DataFrame(item, columns = [0, 1, 2, 3, 4]) for item in list_dataframes]

# a
def forloop(list_of_dataframes, list_of_numbers):
        for drawn in list_of_numbers:
            for index, dataframe in enumerate(list_of_dataframes):
                dataframe.replace(drawn, 100, inplace = True)
                for col in dataframe.columns:
                    if sum(dataframe[col]) == 500:
                        unmarked_numbers = 0
                        for ar in dataframe.values:
                            for item in ar:
                                if item != 100:
                                    unmarked_numbers += item
                        return unmarked_numbers*drawn

                for col in dataframe.T.columns:
                    if sum(dataframe.T[col]) == 500:
                        unmarked_numbers = 0
                        for ar in dataframe.values:
                            for item in ar:
                                if item != 100:
                                    unmarked_numbers += item
                        return unmarked_numbers*drawn

final_score = forloop(list_dataframes, drawn)
print(final_score)



# b
def forloop_b(list_of_dataframes, list_of_numbers):
    tabs_dict = {}
    for index, table in enumerate(list_of_dataframes):
        tabs_dict[index] = [True, table]

    falses = 0
    for drawn in list_of_numbers:
        number_index = list_of_numbers.index(drawn)
        for table_index, tabs_bool in tabs_dict.items():
            if tabs_bool[0] == True:
                tabs_bool[1].replace(drawn, 100, inplace = True)
                for col in tabs_bool[1].columns:
                    if sum(tabs_bool[1][col]) == 500:
                        if tabs_bool[0] == True:
                            falses += 1
                        tabs_bool[0] = False
                    if falses == len(tabs_dict.keys()):
                        table_values = tabs_bool[1].values
                        unmarked_numbers = 0
                        for single_array in table_values:
                            for item in single_array:
                                if item != 100:
                                    unmarked_numbers += item
                        return unmarked_numbers*drawn
                for col in tabs_bool[1].T.columns:
                    if sum(tabs_bool[1].T[col]) == 500:
                        if tabs_bool[0] == True:
                            falses += 1
                        tabs_bool[0] = False
                    if falses == len(tabs_dict.keys()):
                        table_values = tabs_bool[1].values
                        unmarked_numbers = 0
                        for single_array in table_values:
                            for item in single_array:
                                if item != 100:
                                    unmarked_numbers += item
                        return unmarked_numbers*drawn
print(forloop_b(list_dataframes, drawn))

















