import math


class Node:
    def __init__(self, state, parent = None):
        self.children = []
        self.parent = None
        self.depth

        self.state = state

        self.value = 0
        self.times_visited = 0

    def uct(self, t, c=math.sqrt(2)):
        return self.value/self.times_visited + c * math.sqrt(math.log(t) / self.times_visited)

    def is_fully_expanded(self):
        if self.state.is_terminal():
            return True
        if not self.children:
            return False
        for child in self.children:
            if child.times_visited == 0:
                return False
        return True

    def highest_uct_child(self, time):
        max_uct = self.children[0].uct(time)
        max_uct_child = self.children[0]
        for c in self.children:
            c_uct = c.uct(time)
            if c_uct > max_uct:
                max_uct = c_uct
                max_uct_child = c
        return max_uct_child

    def highest_value_child(self):
        max_value = self.children[0].value
        max_value_child = self.children[0]
        for c in self.children:
            if c.value > max_value:
                max_value = c.value
                max_value_child = c
        return max_value_child

    def expand(self, child_states):
        for child_state in child_states:
            child = Node(child_state, self)
            child.depth = self.depth + 1
            self.children.append(child)

    def backpropagate(self, value):
        backpropagator = self
        while backpropagator.parent is not None:
            backpropagator.value += value
            backpropagator = backpropagator.parent
        backpropagator.value += value


