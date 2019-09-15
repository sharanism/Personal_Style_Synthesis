from Analyzer import Analyzer
import os


class Participant:

    def __init__(self, name):
        self._name = name
        self._data = self.get_all_files_of_participant()

    def get_all_files_of_participant(self):
        """
        :return: 2D list, include data of the file (DataFrame) and path to reference picture
        """
        lst = []
        path = None
        for picture in os.listdir("data"):
            if "DS_Store" not in picture:
                for person in os.listdir("data/" + picture):
                    if "DS_Store" not in person:
                        if person == self._name:
                            for file in os.listdir("data/" + picture + "/" + person):
                                if "DS_Store" not in file:
                                    if file.endswith(".txt"):
                                        path = "data/" + picture + "/" + person + "/" + file
                            if path is not None:
                                drawing = Analyzer.create_drawing(path)
                                if drawing is not None:
                                    lst.append(drawing)

        return lst

    def plot_participant_pictures(self):
        for drawing in self._data:
            drawing.plot_picture()

