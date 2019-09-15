import pandas as pd
from Stroke import Stroke
from File import File


class Analyzer:
    MIN_SIZE_OF_STROKE = 2
    TIME_STAMP = 0.017

    @staticmethod
    def get_data_file(path):
        """
        :param path: string
        :return: DataFrame object
        """
        return pd.read_csv(path, delimiter='\t')

    @staticmethod
    def get_file(data):
        """
        :param data: DataFrame object
        :return: new File object that represent the data
        """
        stroke_list = []
        stroke = dict()
        start_stroke_location = 0  # the location of the next stroke in data
        current_time = 0.0

        for i, time in enumerate(data['time']):
            if time == 'Pause':
                if i - start_stroke_location < Analyzer.MIN_SIZE_OF_STROKE:  # MIN_SIZE_OF_STROKE = 2
                    start_stroke_location = i + 1
                    continue

                for feature in data:
                    stroke[feature] = data[feature][start_stroke_location:i]
                    if feature == 'time':
                        for j in range(start_stroke_location, i):
                            stroke['time'][j] = current_time
                            current_time += Analyzer.TIME_STAMP  # TIME_STAMP = 0.017

                start_stroke_location = i + 1
                stroke_list.append(Stroke(stroke))
                stroke = dict()

        return File(stroke_list)


if __name__ == "__main__":
    input1 = "data/D_01/aliza/aliza__130319_0935_D_01.txt"
    input2 = "data/D_01/zoey/zoey__130319_1208_D_01.txt"

    # b = Analyzer.get_file(Analyzer.get_data_file(input2))
    # a = Analyzer.get_file(Analyzer.get_data_file(input1))
    # a_one = a.get_strokes_as_one()
    from Person import Person
    person = Person("aliza")
    person.plot_all_person_pictures()
