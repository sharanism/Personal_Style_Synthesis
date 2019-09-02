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


def calc_dist_2D(old_x, new_x, old_y, new_y):
    """
    :return: the distance between two points - 2D
    """
    return math.sqrt(float(pow(new_x - old_x, 2)) + float(pow(new_y - old_y, 2)))


def calc_dist_1D(old_point, new_point):
    """
    :return: the distance between two points - 1D
    """
    return abs(float(new_point) - float(old_point))


####################
# Geometric length #
####################
def calc_dist_of_stripe(x_array, y_array):
    """
    :param x_array: array of all the x values
    :param y_array: array of all the y values
    :return: the incremental distance in a single stripe
    """
    dist = 0
    for i in range(1, len(x_array)):
        dist += calc_dist_2D(x_array[i-1], x_array[i], y_array[i-1], y_array[i])

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


def calc_dist_average_of_stripe(stripes_list):
    return float(calc_file_dist(stripes_list)) / float(len(stripes_list))


###############
# Time length #
###############
def calc_time_of_stripe(time_array):
    time = 0
    for i in range(1, len(time_array)):
        time += calc_dist_1D(float(time_array[i - 1]), float(time_array[i]))

    return time


def calc_file_time(stripes_list):
    time = 0
    for stripe in stripes_list:
        time += calc_time_of_stripe(list(stripe['time']))

    return time


def calc_time_average_of_stripe(stripes_list):
    return float(calc_file_time(stripes_list)) / float(len(stripes_list))


#########
# Tests #
#########
input1 = "data/week1/D_01/aliza/aliza__130319_0935_D_01.txt"
input2 = "data/week1/D_01/zoey/zoey__130319_1208_D_01.txt"
stripe_list1 = get_stripes(get_data_file(input1))
stripe_list2 = get_stripes(get_data_file(input2))

print("In Dubby picture: ")
print()

print("Total geometric length of Aliza: " + str(calc_file_dist(stripe_list1)))
print("Average geometric length of Aliza: " + str(calc_dist_average_of_stripe(stripe_list1)))
print("Total time of Aliza: " + str(calc_file_time(stripe_list1)))
print("Average geometric length of Aliza: " + str(calc_time_average_of_stripe(stripe_list1)))

print()

print("Total geometric length of Zoey: " + str(calc_file_dist(stripe_list2)))
print("Average Geometric length of Zoey: " + str(calc_dist_average_of_stripe(stripe_list2)))
print("Total time of Zoey: " + str(calc_file_time(stripe_list2)))
print("Average geometric length of Zoey: " + str(calc_time_average_of_stripe(stripe_list2)))