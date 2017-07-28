# -*- coding: utf-8 -*-

import json
import tkinter
import time
from collections import Counter
from tkinter import messagebox
from tkinter import filedialog

# select a .json file with the database export

root = tkinter.Tk()
root.withdraw()
messagebox.showinfo(title="Select file", message="Please select a json file")
mappingpath = filedialog.askopenfilename()

print("Enter a default matcher")

matcher_input = input()

default_matcher = matcher_input

mappingsdict = {}
bad_values = {}
temp_dict = {}
translations_list = []
values_to_avoid = ['multicolor', 'multicolore', 'multicoloured',
                   'multi-coloured', 'multicolour', 'multi', 'mehrfarbig']
finaldict = {}
datedict = {}
bad_values = {}
multi_transl_dict = {}
two_transl_dict = {}
source_map_item_list = []
list_of_values = []
list_of_dates = []
best_translation = ""
most_recent_date = ""

# if the translation is "multicolor" and the soruce value is not
# "multicolor", we don't want to use that map item


def clean_color_name_dict(input_dictionary):
    for key, value in input_dictionary.copy().items():
        if key[1].lower() not in values_to_avoid and (
                value[0].lower() in values_to_avoid):
            del input_dictionary[key]
            bad_values[key[1]] = value[0]

# if one source value has more than 2 translations, we pick the most common one


def pick_most_common_translation(input_dictionary, output_dictionary):
    list_of_values = (list(input_dictionary.values()))
    for item in list_of_values:
        translations_list.append(item[0].lower())
    best_translation = Counter(translations_list).most_common(1)[0][0]
    output_dictionary[(default_matcher, element)] = best_translation

# if there are only 2 translations, we pick the most recent one


def pick_most_recent_translation(input_dictionary, output_dictionary):
    list_of_values = (list(input_dictionary.values()))
    for item in list_of_values:
        datedict[time.strptime(item[1], '%Y-%m-%d %H:%M:%S')] = item[0]
    list_of_dates = (list(datedict.keys()))
    most_recent_date = max(list_of_dates)
    best_translation = datedict.get(most_recent_date)
    output_dictionary[(default_matcher, element)] = best_translation

# after reading the file, we create a dictionary with a tuple of the
# map_id and the source value as key and a list with the target value and
# the creation date as value


with open(mappingpath, encoding='utf-8-sig') as data_file:
    data = json.loads(data_file.read())
    number_of_elements = (len(data))
    print("number of json objects: ", number_of_elements)
    for index in range(0, number_of_elements):
        if "�" not in data[index]['source_value'] and (
                "�" not in data[index]['target_value']):
            mappingsdict[(data[index]['attribute_map_id'],
                          data[index]['source_value'])] = [
                data[index]['target_value'], data[index]['created_at']]


print("Json file processed")

# creating a list of unique source values to iterate through them and
# process the same source value twice
print("Creating list of source values")
for k, v in mappingsdict.items():
    source_map_item_list.append(k[1])


source_map_item_list = set(source_map_item_list)

elements_in_list = len(source_map_item_list)

# assumes input json is marketplace arc-specific
count = 0
for element in source_map_item_list:
    count += 1
    for key, value in mappingsdict.items():
        if key[1] == element:
            temp_dict[key] = value
    number_of_possible_translations = len(temp_dict.values())
    if number_of_possible_translations > 2:
        pick_most_common_translation(temp_dict, finaldict)
    elif number_of_possible_translations == 2:
        pick_most_recent_translation(temp_dict, finaldict)
    else:
        for i, e in temp_dict.items():
            finaldict[(default_matcher, i[1])] = e[0]
    temp_dict.clear()
    datedict.clear()
    del list_of_values[:]
    del translations_list[:]
    del list_of_dates[:]
    best_translation = ""
    most_recent_date = ""
    print("finished with item " + str(count) +
          " out of " + str(elements_in_list))


output_file = open(r'Target\Directory\Output_file.txt',
                   "w", encoding="utf-8")

output_file.write(
    "map_id	source_attribute_value	target_attribute_value" + "\n")

print("Writing output file")

for x, y in finaldict.items():
    if str(x[1]) != "" and str(y) != "":
        output_file.write(str(x[0]) + "	" + str(x[1]) + "	" + str(y) + "\n")

output_file.close()

print("Output file created!")
