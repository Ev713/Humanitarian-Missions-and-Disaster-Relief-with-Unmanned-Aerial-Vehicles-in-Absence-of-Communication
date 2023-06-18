

class Node:
    def __init__(self, value, name):
        self.children = []
        self.value = value
        self.name = name
        self.is_terminal = False

    def __str__(self):
        return self.name # +", "+str(self.value)

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
                    line += "    "
            print(line)

