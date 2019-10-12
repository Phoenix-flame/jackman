# Uninformed search algorithm

from threading import Thread
import time
from source.state import *
from tabulate import tabulate
from enum import Enum


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    NO = 5


class BFSv2(Thread):
    def __init__(self, _map):
        super().__init__()
        self.map = _map
        self.res = None

        # Performance measure
        self.cost_to_path = 0
        self.nodes_expanded = 0
        self.fringe_size = 0
        self.max_fringe_size = 0
        self.search_depth = 0
        self.max_search_depth = 0

        self.food1 = []
        self.food2 = []
        self.food3 = []

        self.target = None

    def run(self):
        tic = time.time()
        visited = []
        frontier = []
        p = self.map.getCell(self.map.p)
        q = self.map.getCell(self.map.q)

        frontier.append(Statev2(p, q, None, None, len(self.map), None, 0))
        startPoint = frontier[0]
        if self._bfs(visited, frontier):
            parent = self.target
            while parent != startPoint:
                print(parent)
                parent = parent.parent
            print("Done")
        else:
            print("There is no path :(")
        toc = time.time()
        self.show_performance(toc - tic)










    def _bfs(self, visited, frontier):
        if len(frontier) == 0:
            return False
        curNode = frontier[0]
        del frontier[0]

        if curNode.result == 0:
            self.target = curNode
            self.search_depth = curNode.depth
            return True

        visited.append(curNode)

        # time.sleep(0.05)
        children = self.getAdjacents(curNode)
        self.nodes_expanded += 1

        for child in children:
            if child not in visited:
                frontier.append(child)
                visited.append(child)
                # path[child] = curNode
                if child.depth > self.max_search_depth:
                    self.max_search_depth += 1
        return self._bfs(visited, frontier)












    def getAdjacents(self, curState):
        p = curState.p
        q = curState.q
        p_adj, food1 = self.getAdjacentsCell(p, 'P')
        q_adj, food2 = self.getAdjacentsCell(q, 'Q')
        food = food1 + food2
        res = []
        for i in p_adj:
            for j in q_adj:
                if j[2] == -1 or j[2] == -1:
                    if j[0] not in curState.food and i[0] not in curState.food:
                        res.append(Statev2(i[0], j[0],  # Nodes
                                           i[1], j[1],  # Actions
                                           curState.result + i[2] + j[2],  # total number of foods
                                           curState,  # parent
                                           curState.depth + 1,
                                           food=food))  # depth
                    elif j[0] not in curState.food and i[0] in curState.food:
                        res.append(Statev2(i[0], j[0],  # Nodes
                                           i[1], j[1],  # Actions
                                           curState.result + j[2],  # total number of foods
                                           curState,  # parent
                                           curState.depth + 1,
                                           food=food))  # depth
                    elif i[0] not in curState.food and j[0] in curState.food:
                        res.append(Statev2(i[0], j[0],  # Nodes
                                           i[1], j[1],  # Actions
                                           curState.result + i[2],  # total number of foods
                                           curState,  # parent
                                           curState.depth + 1,
                                           food=food))  # depth
                else:
                    res.append(Statev2(i[0], j[0],  # Nodes
                                       i[1], j[1],  # Actions
                                       curState.result,  # total number of foods
                                       curState,  # parent
                                       curState.depth + 1,
                                       food=food))  # depth

        return res

    def getNextCell(self, curCell, direction):
        _x = curCell.x
        _y = curCell.y
        if direction == Direction.UP:
            try:
                return self.map.map[(_x, _y - 1)]
            except KeyError:
                return None
        elif direction == Direction.DOWN:
            try:
                return self.map.map[(_x, _y + 1)]
            except KeyError:
                return None
        elif direction == Direction.RIGHT:
            try:
                return self.map.map[(_x + 1, _y)]
            except KeyError:
                return None
        elif direction == Direction.LEFT:
            try:
                return self.map.map[(_x - 1, _y)]
            except KeyError:
                return None
        elif direction == Direction.NO:
            try:
                return self.map.map[(_x, _y)]
            except KeyError:
                return None

    def getAdjacentsCell(self, curCell, player):
        result = []
        foods = []
        for d in Direction:
            nextCell = self.getNextCell(curCell, d)
            if nextCell is not None:
                if nextCell.getType() is not '%':
                    if player == 'P':
                        if nextCell.getType() != 'Q' and nextCell.getType() != '2':
                            if nextCell.getType() == '1' or nextCell.getType() == '3':
                                result.append([nextCell, d, -1])
                                foods.append(nextCell)
                            else:
                                result.append([nextCell, d, 0])
                    elif player == 'Q':
                        if nextCell.getType() != 'P' and nextCell.getType() != '1':
                            if nextCell.getType() == '2' or nextCell.getType() == '3':
                                result.append([nextCell, d, -1])
                                foods.append(nextCell)
                            else:
                                result.append([nextCell, d, 0])
        return result, foods

    def show_performance(self, _time):
        print(tabulate([['Nodes expanded', self.nodes_expanded],
                        ['Max search depth', self.max_search_depth],
                        ['Search depth', self.search_depth],
                        ['Max fringe size', self.max_fringe_size],
                        ['Time', _time]], headers=['Parameter', 'Value']))
