import pandas as pd
import os
import numpy as np
import math


def get_data_file(path):
    data = pd.read_csv(path, delimiter='\t')
    return data


def get_all_files_of_person(input_name):
    lst = []
    for week in os.listdir("data"):
        if week != ".DS_Store":
            for type in os.listdir("data/" + week):
                if type != ".DS_Store":
                    for name in os.listdir("data/" + week + "/" + type):
                        if name == input_name:
                            for file in os.listdir("data/" + week + "/" + type + "/" + name):
                                if file.endswith(".txt"):
                                    lst.append(get_data_file("data/" + week + "/" + type + "/" + name + "/" +
                                                             file))
    return lst


def get_stripes(data):
    stripe_list = []
    stripe = dict()
    counter = 0
    for i, time in enumerate(data['time']):
        if time == 'Pause':
            if i - counter < 2:
                counter = i
                continue
            for column in data:
                stripe[column] = data[column][counter:i]
            counter = i
            stripe_list.append(stripe)
            stripe = dict()

    return stripe_list


get_stripes(get_data_file("data/week1/D_01/aliza/aliza__130319_0935_D_01.txt"))