import os
import random

import numpy as np


def generate_mountains():
    return []


def generate_init_loc(agent_hash):
    return 0


class Generator:
    def __init__(self):
        self.MAX_REWARD = 4
        self.CORNERS = True
        self.SIMPLE = False
        self.VERY_SIMPLE = False
        self.M = 6
        self.N = 6
        self.NUM_OF_AGENTS = 2
        self.HORIZON = 7
        self.ACC = 1

    def generate_distr(self, vertex_hash):
        distr_size = np.random.randint(1, self.MAX_REWARD)
        distr = {}
        if self.CORNERS and (vertex_hash % self.M == self.M - 1 or vertex_hash >= (self.N - 1) * self.M):
            return {10: 1}
        if self.SIMPLE:
            p = round(random.random(), 1)
            r = random.randint(0, self.MAX_REWARD)
            if r == 0:
                return {0: 1}
            else:
                return {r: p, 0: 1-p}
        if self.VERY_SIMPLE:
            return {1: 1}

        if distr_size == 1:
            return {0: 1}
        for _ in range(distr_size-1):
            distr[np.random.randint(1, self.MAX_REWARD)] = round(random.uniform(pow(1/10, self.ACC), 1 - sum(distr.values())), self.ACC)
        distr[0] = round(1 - sum(distr.values()), self.ACC)
        return distr

    def generate_utility_budget(self, agent_hash):
        return self.HORIZON*2/3

    def generate_movement_budget(self, agent_hash):
        return self.HORIZON

    def gen_map(self):
        f.write("import Instance \nimport Vertex\nimport Agent\n")
        mountns = generate_mountains()  # (np.random.rand(dense) * n * m).round()
        # f.write(mountns)
        map1 = []
        for i in range(self.N):
            for j in range(self.M):
                vertex_hash = i * self.M + j
                if vertex_hash in mountns:
                    continue
                map1.append("vertex" + str(vertex_hash))
                f.write("vertex" + str(vertex_hash) + " = Vertex.Vertex("+str(vertex_hash) + ")\n")
                f.write("vertex" + str(vertex_hash) + ".distribution = ")
                f.write(str(self.generate_distr(vertex_hash)) + "\n")

        for i in range(self.N):
            for j in range(self.M):
                vertex_hash = i * self.N + j
                if vertex_hash in mountns:
                    continue
                else:
                    f.write("vertex" + str(vertex_hash) + ".neighbours = [")
                    ngbrs = []
                    if i > 0 and ((vertex_hash - self.N) not in mountns):
                        ngbrs.append(vertex_hash - self.N)
                    if j > 0 and ((vertex_hash - 1) not in mountns):
                        ngbrs.append(vertex_hash - 1)
                    if i < self.N - 1 and ((vertex_hash + self.N) not in mountns):
                        ngbrs.append(vertex_hash + self.N)
                    if j < self.M - 1 and ((vertex_hash + 1) not in mountns):
                        ngbrs.append(vertex_hash + 1)
                    for t in range(len(ngbrs)):
                        if t < len(ngbrs) - 1:
                            f.write("vertex" + str(ngbrs[t]) + ", ")
                        else:
                            f.write("vertex" + str(ngbrs[t]))
                    f.write("]\n")

        agents = []
        for i in range(self.NUM_OF_AGENTS):
            f.write(
                "agent" + str(i) + " = Agent.Agent(" + str(i) + ", " + "vertex" + str(generate_init_loc(i)) + ", " +
                str(self.generate_utility_budget(i)) + ", " + str(self.generate_movement_budget(i)) + ")\n")
            agents.append("agent" + str(i))

        f.write("map1 = [")
        for i in range(len(map1)):
            if i < len(map1) - 1:
                f.write(map1[i] + ", ")
                if (i + 1) % self.N == 0:
                    f.write("\n        ")
            else:
                f.write(map1[i])
        f.write("]\n")

        f.write("agents = [")
        for i in range(self.NUM_OF_AGENTS):
            if i < self.NUM_OF_AGENTS - 1:
                f.write(agents[i] + ", ")
            else:
                f.write(agents[i])
        f.write("]\n")

        f.write("instance1 = Instance.Instance(map1, agents, " + str(self.HORIZON) + ")\n")


G = Generator()
filename = "grid" + str(G.M) + "X" + str(G.N)
if G.CORNERS:
    filename += "_CORNERS"
if G.SIMPLE:
    filename += "_SIMPLE"
if G.VERY_SIMPLE:
    filename += "_VERY_SIMPLE"
filename += ".py"
f = open(filename, "w")
G.gen_map()
f.close()
print(filename+" added.")