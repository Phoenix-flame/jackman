# Informed search algorithm

from threading import Thread
import numpy as np
import operator
import time
from tabulate import tabulate
from heapq import heapify, heappop, heappush

from source.state import *
from source.direction import *


class Astar(Thread):
    def __init__(self, _map):
        super().__init__()
        print("This is A*")
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
        self.time = 0

    def run(self):
        print("Let's rock")

        # Preparation
        frontier = []

        visited = set()
        self.createInitState(frontier)
        g_val = 0


        # Let's rock
        tic = time.time()

        came_from, cost_so_far = self.astar2()



        print('ok')
        print(self.target.parent)
        # for i in came_from:
        #     print(i)
        self.getPath()
        toc = time.time()
        self.show_performance(toc - tic)
        self.showResult()

        # if self._astar(frontier, visited, g_val):
        #     self.getPath()
        #     toc = time.time()
        #     self.show_performance(toc - tic)
        #     self.showResult()  # It will be deprecated in final version
        # else:
        #     print("There is no path :(")


    def _astar(self, frontier, visited, g_val):

        heapify(frontier)
        heap_entry = {self.startPoint.__hash__(): (self.startPoint, 0)}
        visited = set()
        visited.add(self.startPoint)
        while frontier.__len__():
            curNode = heappop(frontier)
            if curNode.result == 0:
                self.target = curNode
                return True

            children = self.getAdjacents(curNode)
            self.nodes_expanded += 1


            for child in children:
                child.f_val = g_val + self.heuristic(child)

                if child not in visited:
                    heappush(frontier, child)
                    visited.add(child)
                    heap_entry[child.__hash__()] = (child, child.f_val)

                # elif child in visited:
                #
                #     if child.f_val < heap_entry[child.__hash__()][1]:
                #         tmp = heap_entry[child.__hash__()][0]
                #         print(child.f_val, tmp.f_val)
                #         hindex = frontier.index(tmp)
                #         frontier[hindex] = child
                #         heap_entry[child.__hash__()] = (child, child.f_val)
                #
                #         heapify(frontier)

            g_val += 1

    def astar2(self):
        frontier = [self.startPoint]
        heapify(frontier)
        came_from = {}
        cost_so_far = {}
        came_from[self.startPoint] = None
        cost_so_far[self.startPoint] = 0

        while frontier:
            curNode = heappop(frontier)
            if curNode.result == 0:
                self.target = curNode
                break

            for next in self.getAdjacents(curNode):
                new_cost = cost_so_far[curNode] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    next.f_val = new_cost + self.heuristic(next)
                    heappush(frontier, next)
                    came_from[next] = curNode

        return came_from, cost_so_far

    def heuristic(self, state):
        p_cell = state.p
        q_cell = state.q

        result = state.result

        sum_dist_p = 1
        sum_dist_q = 1

        p_foods = []
        q_foods = []
        for f1 in self.map.food1:
            if f1 in state.foods:
                continue
            p_foods.append(self.ManhatanDist(self.map.getCell(f1), p_cell))
            sum_dist_p += self.ManhatanDist(self.map.getCell(f1), p_cell)
        for f2 in self.map.food2:
            if f2 in state.foods:
                continue
            q_foods.append(self.ManhatanDist(self.map.getCell(f2), q_cell))
            sum_dist_q += self.ManhatanDist(self.map.getCell(f2), q_cell)
        for f3 in self.map.food3:
            if f3 in state.foods:
                continue
            p_foods.append(self.ManhatanDist(self.map.getCell(f3), p_cell))
            q_foods.append(self.ManhatanDist(self.map.getCell(f3), q_cell))
            sum_dist_p += self.ManhatanDist(self.map.getCell(f3), p_cell)
            sum_dist_q += self.ManhatanDist(self.map.getCell(f3), q_cell)

        if len(p_foods) != 0:
            p_foods = min(p_foods)
        else:
            p_foods = 0

        if len(q_foods) != 0:
            q_foods = min(q_foods)
        else:
            q_foods = 0

        dist_overall = p_foods + q_foods

        return dist_overall * result


    @staticmethod
    def EuclideanDist(p1, p2):
        return np.sqrt(np.power(p1.x - p2.x, 2) + np.power(p1.y - p2.y, 2))

    @staticmethod
    def ManhatanDist(p1, p2):
        return np.abs(p1.x - p2.x) + np.abs(p1.y - p2.y)


    # Adherents of current state -> State
    def getAdjacents(self, curState):
        res = deque([])
        p = curState.p
        q = curState.q
        # Possible adjacents for each agent
        p_adj = self.getAdjacentsCell(p)
        q_adj = self.getAdjacentsCell(q)

        # Q remains in its location, P must choose between its neighbors
        if q_adj.get(Direction.NO) is not None:
            q_dir = Direction.NO
            for p_dir in p_adj:
                if p_dir == Direction.NO:
                    continue
                p_cell = p_adj[p_dir]
                q_cell = q_adj[Direction.NO]

                # Food type 2 is poison for 'P'
                # It should be ignored, if it is remained.
                if p_cell.getType() == '2' and p_cell.getKey() not in curState.foods:
                    continue

                score = 0
                unseen_foods = deque([])
                if p_cell.getKey() != q_cell.getKey():
                    if p_cell.getKey() not in curState.foods and (p_cell.getType() == '1' or p_cell.getType() == '3'):
                        unseen_foods.append(p_cell.getKey())
                        score += 1

                    res.append(StateA(p_cell, q_cell,
                                     p_dir, q_dir,
                                     curState.result - score,
                                     curState,
                                     curState.depth + 1,
                                     curState.foods + unseen_foods))

        # P remains in its location, Q must choose between its neighbors
        if p_adj.get(Direction.NO) is not None:
            for q_dir in q_adj:
                if q_dir == Direction.NO:
                    continue
                q_cell = q_adj[q_dir]
                p_cell = p_adj[Direction.NO]

                # Food type 1 is poison for 'Q'
                if q_cell.getType() == '1' and q_cell.getKey() not in curState.foods:
                    continue

                score = 0
                unseen_foods = deque([])
                if p_cell.getKey() != q_cell.getKey():
                    if q_cell.getKey() not in curState.foods and (q_cell.getType() == '2' or q_cell.getType() == '3'):
                        unseen_foods.append(q_cell.getKey())
                        score += 1
                    # p, q, p_action, q_action, res, parent, depth, foods=None):
                    res.append(StateA(p_cell, q_cell,
                                     Direction.NO, q_dir,
                                     curState.result - score,
                                     curState,
                                     curState.depth + 1,
                                     curState.foods + unseen_foods))

        return res


    # Adjacents of current cell -> Cell
    def getAdjacentsCell(self, curCell):
        res = {}
        for d in Direction:
            nextCell = self.getNextCell(curCell, d)
            if nextCell.getType() == '%' or nextCell is None:
                continue
            res[d] = nextCell
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




    def getPath(self):
        result = []
        parent = self.target
        result.append(parent)
        while parent != self.startPoint:
            parent = parent.parent
            result.append(parent)
        result.reverse()
        self.path = result
        print('Path length:', len(self.path))

    def createInitState(self, frontier):
        p = self.map.getCell(self.map.p)
        q = self.map.getCell(self.map.q)
        self.startPoint = StateA(p, q, None, None, len(self.map), None, 0)
        self.startPoint.f_val = self.heuristic(self.startPoint)

        heappush(frontier, self.startPoint)


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

    def show_performance(self, _time):
        self.time = _time
        print(tabulate([['Nodes expanded', self.nodes_expanded],
                        ['Max search depth', self.max_search_depth],
                        ['Search depth', self.search_depth],
                        ['Max fringe size', self.max_fringe_size],
                        ['Time', _time]], headers=['Parameter', 'Value']))