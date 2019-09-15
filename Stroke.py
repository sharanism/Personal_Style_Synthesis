import numpy as np
import math


class Stroke:
    def __init__(self, data):
        """
        :param data: dictionary. keys are the features (time, x, y ,...) and their values.
        """
        self._data = data

    def get_data(self):
        """
        :return: dictionary. keys are the features (time, x, y ,...) and their values.
        """
        return self._data

    def size(self):
        """
        :return: number of stamps in a stroke
        """
        return len(self._data['time'])

    def time(self):
        """
        :return: numpy array of time values of the stroke
        """
        return self._string2float_array(self._data['time'])

    def x(self):
        """
        :return: numpy array of x values of the stroke, in case of pause-stroke, fill -1
        """
        return self._string2float_array(self._data['x'])

    def y(self):
        """
        :return: numpy array of y values of the stroke, in case of pause-stroke, fill -1
        """
        return self._string2float_array(self._data['y'])

    def pressure(self):
        """
        :return: numpy array of pressure values of the stroke, in case of pause-stroke, fill 0
        """
        return self._string2float_array(self._data['pressure'])

    def tiltX(self):
        """
        :return: numpy array of tiltX values of the stroke, in case of pause-stroke, fill -1
        """
        return self._string2float_array(self._data['tiltX'])

    def tiltY(self):
        """
        :return: numpy array of tiltY values of the stroke, in case of pause-stroke, fill -1
        """
        return self._string2float_array(self._data['tiltY'])

    def azimuth(self):
        """
        :return: numpy array of azimuth values of the stroke, in case of pause-stroke, fill -1
        """
        return self._string2float_array(self._data['azimuth'])

    def sidePressure(self):
        """
        :return: numpy array of sidePressure values of the stroke, in case of pause-stroke, fill -1
        """
        return self._string2float_array(self._data['sidePressure'])

    def rotation(self):
        """
        :return: numpy array of rotation values of the stroke, in case of pause-stroke, fill -1
        """
        return self._string2float_array(self._data['rotation'])

    def total_length(self):
        """
        :return: the total geometric length of a stroke (unit -> pixel)
        """
        x_array = self.x()
        y_array = self.y()
        dist = 0.0
        for i in range(1, len(x_array)):
            dist += self.calc_dist_2D(x_array[i - 1], x_array[i], y_array[i - 1], y_array[i])

        return dist

    def total_time(self):
        """
        :return: the total time of a stroke
        """
        time_array = self.time()
        time = 0.0
        for i in range(1, len(time_array)):
            time += (time_array[i] - time_array[i-1])

        return time

    def average_speed(self):
        """
        :return: the average speed of a stroke
        """
        return self.total_length() / self.total_time()

    def average_pressure(self):
        """
        :return: average pressure of the stroke
        """
        return self.pressure().mean()

    def average_tiltX(self):
        """
        :return: average tiltX of the stroke
        """
        return self.tiltX().mean()

    def average_tiltY(self):
        """
        :return: average tiltY of the stroke
        """
        return self.tiltY().mean()

    def average_azimuth(self):
        """
        :return: average azimuth of the stroke
        """
        return self.azimuth().mean()

    def average_sidePressure(self):
        """
        :return: average sidePressure of the stroke
        """
        return self.sidePressure().mean()

    def average_rotation(self):
        """
        :return: average rotation of the stroke
        """
        return self.rotation().mean()

    @staticmethod
    def calc_dist_2D(old_x, new_x, old_y, new_y):
        """
        :return: the distance between two points - 2D
        """
        return math.sqrt(float(pow(new_x - old_x, 2)) + float(pow(new_y - old_y, 2)))

    @staticmethod
    def _string2float_array(string_array):
        """
        :param string_array: array with numbers represents by strings
        :return: numpy array with float values instead of strings
        """
        array = []
        for value in string_array:
            array.append(float(value))
        return np.asarray(array)
