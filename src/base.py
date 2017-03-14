import os
import math


class Base:
    def __init__(self):
        pass

    yield_dir = "../yld_data"
    weather_dir = "../wx_data"
    answers_dir = "../answers"

    def run_problem(self, problem):
        # Collect list of all weather files
        weather_station_files = os.listdir(self.weather_dir)

        # Sort the files acceding
        weather_station_files.sort()

        results = {}

        problem(self, results, weather_station_files)

    def average(self, x):
        assert len(x) > 0
        return float(sum(x)) / len(x)

    def pearson_def(self, x, y):
        assert len(x) == len(y)
        n = len(x)
        assert n > 0
        avg_x = self.average(x)
        avg_y = self.average(y)
        diffprod = 0
        xdiff2 = 0
        ydiff2 = 0
        for idx in range(n):
            xdiff = x[idx] - avg_x
            ydiff = y[idx] - avg_y
            diffprod += xdiff * ydiff
            xdiff2 += xdiff * xdiff
            ydiff2 += ydiff * ydiff

        return diffprod / math.sqrt(xdiff2 * ydiff2)
