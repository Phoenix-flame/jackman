# Uninformed search algorithm

from threading import Thread
import time
class BFS(Thread):
    def __init__(self, _map, _startPoint):
        super().__init__()
        self.map = _map
        self.startPoint = _startPoint

    def run(self):
        frontier = []
        visited = []
        test = []
        self._bfs(self.startPoint, visited, frontier, test)


    def _bfs(self, curNode, visited, frontier, test):
        if curNode.getType() == 'Q':
            curNode.changeType(' ')
            return True

        visited.append(curNode)
        if curNode.getType() is not 'P':
            curNode.changeType('*')

        time.sleep(0.005)
        children = self.map.getAdjacents(curNode)
        # print(childs)


        for child in children:
            if child not in visited and child not in frontier:
                frontier.append(child)
                test.append(str(child))
        # print(test)
        for node in frontier:
            del frontier[0]
            del test[0]
            if self._bfs(node, visited, frontier, test):
                break

        return True
