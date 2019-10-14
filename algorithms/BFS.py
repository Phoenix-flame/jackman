# Uninformed search algorithm

from threading import Thread
import time
from tabulate import tabulate
from source.state import *
from source.direction import *



class BFS(Thread):
    def __init__(self, _map):
        super().__init__()
        self.map = _map
        self.path = None
        self.startPoint = None
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
        visited = set()
        frontier = deque([])
        self.createInitState(frontier)

        # test = self.getAdjacents(self.startPoint)
        # for i in test:
        #     print(i)
        if self._bfs(visited, frontier):
            self.getPath()
            print("Done")
            toc = time.time()
            self.show_performance(toc - tic)
            self.showResult()

        else:
            print("There is no path :(")










    def _bfs(self, visited, frontier):
        if frontier.__len__() == 0:
            return False
        curNode = frontier.popleft()

        if curNode.result == 0:
            self.target = curNode
            self.search_depth = curNode.depth
            return True

        visited.add(curNode)

        # DON'T touch this
        children = self.getAdjacents(curNode)
        self.nodes_expanded += 1


        for child in children:
            if child not in visited:
                frontier.append(child)
                visited.add(child)

                # DON'T touch this
                if child.depth > self.max_search_depth:
                    self.max_search_depth += 1

        # DON'T touch this
        if len(frontier) > self.max_fringe_size:
            self.max_fringe_size = len(frontier)

        return self._bfs(visited, frontier)











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

        # P remains in its location, Q must choose between its neighbors
        if p_adj.get(Direction.NO) is not None:
            for q_dir in q_adj:
                q_cell = q_adj[q_dir]
                p_cell = p_adj[Direction.NO]

                # Food type 1 is poison for 'Q'
                if q_cell.getType() == '1' and q_cell.getKey() not in curState.foods:
                    continue

                score = 0
                unseen_foods = deque([])
                if p_cell.getKey() != q_cell.getKey():
                    if p_cell.getKey() not in curState.foods and (p_cell.getType() == '1' or p_cell.getType() == '3'):
                        unseen_foods.append(p_cell.getKey())
                        score += 1
                    if q_cell.getKey() not in curState.foods and (q_cell.getType() == '2' or q_cell.getType() == '3'):
                        unseen_foods.append(q_cell.getKey())
                        score += 1
                    # p, q, p_action, q_action, res, parent, depth, foods=None):
                    res.append(State(p_cell, q_cell,
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

    def createInitState(self, frontier):
        p = self.map.getCell(self.map.p)
        q = self.map.getCell(self.map.q)

        frontier.append(State(p, q, None, None, len(self.map), None, 0))
        self.startPoint = frontier[0]


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
        print(tabulate([['Nodes expanded', self.nodes_expanded],
                        ['Max search depth', self.max_search_depth],
                        ['Search depth', self.search_depth],
                        ['Max fringe size', self.max_fringe_size],
                        ['Time', _time]], headers=['Parameter', 'Value']))
