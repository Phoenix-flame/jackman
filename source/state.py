from collections import deque

class State:
    def __init__(self, p, q, p_action, q_action, res, parent, depth, foods=deque([])):
        self.p = p
        self.q = q
        self.p_action = p_action
        self.q_action = q_action
        self.result = res
        self.depth = depth
        self.parent = parent
        self.foods = foods

    def __eq__(self, other):
        return ((self.p.getKey() == other.p.getKey()) and
                (self.q.getKey() == other.q.getKey()) and
                (self.foods == other.foods)) and (self.depth == other.depth)

    def __str__(self):
        return "[" + str(self.p) + ", " + str(self.q) + "]" + " -> " \
               + " [" + str(self.depth) + ", " + str(self.result) + "]" +\
               "[" + str(self.p_action) + ", " + str(self.q_action) + "]" +\
                str(self.foods)

    def __hash__(self):
        tmp = ''
        for i in self.foods:
            tmp += "[" + str(i) + "]"
        return hash(self.p.getKey()) ^ hash(self.q.getKey()) ^ hash(tmp)


class StateB:
    def __init__(self, p, q, p_action, q_action, res, parent, depth, foods=deque([])):
        self.p = p
        self.q = q
        self.p_action = p_action
        self.q_action = q_action
        self.result = res
        self.depth = depth
        self.parent = parent
        self.foods = foods

    def __eq__(self, other):
        return ((self.p.getKey() == other.p.getKey()) and
                (self.q.getKey() == other.q.getKey()) and
                (self.foods == other.foods))

    def __str__(self):
        return "[" + str(self.p) + ", " + str(self.q) + "]" + " -> " \
               + " [" + str(self.depth) + ", " + str(self.result) + "]" + \
               "[" + str(self.p_action) + ", " + str(self.q_action) + "]" + \
               str(self.foods)

    def __hash__(self):
        tmp = ''
        for i in self.foods:
            tmp += "[" + str(i) + "]"
        return hash(self.p.getKey()) ^ hash(self.q.getKey()) ^ hash(tmp)


class StateA:
    def __init__(self, p, q, p_action, q_action, res, parent, depth, foods=deque([])):
        self.p = p
        self.q = q
        self.p_action = p_action
        self.q_action = q_action
        self.result = res
        self.depth = depth
        self.parent = parent
        self.foods = foods
        self.f_val = 0
        self.g_val = 0
        self.h_val = 0

    def __eq__(self, other):
        return ((self.p.getKey() == other.p.getKey()) and
                (self.q.getKey() == other.q.getKey()) and
                (self.foods == other.foods))

    def __str__(self):
        return "[" + str(self.p) + ", " + str(self.q) + "]" + " -> " \
               + " [" + str(self.depth) + ", " + str(self.result) + "]" +\
               "[" + str(self.p_action) + ", " + str(self.q_action) + "]" +\
                str(self.foods)


    def __lt__(self, other):
        return self.f_val < other.f_val

    def __gt__(self, other):
        return self.f_val > other.f_val

    def __le__(self, other):
        return self.f_val <= other.f_val

    def __ge__(self, other):
        return self.f_val >= other.f_val

    def __hash__(self):
        tmp = ''
        for i in self.foods:
            tmp += "[" + str(i) + "]"
        return hash(self.p.getKey()) ^ hash(self.q.getKey()) ^ hash(tmp)
