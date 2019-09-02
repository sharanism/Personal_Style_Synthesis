import pandas as pd
import os
import numpy as np
import math


def get_data_file(path):
    return pd.read_csv(path, delimiter='\t')


def get_all_files_of_person(input_name):
    """
    :param input_name: name of the artist
    :return: list of all the files of the given name (in csv format)
    """
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
    """
    :param data: csv format data
    :return: list of dicts. every dict represent a stripe, the keys are the columns ('time','x','y',...), the values
             are floats the represent the values of every row in the stripe.
    """
    stripe_list = []
    stripe = dict()
    counter = 0
    for i, time in enumerate(data['time']):
        if time == 'Pause':
            if i - counter < 2:
                counter = i + 1
                continue
            for column in data:
                stripe[column] = data[column][counter:i]
            counter = i + 1
            stripe_list.append(stripe)
            stripe = dict()

    return stripe_list


def calc_dist(old_x, new_x, old_y, new_y):
    """
    :return: the distance between two points
    """
    return math.sqrt(float(pow(new_x - old_x, 2)) + float(pow(new_y - old_y, 2)))


def calc_dist_of_stripe(x_array, y_array):
    """
    :param x_array: array of all the x values
    :param y_array: array of all the y values
    :return: the incremental distance in a single stripe
    """
    dist = 0
    for i in range(1, len(x_array)):
        dist += calc_dist(x_array[i-1], x_array[i], y_array[i-1], y_array[i])

    return dist


def calc_file_dist(stripes_list):
    """
    :param stripes_list: list of all the stripes, every stripe represent as dict
    :return: the total distance of the drawing
    """
    dist = 0
    for stripe in stripes_list:
        dist += calc_dist_of_stripe(list(stripe['x']), list(stripe['y']))

    return int(dist)




stripe_list = get_stripes(get_data_file("data/week1/D_01/aliza/aliza__130319_0935_D_01.txt"))
print(calc_file_dist(stripe_list))