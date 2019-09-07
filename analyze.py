import pandas as pd
import os
import numpy as np
import math
import matplotlib.pyplot as plt
import scipy.fftpack


def get_data_file(path):
    return pd.read_csv(path, delimiter='\t')


def get_all_files_of_person(input_name):
    """
    :param input_name: name of the artist
    :return: list of all the files of the given name (in csv format)
    """
    lst = []
    for week in os.listdir("data"):
        if "DS_Store" not in week:
            for type in os.listdir("data/" + week):
                if "DS_Store" not in type:
                    for name in os.listdir("data/" + week + "/" + type):
                        if "DS_Store" not in name:
                            if name == input_name:
                                for file in os.listdir("data/" + week + "/" + type + "/" + name):
                                    if "DS_Store" not in file:
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


def calc_std(num_array):
    np_array = np.asarray(num_array)
    return np.std(np_array)

################################################################################
####################
# Geometric length #
####################
################################################################################
def calc_dist_of_stripe(x_array, y_array):
    """
    @TODO units? after dividing by 100 is cm?
    :param x_array: array of all the x values
    :param y_array: array of all the y values
    :return: the incremental distance in a single stripe, in cm (I think)
    """
    dist = 0.0
    arr = []
    for i in range(1, len(x_array)):
        arr.append(calc_dist_2D(x_array[i-1], x_array[i], y_array[i-1], y_array[i]))
        dist += calc_dist_2D(x_array[i-1], x_array[i], y_array[i-1], y_array[i])

    return dist / 100.0, arr


def calc_file_dist(stripes_list):
    """
    :param stripes_list: list of all the stripes, every stripe represent as dict
    :return: the total distance of the drawing
    """
    dist = 0.0
    arr = []
    for stripe in stripes_list:
        arr.append(calc_dist_of_stripe(list(stripe['x']), list(stripe['y']))[0])
        dist += calc_dist_of_stripe(list(stripe['x']), list(stripe['y']))[0]

    return int(dist), arr


def calc_dist_average_of_stripe(stripes_list):
    """
    :param stripes_list: list of all the stripes, every stripe represent as dict
    :return: average of geometric length of a single stripe
    """
    return float(calc_file_dist(stripes_list)[0]) / float(len(stripes_list))


def get_stripe_distance_std(stripe):
    return calc_std(calc_dist_of_stripe(list(stripe['x']), list(stripe['y']))[1])


def get_file_distance_std(stripes_list):
    return calc_std(calc_file_dist(stripes_list)[1])

################################################################################
###############
# Time length #
###############
################################################################################
def calc_time_of_stripe(time_array):
    """
    :param time_array: array of all the time of the given stripe
    :return: the incremental time of a single stripe
    """
    time = 0.0
    for i in range(1, len(time_array)):
        time += calc_dist_1D(float(time_array[i - 1]), float(time_array[i]))

    return time


def calc_file_time(stripes_list):
    """
    :param stripes_list: list of all the stripes, every stripe represent as dict
    :return: the total time of the drawing (without waiting between stripes)
    """
    time = 0.0
    for stripe in stripes_list:
        time += calc_time_of_stripe(list(stripe['time']))

    return time


def calc_time_average_of_stripe(stripes_list):
    """
    :param stripes_list: list of all the stripes, every stripe represent as dict
    :return: average time of a single stripe
    """
    return float(calc_file_time(stripes_list)) / float(len(stripes_list))


def calc_waiting_time(stripe_list):
    waiting_time = 0.0
    for i in range(1, len(stripe_list)):
        waiting_time += (float(list(stripe_list[i]['time'])[0]) - float(list(stripe_list[i-1]['time'])[-1]))

    return waiting_time

################################################################################
############
# Pressure #
############
################################################################################
def calc_pressure_average_of_stripe(pressure_array):
    """
    :param stripes_list: list of all the stripes, every stripe represent as dict
    :return: average time of a single stripe
    """
    pressure = 0.0
    for i in range(len(pressure_array)):
        pressure += float(pressure_array[i])

    return float(pressure) / float(len(pressure_array))


def calc_pressure_average_of_file(stripes_list):
    """
    :param stripes_list: list of all the stripes, every stripe represent as dict
    :return: the total time of the drawing (without waiting between stripes)
    """
    pressure = 0.0
    for stripe in stripes_list:
        pressure += calc_pressure_average_of_stripe(list(stripe['pressure']))

    return float(pressure) / float(len(stripes_list))

