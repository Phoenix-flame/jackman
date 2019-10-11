# Informed search algorithm

from threading import Thread
import numpy as np
import operator
import time

class Astar(Thread):
    def __init__(self, _map, _start, _target):
        super().__init__()
        self.startPoint = _start
        self.target = _target
        self.map = _map


    def run(self):
        print("Let's rock")
        frontier = []
        visited = []
        path = {}
        g_val = 0
        self.startPoint.f = self.EuclideanDist(self.startPoint, self.target)
        self.startPoint.h = self.startPoint.f

        frontier.append(self.startPoint)
        if self._astar(self.startPoint, frontier, visited, path, self.target, g_val):

            res = [self.target]
            parent = path[self.target]
            while parent != self.startPoint:
                res.append(parent)
                cur = parent
                parent = path[cur]
            res.append(parent)

            for i in res:
                if i.cellType == '*':
                    i.changeType('Q')
                # print(i)
            print("Done")
        else:
            print("There is no path :(")

    def _astar(self, curNode, frontier, visited, path, target, g_val):
        if curNode == target:
            return True

        time.sleep(0.01)

        visited.append(curNode)
        if curNode.cellType == ' ':
            curNode.changeType('*')


        children = self.map.getAdjacents(curNode, 'P')
        for child in children:
            if child not in visited:
                visited.append(child)
                path[child] = curNode
                child.f = g_val + (self.EuclideanDist(child, target))
                child.g = g_val
                child.h = self.EuclideanDist(child, target)
                frontier.append(child)

        if len(frontier) == 0:
            return False

        frontier = sorted(frontier, key=operator.attrgetter('f'))
        g_val += 10

        node = frontier[0]
        del frontier[0]
        return self._astar(node, frontier, visited, path, target, g_val)




    @staticmethod
    def EuclideanDist(p1, p2):
        return np.sqrt(np.power(p1.x - p2.x, 2) + np.power(p1.y - p2.y, 2))

    @staticmethod
    def ManhatanDist(p1, p2):
        return np.abs(p1.x - p2.x) + np.abs(p1.y - p2.y)

