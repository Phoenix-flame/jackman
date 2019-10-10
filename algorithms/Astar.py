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
        path = {}
        g_val = 0
        frontier[self.startPoint] = self.EuclideanDist(self.startPoint, self.target)
        self._astar(self.startPoint, frontier, visited, path, self.target, g_val)

        res = [self.target]
        parent = path[self.target]
        while parent != self.startPoint:
            res.append(parent)
            cur = parent
            parent = path[cur]
        res.append(parent)

        for i in res:
            i.changeType('2')
            print(i)
        print("Done")

    def _astar(self, curNode, frontier, visited, path, target, g_val):
        g_val_tmp = g_val
        if len(frontier) == 0:
            return False
        if curNode == target:
            print(curNode)
            return True
        #
        time.sleep(0.01)

        visited.append(curNode)
        children = self.map.getAdjacents(curNode)
        for child in children:
            if child not in visited:
                visited.append(child)
                path[child] = curNode
                frontier[child] = g_val_tmp + self.EuclideanDist(child, target)

        print(frontier.values())

        node = list(frontier.keys())[list(frontier.values()).index(min(frontier.values()))]
        print("g:", g_val, "h:", self.EuclideanDist(node, target), node)
        del frontier[node]
        node.changeType('*')
        g_val += 10
        return self._astar(node, frontier, visited, path, target, g_val)



    @staticmethod
    def EuclideanDist(p1, p2):
        return np.sqrt(np.power(p1.x - p2.x, 2) + np.power(p1.y - p2.y, 2))

    @staticmethod
    def ManhatanDist(p1, p2):
        return np.abs(p1.x - p2.x) + np.abs(p1.y - p2.y)

