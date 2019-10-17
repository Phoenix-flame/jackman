
from matplotlib import pyplot as plt
import os

from source.map import *
from algorithms.AStar import *
from algorithms.BFS import *
from algorithms.IDS import *



class Game:
    def __init__(self):
        super().__init__()
        self.map = Map("testcases/test5")
        self.__stopped = False
        self.started_algorithm = False

    def run(self):
        time = 0
        self.started_algorithm = True
        for i in range(3):
            tmp = BFS(self.map)
            tmp.run()
            time += tmp.time
        print(time / 3.0)

    def runPlot(self):
        times = []
        dists = []

        path = './testcases'
        testCases = os.listdir(path)
        name = ""
        for i in testCases:
            self.map = Map(path + '/' + i)
            tmp = BFS(self.map)
            name = tmp.name
            tmp.run()
            times.append(tmp.time)
            dists.append(tmp.distance)

        plt.scatter(dists, times)
        plt.title(name)
        plt.xlabel("Distance")
        plt.ylabel("Time")
        plt.show()
