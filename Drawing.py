import numpy as np
import copy
from Stroke import Stroke
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


class Drawing:
    def __init__(self, data, pic_path, ref_path):
        """
        :param data: list of Strokes objects
        """
        self._data = data
        self._ref_path = ref_path
        self._pic_path = pic_path

    def get_ref_path(self):
        return self._ref_path

    def get_pic_path(self):
        return self._pic_path

    def get_data(self):
        """
        :return: list of Stroke objects
        """
        return self._data

    def size(self):
        """
        :return: number of stroke in the file
        """
        return len(self._data)

    def total_length(self):
        """
        :return: first value is the total geometric length of a file (unit -> pixel),
                 second value is array of all the strokes lengths
        """
        dist = 0.0
        arr = []
        for stroke in self._data:
            arr.append(stroke.total_length())
            dist += stroke.total_length()

        return dist, np.asarray(arr)

    def average_length_of_stroke(self):
        """
        :return: average of geometric length of a single stroke
        """
        return self.total_length()[0] / float(self.size())

    def length_std(self):
        """
        :return: std of the geometric length of the strokes
        """
        return self.total_length()[1].std()

    def active_time(self):
        """
        :return: total active time (without pauses time)
        """
        return self._data[-1].time()[-1]

    def get_strokes_as_one(self):
        """
        @TODO - this is not efficient implements
        :return: all the strokes in the file, merged into one stroke, without pauses
        """
        stroke_list = []
        for stroke in self._data:
            stroke_list.append(stroke.get_data())

        stroke_list_copy = copy.deepcopy(stroke_list)
        for stroke in stroke_list_copy:
            for feature in stroke.keys():
                stroke[feature] = list(stroke[feature])

        for key, value in stroke_list_copy[0].items():
            for i in range(1, len(stroke_list_copy)):
                value.extend(stroke_list_copy[i][key])
        return Stroke(stroke_list_copy[0])

    def speed_vs_time(self):
        """
        plot graph of speed vs time
        """
        time = []
        speed = []
        for stroke in self.get_data():
            time.append(stroke.time()[0])
            speed.append(stroke.average_speed())

        time = np.asarray(time)
        speed = np.asarray(speed)
        plt.scatter(time, speed, s=2)
        plt.title("speed mean is: " + str(speed.mean()) + "\nspeed std is: " + str(speed.std()))
        plt.xlabel('time [sec]')
        plt.ylabel('speed [pixel/sec]')
        plt.show()

    def pressure_vs_time(self):
        """
        plot graph of speed vs time
        """
        time = []
        pressure = []
        for stroke in self.get_data():
            time.append(stroke.time()[0])
            pressure.append(stroke.average_pressure())

        time = np.asarray(time)
        pressure = np.asarray(pressure)
        plt.scatter(time, pressure, s=2)
        plt.title("pressure mean is: " + str(pressure.mean()) + "\npressure std is: " + str(pressure.std()))
        plt.xlabel('time [sec]')
        plt.ylabel('pressure [?]')
        plt.show()

    def length_vs_time(self):
        """
        plot graph of speed vs time
        """
        time = []
        length = []
        for stroke in self.get_data():
            time.append(stroke.time()[0])
            length.append(stroke.total_length())

        time = np.asarray(time)
        length = np.asarray(length)
        plt.scatter(time, length, s=2)
        plt.title("length mean is: " + str(length.mean()) + "\nlength std is: " + str(length.std()))
        plt.xlabel('time [sec]')
        plt.ylabel('length [pixel]')
        plt.show()

    def plot_picture(self):
        """
        @TODO - rotate
        """
        # one_stroke = self.get_strokes_as_one()
        #
        # plt.subplot(1, 3, 1)
        # plt.scatter(one_stroke.x(), one_stroke.y(), s=0.5,)
        if self._ref_path == "ref_pics/D12":
            return

        plt.subplot(1, 2, 1)
        plt.imshow(mpimg.imread(self._pic_path))

        plt.subplot(1, 2, 2)
        plt.imshow(mpimg.imread(self._ref_path))

        plt.show()