################################################################################
#########
# Speed #
#########
################################################################################
def calc_average_speed_in_stripe(stripe):
    """
    @TODO units? cm/sec?
    :param stripe: dict of feathers and their values
    :return: the average speed in stripe
    """
    return float(calc_dist_of_stripe(list(stripe['x']), list(stripe['y']))[0]) / \
           float(calc_time_of_stripe(list(stripe['time'])))


def calc_average_speed_in_file(stripe_list):
    """
    @TODO units? cm/sec?
    :param stripe_list: list of all the stripes, every stripe represent as dict
    :return: the average speed in the file
    """
    speed = 0.0
    for stripe in stripe_list:
        speed += calc_average_speed_in_stripe(stripe)

    return float(speed) / float(len(stripe_list))


def plot_speed_vs_stripeIndex(stripe_list):
    """
    plot graph of speed vs time # (its not really time)
    :param stripe_list: list of all the stripes, every stripe represent as dict
    """
    x = np.arange(len(stripe_list))
    y = np.zeros(len(stripe_list))
    for i, stripe in enumerate(stripe_list):
        y[i] = calc_average_speed_in_stripe(stripe)

    plt.scatter(x, y)
    plt.show()


################################################################################
###############
# Frequencies #
###############
################################################################################
def get_array_of_destances(x_array, y_array):
    arr = [0.0]
    for i in range(1, len(x_array)):
        arr.append(calc_dist_2D(x_array[i - 1], x_array[i], y_array[i - 1], y_array[i]))

    return arr


def length_vs_time(stripe):
    x = np.asarray(stripe['time'])
    y = np.asarray(get_array_of_destances(list(stripe['x']), list(stripe['y'])))

    # Number of samplepoints
    N = int(len(stripe))
    # sample spacing
    T = 1.0 / 200.0
    # x = np.linspace(0.0, N * T, N)
    # y = np.sin(50.0 * 2.0 * np.pi * x) + 0.5 * np.sin(80.0 * 2.0 * np.pi * x)
    yf = scipy.fftpack.fft(y)
    xf = np.linspace(0.0, 1.0 / (2.0 * N), int(N / 2))

    fig, ax = plt.subplots()
    ax.plot(xf, 2.0 / N * np.abs(yf[:N // 2]))
    plt.show()

    # t = np.arange(20)
    # sp = np.fft.fft(np.sin(t))
    # freq = np.fft.fftfreq(t.shape[-1])
    # plt.plot(freq, sp.real, freq, sp.imag)
    # plt.show()
    # #
    # # plt.plot(x, y)
    # # plt.show()

################################################################################
#########
# Tests #
#########
################################################################################
input1 = "data/week01/D_01/aliza/aliza__130319_0935_D_01.txt"
input2 = "data/week01/D_01/zoey/zoey__130319_1208_D_01.txt"
stripe_list1 = get_stripes(get_data_file(input1))
stripe_list2 = get_stripes(get_data_file(input2))

print("In Dubby picture: ")
print()

print("Total geometric length of Aliza: " + "%.3f" % calc_file_dist(stripe_list1)[0] + "cm")
print("Average geometric length of Aliza per stripe: " + "%.3f" % calc_dist_average_of_stripe(stripe_list1) + "cm")
print("Total time of Aliza: " + "%.3f" % calc_file_time(stripe_list1) + "sec")
print("Total waiting time of Aliza: " + "%.3f" % calc_waiting_time(stripe_list1) + "sec")
print("Average time of Aliza per stripe: " + "%.3f" % calc_time_average_of_stripe(stripe_list1) + "sec")
print("Average speed of Aliza: " + "%.3f" % calc_average_speed_in_file(stripe_list1) + "cm/sec")

print()

print("Total geometric length of Zoey: " + "%.3f" % calc_file_dist(stripe_list2)[0] + "cm")
print("Average Geometric length of Zoey per stripe: " + "%.3f" % calc_dist_average_of_stripe(stripe_list2) + "cm")
print("Total time of Zoey: " + "%.3f" % calc_file_time(stripe_list2) + "sec")
print("Total waiting time of Zoey: " + "%.3f" % calc_waiting_time(stripe_list2) + "sec")
print("Average time of Zoey per stripe: " + "%.3f" % calc_time_average_of_stripe(stripe_list2) + "sec")
print("Average speed of Zoey: " + "%.3f" % calc_average_speed_in_file(stripe_list2) + "cm/sec")

