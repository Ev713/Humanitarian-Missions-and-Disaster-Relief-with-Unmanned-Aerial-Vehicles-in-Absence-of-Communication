import os
import random

import numpy as np


class Generator:
    def __init__(self, type):
        self.MAX_REWARD = 4
        self.cols = 8
        self.rows = 8
        self.NUM_OF_AGENTS = 2
        self.HORIZON = 6
        self.ACC = 2 # accuracy
        # types: FR, MT, IRL, AG, SC, 'EMPTY'
        self.type = type
        self.unpassable = None
        if self.type == 'MT':
            self.NUM_OF_CENTERS = 2  # for mountain-top domain
            self.decrease = 0.5
            self.centers = [13, 32]  # self.generate_centers()
            self.dist_to_center = {}
        self.name = "grid" + str(self.cols) + "X" + str(self.rows) + self.type + ".py"

    def get_unpassable(self):
        return []

    def generate_init_loc(self, agent_hash):
        return 1

    def generate_full_random_distr(self, vertex_hash):
        distr_size = np.random.randint(1, self.MAX_REWARD)
        distr = {}

        if distr_size == 1:
            return {0: 1}
        for _ in range(distr_size - 1):
            distr[np.random.randint(1, self.MAX_REWARD)] = round(
                random.uniform(pow(1 / 10, self.ACC), 1 - sum(distr.values())), self.ACC)
        distr[0] = round(1 - sum(distr.values()), self.ACC)
        return distr

    def generate_empty_distr(self):
        return {0: 1}

    def generate_centers(self):
        self.centers = set()
        while len(self.centers) != self.NUM_OF_CENTERS:
            self.centers.add(random.randint(1, self.rows * self.cols))

    def generate_distances(self):
        level = 0
        next_level = self.centers
        for c in self.centers:
            self.dist_to_center[c] = level
            if c in self.unpassable or not self.num_is_legal(c):
                raise Exception("Center "+str(c)+" assigned incorectly")

        while len(self.dist_to_center.keys()) != self.rows * self.cols - len(self.unpassable):
            level += 1
            prev_level = next_level.copy()
            next_level = set()
            for c in prev_level:
                ngbrs = self.get_neighbours(*self.num_to_xy(c))
                pass
                for n in ngbrs:
                    next_level.add(int(n))
            for v in next_level:
                if v not in self.dist_to_center:
                    self.dist_to_center[v] = level

    def distance_to_center_to_distr(self, x):
        return {1: round(1 * pow(self.decrease, (x + 1)), self.ACC), 0: round(1-pow(self.decrease, (x + 1)), self.ACC)}

    def generate_mountain_top_distr(self, vertex_hash):
        if self.centers is None:
            self.generate_centers()
        if not self.dist_to_center:
            self.generate_distances()
        return self.distance_to_center_to_distr(self.dist_to_center[vertex_hash])

    def generate_distr(self, vertex_hash):
        match self.type:
            case 'FR':
                return self.generate_full_random_distr(vertex_hash)
            case 'EMPTY':
                return self.generate_empty_distr()
            case 'MT':
                return self.generate_mountain_top_distr(vertex_hash)

    def generate_utility_budget(self, agent_hash):
        return round(self.HORIZON * 2 / 3)

    def generate_movement_budget(self, agent_hash):
        return self.HORIZON

    def xy_to_num(self, x, y):
        num = y * self.cols + x + 1
        return num

    def get_neighbours(self, x, y):
        neighbours = []
        potential_neighbours = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        n = [int(self.xy_to_num(m, n)) for (m, n) in potential_neighbours if self.xy_is_legal(m, n)]
        return n

    def num_is_legal(self, num):
        return 0 < num <= self.cols * self.rows

    def xy_is_legal(self, x, y):
        return 0 <= x < self.cols and 0 <= y < self.rows and self.xy_to_num(x, y) not in self.unpassable

    def num_to_xy(self, num):
        x, y = (num - 1) % self.cols, (num - 1) // self.cols
        return x, y

    def gen_map(self, f):
        f.write("import Instance \nimport Vertex\nimport Agent\n")
        mountns = self.unpassable
        # f.write(mountns)
        for y in range(self.rows):
            for x in range(self.cols):
                vertex_hash = self.xy_to_num(x, y)
                if vertex_hash in mountns:
                    continue
                f.write("vertex" + str(vertex_hash) + " = Vertex.Vertex(" + str(vertex_hash) + ")\n")
                f.write("vertex" + str(vertex_hash) + ".distribution = ")
                f.write(str(self.generate_distr(vertex_hash)) + "\n")

        for y in range(self.rows):
            for x in range(self.cols):
                vertex_hash = self.xy_to_num(x, y)
                if vertex_hash in mountns:
                    continue
                else:
                    f.write("vertex" + str(vertex_hash) + ".neighbours = [")
                    ngbrs = self.get_neighbours(x, y)
                    for t in range(len(ngbrs)):
                        if t < len(ngbrs) - 1:
                            f.write("vertex" + str(ngbrs[t]) + ", ")
                        else:
                            f.write("vertex" + str(ngbrs[t]))
                    f.write("]\n")

        agents = []
        for y in range(self.NUM_OF_AGENTS):
            f.write(
                "agent" + str(y) + " = Agent.Agent(" + str(y) + ", " + "vertex" + str(
                    self.generate_init_loc(y)) + ", " +
                str(self.generate_movement_budget(y)) + ", " + str(self.generate_utility_budget(y)) + ")\n")
            agents.append("agent" + str(y))

        f.write("map1 = [")
        for y in range(self.rows):
            for x in range(self.cols):
                if x == 0:
                    f.write("\n        ")
                vertex_hash = self.xy_to_num(x, y)
                vertex_str = "vertex" + str(vertex_hash) + ' ' * (
                        len(str(self.rows * self.cols)) - len(str(vertex_hash)))
                if vertex_hash in mountns:
                    f.write(' '*len(vertex_str)+'  ')
                else:
                    f.write(vertex_str + ", ")
        f.write("]\n")

        f.write("agents = [")
        for y in range(self.NUM_OF_AGENTS):
            if y < self.NUM_OF_AGENTS - 1:
                f.write(agents[y] + ", ")
            else:
                f.write(agents[y])
        f.write("]\n")

        f.write("instance1 = Instance.Instance(map1, agents, " + str(self.HORIZON) + ")\n")


'''
G = Generator('MT')
filename = "grid" + str(G.cols) + "X" + str(G.rows)
filename += G.type
filename += ".py"
f = open(filename, "w")
G.gen_map(f)
f.close()
print(filename + " added.")
'''
