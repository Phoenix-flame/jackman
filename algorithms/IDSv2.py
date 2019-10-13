# Uninformed search algorithm

from threading import Thread
import time
from tabulate import tabulate
from enum import Enum
from source.state import *
import copy


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    NO = 5

class IDSv2(Thread):
    def __init__(self, _map):
        super().__init__()
        self.map = _map

        # Performance measure
        self.cost_to_path = 0
        self.nodes_expanded = 0
        self.fringe_size = 0
        self.max_fringe_size = 0
        self.search_depth = 0
        self.max_search_depth = 0

        self.target = None

    def run(self):
        tic = time.time()

        p = self.map.getCell(self.map.p)
        q = self.map.getCell(self.map.q)
        startPoint = Statev2(p, q, None, None, len(self.map), None, 0)

        if self._ids(100):
            print()
            parent = self.target
            while parent != startPoint:
                print(parent)
                parent = parent.parent
            print("Done")
        else:
            print("There is no path :(")

        toc = time.time()
        self.show_performance(toc - tic)

    def _ids(self, maxDepth):

        for i in range(maxDepth):
            visited = []
            frontier = []
            p = self.map.getCell(self.map.p)
            q = self.map.getCell(self.map.q)
            frontier.append(Statev2(p, q, None, None, len(self.map), None, 0))


            if self._dfs(visited, frontier, i):
                return True
        return False


    def _dfs(self, visited, frontier, maxDepth):
        if len(frontier) == 0:
            return False
        curNode = frontier[-1]
        del frontier[-1]
        print(curNode.result)
        if curNode.result == 0:
            self.target = curNode
            self.search_depth = curNode.depth
            return True


        # time.sleep(0.01)

        if maxDepth <= 0:
            return False

        visited.append(curNode)

        # DON'T touch this
        children = reversed(self.getAdjacents(curNode))
        self.nodes_expanded += 1


        for child in children:
            if child not in visited:
                visited.append(child)
                frontier.append(child)
                if self._dfs(visited, frontier, maxDepth - 1):
                    return True

        return False






    # Adherents of current state -> State
    def getAdjacents(self, curState):
        res = []
        p = curState.p
        q = curState.q

        # Possible adjacents for each agent
        p_adj = self.getAdjacentsCell(p, 'P')
        q_adj = self.getAdjacentsCell(q, 'Q')

        # Create states by combining adjacents
        # each adjacent consists of a cell and a dir:
        for i in p_adj:
            for j in q_adj:
                score = 0
                unseen_foods = []
                if i['cell'] != j['cell']:
                    p_dir, q_dir = i['dir'], j['dir']
                    p_cell, q_cell = i['cell'], j['cell']
                    if p_cell.getKey() not in curState.foods and (p_cell.getType() == '1' or p_cell.getType() == '3'):
                        unseen_foods.append(p_cell.getKey())
                        score += 1
                    if q_cell.getKey() not in curState.foods and (q_cell.getType() == '2' or q_cell.getType() == '3'):
                        unseen_foods.append(q_cell.getKey())
                        score += 1
                    # p, q, p_action, q_action, res, parent, depth, foods=None):
                    res.append(Statev2(p_cell, q_cell,
                                       p_dir, q_dir,
                                       curState.result - score,
                                       curState,
                                       curState.depth + 1,
                                       curState.foods + unseen_foods))


                else:
                    continue
        return res


    # Adjacents of current cell -> Cell
    def getAdjacentsCell(self, curCell, player):
        res = []
        for d in Direction:
            nextCell = self.getNextCell(curCell, d)
            if nextCell.getType() == '%':
                continue
            if player == 'P' and nextCell and nextCell.getType() != '2':
                res.append({'cell': nextCell, 'dir': d})
            elif player == 'Q' and nextCell and nextCell.getType() != '1':
                res.append({'cell': nextCell, 'dir': d})
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



    def show_performance(self, _time):
        print(tabulate([['Nodes expanded', self.nodes_expanded],
                        ['Max search depth', self.max_search_depth],
                        ['Search depth', self.search_depth],
                        ['Max fringe size', self.max_fringe_size],
                        ['Time', _time]], headers=['Parameter', 'Value']))
