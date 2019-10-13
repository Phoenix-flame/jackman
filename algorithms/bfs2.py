# Uninformed search algorithm

from threading import Thread
import time
from tabulate import tabulate
from collections import deque
from source.state import *
from source.direction import *



class BFSv2(Thread):
    def __init__(self, _map):
        super().__init__()
        self.map = _map
        self.res = None
        self.target = None

        # Performance measure
        self.cost_to_path = 0
        self.nodes_expanded = 0
        self.fringe_size = 0
        self.max_fringe_size = 0
        self.search_depth = 0
        self.max_search_depth = 0


    def run(self):
        tic = time.time()
        visited = deque([])
        frontier = deque([])
        p = self.map.getCell(self.map.p)
        q = self.map.getCell(self.map.q)


        frontier.append(Statev2(p, q, None, None, len(self.map), None, 0))
        startPoint = frontier[0]

        result = []
        if self._bfs(visited, frontier):
            print()
            parent = self.target
            result.append(parent)
            while parent != startPoint:
                # print(parent)
                parent = parent.parent
                result.append(parent)
            print("Done")

            result.reverse()
            for i in range(len(result)):
                if i == 0:
                    continue
                p_old, q_old = result[i - 1].p, result[i - 1].q
                p_new, q_new = result[i].p, result[i].q
                p_old.changeType(' ')
                q_old.changeType(' ')
                p_new.changeType('P')
                q_new.changeType('Q')
                time.sleep(1)

        else:
            print("There is no path :(")

        toc = time.time()
        self.show_performance(toc - tic)










    def _bfs(self, visited, frontier):
        if len(frontier) == 0:
            return False
        curNode = frontier.popleft()
        # print(curNode)
        if curNode.result == 0:
            self.target = curNode
            self.search_depth = curNode.depth
            return True

        visited.append(curNode)

        # DON'T touch this
        children = self.getAdjacents(curNode)
        self.nodes_expanded += 1


        for child in children:
            if child not in visited:
                frontier.append(child)
                visited.append(child)

                # DON'T touch this
                if child.depth > self.max_search_depth:
                    self.max_search_depth += 1

        # DON'T touch this
        if len(frontier) > self.max_fringe_size:
            self.max_fringe_size = len(frontier)

        return self._bfs(visited, frontier)











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
                p_dir, q_dir = i['dir'], j['dir']
                p_cell, q_cell = i['cell'], j['cell']
                if p_dir != Direction.NO and q_dir != Direction.NO:
                    continue
                if q_cell.getType() == '1' and q_cell.getKey() not in curState.foods:
                    continue
                if p_cell.getType() == '2' and p_cell.getKey() not in curState.foods:
                    continue
                score = 0
                unseen_foods = []
                if p_cell != q_cell:
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
            if player == 'P' and nextCell:
                res.append({'cell': nextCell, 'dir': d})
            elif player == 'Q' and nextCell:
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