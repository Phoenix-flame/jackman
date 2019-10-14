# Informed search algorithm

from threading import Thread
import numpy as np
import operator
import time
from tabulate import tabulate
from source.state import *
from source.direction import *


class Astar(Thread):
    def __init__(self, _map):
        super().__init__()
        self.map = _map
        self.startPoint = None
        self.target = None
        self.path = []


        # Performance measure
        self.cost_to_path = 0
        self.nodes_expanded = 0
        self.fringe_size = 0
        self.max_fringe_size = 0
        self.search_depth = 0
        self.max_search_depth = 0


    def run(self):
        print("Let's rock")

        # Preparation
        frontier = deque([])
        visited = set()
        self.createInitState(frontier)
        g_val = 0

        # Let's rock
        tic = time.time()
        if self._astar(frontier, visited, g_val):
            self.getPath()
            toc = time.time()
            self.show_performance(toc - tic)
            self.showResult()  # It will be deprecated in final version
        else:
            print("There is no path :(")


    def _astar(self, frontier, visited, g_val):
        curNode = frontier.popleft()

        if curNode.result == 0:
            self.target = curNode
            # DON'T touch it
            self.search_depth = curNode.depth
            return True

        visited.add(curNode)

        # DON'T touch this
        children = self.getAdjacents(curNode)
        self.nodes_expanded += 1

        for child in children:
            if child not in visited:
                child.f_val = (self.heuristic(child)) + g_val
                visited.add(child)
                frontier.append(child)
                if child.depth > self.max_search_depth:
                    self.max_search_depth += 1

        if len(frontier) == 0:
            return False

        frontier = deque(sorted(frontier, key=operator.attrgetter('f_val')))
        g_val += 1

        # DON'T touch it
        if len(frontier) > self.max_fringe_size:
            self.max_fringe_size = len(frontier)

        return self._astar(frontier, visited, g_val)




    def heuristic(self, state):
        p_cell = state.p
        q_cell = state.q

        result = state.result

        sum_dist_p = 0
        sum_dist_q = 0

        for f1 in self.map.food1:
            if f1 in state.foods:
                continue
            sum_dist_p += self.EuclideanDist(self.map.getCell(f1), p_cell)
        for f2 in self.map.food2:
            if f2 in state.foods:
                continue
            sum_dist_q += self.EuclideanDist(self.map.getCell(f2), q_cell)
        for f3 in self.map.food3:
            if f3 in state.foods:
                continue
            sum_dist_p += self.EuclideanDist(self.map.getCell(f3), p_cell)
            sum_dist_q += self.EuclideanDist(self.map.getCell(f3), q_cell)

        dist_overall = sum_dist_p + sum_dist_q

        return np.exp(dist_overall) ** result

    @staticmethod
    def EuclideanDist(p1, p2):
        return np.sqrt(np.power(p1.x - p2.x, 2) + np.power(p1.y - p2.y, 2))

    @staticmethod
    def ManhatanDist(p1, p2):
        return np.abs(p1.x - p2.x) + np.abs(p1.y - p2.y)


    # Adjacents of current state -> State
    def getAdjacents(self, curState):
        res = deque([])
        p = curState.p
        q = curState.q

        # Possible adjacents for each agent
        p_adj = self.getAdjacentsCell(p)
        q_adj = self.getAdjacentsCell(q)

        # Create states by combining adjacents
        # each adjacent consists of a cell and a dir:
        for i in p_adj:
            for j in q_adj:
                p_dir, q_dir = i['dir'], j['dir']
                p_cell, q_cell = i['cell'], j['cell']
                if p_dir != Direction.NO and q_dir != Direction.NO:
                    continue
                if q_cell.getType() == '1' and q_cell.getKey() not in curState.foods:
                    continue
                if p_cell.getType() == '2' and p_cell.getKey() not in curState.foods:
                    continue
                score = 0
                unseen_foods = deque([])
                if p_cell != q_cell:
                    if p_cell.getKey() not in curState.foods and (p_cell.getType() == '1' or p_cell.getType() == '3'):
                        unseen_foods.append(p_cell.getKey())
                        score += 1
                    if q_cell.getKey() not in curState.foods and (q_cell.getType() == '2' or q_cell.getType() == '3'):
                        unseen_foods.append(q_cell.getKey())
                        score += 1
                    # p, q, p_action, q_action, res, parent, depth, foods=None):
                    res.append(State(p_cell, q_cell,
                                       p_dir, q_dir,
                                       curState.result - score,
                                       curState,
                                       curState.depth + 1,
                                       curState.foods + unseen_foods))
                else:
                    continue
        return res


    # Adjacents of current cell -> Cell
    def getAdjacentsCell(self, curCell):
        res = []
        for d in Direction:
            nextCell = self.getNextCell(curCell, d)
            if nextCell is None:
                continue
            if nextCell.getType() == '%':
                continue
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


    # Finding optimal path by traversing over parents of target
    def getPath(self):
        result = []
        parent = self.target
        result.append(parent)
        while parent != self.startPoint:
            parent = parent.parent
            result.append(parent)
        result.reverse()
        self.path = result


    # This function will be deprecated in final version
    def showResult(self):
        for i in range(len(self.path)):
            if i == 0:
                continue
            p_old, q_old = self.path[i - 1].p, self.path[i - 1].q
            p_new, q_new = self.path[i].p, self.path[i].q
            p_old.changeType(' ')
            q_old.changeType(' ')
            p_new.changeType('P')
            q_new.changeType('Q')
            time.sleep(0.2)


    # Initiating very first state of the problem
    def createInitState(self, frontier):
        p = self.map.getCell(self.map.p)
        q = self.map.getCell(self.map.q)
        frontier.append(State(p, q, None, None, len(self.map), None, 0))
        frontier[0].f_val = self.heuristic(frontier[0])
        self.startPoint = frontier[0]

    def show_performance(self, _time):
        print(tabulate([['Nodes expanded', self.nodes_expanded],
                        ['Max search depth', self.max_search_depth],
                        ['Search depth', self.search_depth],
                        ['Max fringe size', self.max_fringe_size],
                        ['Time', _time]], headers=['Parameter', 'Value']))
