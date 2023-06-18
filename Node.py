import math


class Node:
    def __init__(self, state, parent=None):
        self.children = []
        self.parent = parent
        if self.parent is None:
            self.depth = 0
        else:
            self.depth = parent.depth + 1

        self.state = state

        self.value = 0
        self.times_visited = 0

    def __str__(self):
        return "TV:"+str(self.times_visited)+" R:"+str(self.value)+" "+str(self.state)

    def uct(self, t, c=math.sqrt(2)):
        return self.value / self.times_visited + c * math.sqrt(math.log(t) / self.times_visited)

    def all_children_visited(self):
        if self.state.is_terminal():
            return True
        if not self.children:
            return False
        for child in self.children:
            if child.times_visited == 0:
                return False
        return True

    def pick_unvisited_child(self):
        for c in self.children:
            if not c.times_visited:
                return c
        raise Exception("All children are visited!")
        return None

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

    def most_visited_child(self):
        max_visits = self.children[0].times_visited
        max_visits_child = self.children[0]
        for c in self.children:
            if c.times_visited > max_visits:
                max_visits = c.times_visited
                max_visits_child = c
        return max_visits_child

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

    def add_to_paths(self, paths):
        new_paths = []
        for i in range(len(paths)):
            attachment = None
            if i == 0:
                attachment = self
            path = [attachment]
            path_i = paths[i]
            path.extend(path_i)
            new_paths.append(path)
        return new_paths

    def get_leaf_paths(self):
        if not len(self.children):
            leaf = [[self]]
            return leaf
        else:
            paths = []
            for child in self.children:
                paths.extend(child.get_leaf_paths())
            return self.add_to_paths(paths)

    def get_tree(self):
        for path in self.get_leaf_paths():
            line = ""
            is_first = True
            for n in path:
                if n is not None:
                    if is_first:
                        line += "└── "
                        is_first = False
                    else:
                        line += "── "
                    line += str(n)
                else:
                    line += "                                                         "
            print(line)
