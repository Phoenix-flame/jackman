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
        if self._ids(self.startPoint, self.target, 20):
            # res = [self.target]
            # parent = path[self.target]
            # while parent != self.startPoint:
            #     # print(parent)
            #     res.append(parent)
            #     cur = parent
            #     parent = path[cur]
            # res.append(parent)
            #
            # for i in res:
            #     if i.cellType == '*':
            #         i.changeType('Q')
            print("Done")
        else:
            print("There is no path :(")


    def _ids(self, source, target, maxDepth):

        for i in range(maxDepth):
            visited = []
            if self._dfs(source, target, visited, i):
                return True
        return False


    def _dfs(self, curNode, target, visited, maxDepth):
        print(curNode)
        if curNode == target:
            return True


        time.sleep(0.01)

        if maxDepth <= 0:
            return False
        visited.append(curNode)
        if curNode.cellType == ' ':
            curNode.changeType('*')


        children = self.map.getAdjacents(curNode, 'P')

        for child in children:
            if child not in visited:
                if self._ids(child, target, maxDepth - 1):
                    # path[child] = curNode
                    return True

        return False


