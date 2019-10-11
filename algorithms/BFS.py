# Uninformed search algorithm

from threading import Thread
import time
from source.state import *
from tabulate import tabulate

class BFS(Thread):
    def __init__(self, _map, _start, _target):
        super().__init__()
        self.map = _map
        self.startPoint = _start
        self.target = _target
        self.map = _map
        self.res = None

        # Performance measure
        self.cost_to_path = 0
        self.nodes_expanded = 0
        self.fringe_size = 0
        self.max_fringe_size = 0
        self.search_depth = 0
        self.max_search_depth = 0


    def run(self):
        tic = time.time()
        visited = []
        frontier = []
        path = {}
        frontier.append(State(self.startPoint, None, 0))
        if self._bfs(visited, frontier, path, self.target):
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
            print("Done")
            self.res = res
        else:

            print("There is no path :(")

        toc = time.time()
        self.show_performance(toc - tic)


    def _bfs(self, visited, frontier, path, target):

        if len(frontier) == 0:
            return False
        curNode = frontier[0]
        del frontier[0]
        # print(len(frontier), curNode.node)


        if curNode.node == target:
            self.search_depth = curNode.depth
            return True

        visited.append(curNode)
        if curNode.node.cellType == ' ':
            curNode.node.changeType('*')

        # time.sleep(0.05)
        children = self.map.getAdjacents(curNode.node, 'P')
        self.nodes_expanded += 1


        for child in children:
            child = State(child, curNode.node, curNode.depth + 1)
            if child.node not in visited:
                frontier.append(child)
                visited.append(child.node)
                path[child.node] = curNode.node
                if child.depth > self.max_search_depth:
                    self.max_search_depth += 1

        return self._bfs(visited, frontier, path, target)


    def show_performance(self, _time):
        print(tabulate([['Nodes expanded', self.nodes_expanded],
                        ['Max search depth', self.max_search_depth],
                        ['Search depth', self.search_depth],
                        ['Time', _time]], headers=['Parameter', 'Value']))
        # print('Nodes expanded:', self.nodes_expanded)
        # print('Max search depth:', self.max_search_depth)
        # print('Search depth:', self.search_depth)

