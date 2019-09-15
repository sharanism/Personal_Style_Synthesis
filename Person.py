from Analyzer import Analyzer
import os
import matplotlib.image as mpimg
import matplotlib.pyplot as plt


class Person:

    def __init__(self, name):
        self._name = name

    def get_all_files_of_person(self):
        """
        :return: 2D list, include data of the file (DataFrame) and path to reference picture
        """
        lst = []
        data = None
        path = None
        for picture in os.listdir("data"):
            if "DS_Store" not in picture:
                for person in os.listdir("data/" + picture):
                    if "DS_Store" not in person:
                        if person == self._name:
                            for file in os.listdir("data/" + picture + "/" + person):
                                if "DS_Store" not in file:
                                    if file.endswith(".txt"):
                                        data = Analyzer.get_data_file("data/" + picture + "/" + person + "/" + file)
                                    elif file.endswith(".png"):
                                        path = "data/" + picture + "/" + person + "/" + file
                            if path is not None and data is not None:
                                lst.append([Analyzer.get_file(data), path])
        return lst

    @staticmethod
    def plot_pic_and_ref(file):
        """
        :param file: contains File object, and path to picture and ref of this file (for this person)
        """
        one_stroke = file[0].get_strokes_as_one()

        plt.subplot(1, 2, 1)
        plt.scatter(one_stroke.x(), one_stroke.y(), s=0.5,)

        plt.subplot(1, 2, 2)
        plt.imshow(mpimg.imread(file[1]))

        plt.show()

    def plot_all_person_pictures(self):
        all_file = self.get_all_files_of_person()
        for i, file in enumerate(all_file):
            Person.plot_pic_and_ref(file)

