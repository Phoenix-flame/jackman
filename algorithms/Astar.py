# Informed search algorithm

from threading import Thread
import numpy as np
import time

class Astar(Thread):
    def __init__(self, _map, _start, _target):
        super().__init__()
        self.startPoint = _start
        self.target = _target
        self.map = _map


    def run(self):
        print("Let's rock")
        frontier = {}
        visited = []
        path = []
        g_val = 0
        frontier[self.EuclideanDist(self.startPoint, self.target)] = self.startPoint
        self._astar(self.startPoint, frontier, visited, path, self.target, g_val)
        print("ok")

    def _astar(self, curNode, frontier, visited, path, target, g_val):
        if len(frontier) == 0:
            return False
        if curNode == target:
            print(curNode)
            return True


        time.sleep(0.5)

        visited.append(curNode)
        children = self.map.getAdjacents(curNode)
        for child in children:
            if child not in visited:
                visited.append(child)
                print(g_val + self.EuclideanDist(child, target))
                frontier[g_val + self.EuclideanDist(child, target)] = child


        g_val += 1


        node = frontier[min(frontier.keys())]
        del frontier[min(frontier.keys())]
        node.changeType('*')
        return self._astar(node, frontier, visited, path, target, g_val)



    @staticmethod
    def EuclideanDist(p1, p2):
        return np.sqrt(np.power(p1.x - p2.x, 2) + np.power(p1.y - p2.y, 2)) * 10

    @staticmethod
    def ManhatanDist(p1, p2):
        return np.abs(p1.x - p2.x) + np.abs(p1.y - p2.y)

