# Uninformed search algorithm

from threading import Thread
import time

class IDS(Thread):
    def __init__(self, _map, _start, _target):
        super().__init__()
        self.startPoint = _start
        self.target = _target
        self.map = _map

    def run(self):
        visited = []
        frontier = []
        path = {}
        frontier.append(self.startPoint)
        if self._ids(self.startPoint, visited, frontier, path, self.target):
            res = [self.target]
            parent = path[self.target]
            while parent != self.startPoint:
                # print(parent)
                res.append(parent)
                cur = parent
                parent = path[cur]
            res.append(parent)

            for i in res:
                if i.cellType == '*':
                    i.changeType('Q')
            print("Done")
        else:
            print("There is no path :(")


    def _ids(self, curNode, visited, frontier, path, target):
        if len(frontier) == 0:
            return False
        if curNode == target:
            return True
        if target in frontier:
            return True

        time.sleep(0.01)

        visited.append(curNode)
        if curNode.cellType == ' ':
            curNode.changeType('*')


        children = self.map.getAdjacents(curNode, 'P')

        for child in children:
            if child not in visited:
                if self._ids(child, visited, frontier, path, target):
                    path[child] = curNode
                    return True

        return False

    def _dfs(self):
        pass


