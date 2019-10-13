# class State:
#     def __init__(self, node, parent, depth):
#         self.node = node
#         self.parent = parent
#         self.depth = depth

class Statev2:
    def __init__(self, p, q, p_action, q_action, res, parent, depth, foods=[]):
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
        if other.p == self.p and other.q == self.q and other.result == self.result:
            return True
        return False

    def __str__(self):
        return "[" + str(self.p) + ", " + str(self.q) + "]" + " -> " \
               + " [" + str(self.depth) + ", " + str(self.result) + "]" +\
               "[" + str(self.p_action) + ", " + str(self.q_action) + "]" +\
                str(self.foods)

