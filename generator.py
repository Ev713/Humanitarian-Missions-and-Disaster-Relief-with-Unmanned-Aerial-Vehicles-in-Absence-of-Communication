import os
import random

import numpy as np


class Generator:
    def __init__(self, name, type, cols, rows, agents, horizon, source='-'):
        self.MAX_REWARD = 7
        self.source = source
        self.cols = cols
        self.rows = rows
        self.NUM_OF_AGENTS = agents
        self.HORIZON = horizon
        self.actual_horizon = None
        self.ACC = 5  # accuracy
        # types: FR, MT, IRL, AG, SC, 'EMPTY'
        self.type = type
        self.unpassable = []
        match self.type:
            case 'MT':
                try:
                    self.NUM_OF_CENTERS = random.randint(1, self.rows * self.cols / 5)  # for mountain-top domain
                except:
                    self.NUM_OF_CENTERS = 1
                self.decrease = 0.25
                self.centers = self.generate_centers()
                self.dist_to_center = self.generate_dists(self.centers)
            case 'AG':
                self.max_value = self.MAX_REWARD
                self.min_value = 1
                self.a_locs = {a: self.generate_init_loc(a) for a in range(self.NUM_OF_AGENTS)}
                self.num_of_min_values = min(self.MAX_REWARD - 1,
                                             self.cols * self.rows - len(self.unpassable) - 1 - len(self.a_locs))
                self.dists_to_agents = self.generate_dists(set(self.a_locs.values()))
                self.sorted_by_dists = sorted(self.dists_to_agents.keys(), key=lambda x: self.dists_to_agents[x])
                self.big_vertex = self.sorted_by_dists[-1]
                self.small_vertices = [self.sorted_by_dists[i] for i in
                                       range(len(self.a_locs), len(self.a_locs) + self.num_of_min_values)]
                self.HORIZON = max(self.dists_to_agents.values())
                self.actual_horizon = self.HORIZON
        self.name_no_py = name + self.type
        self.name = self.name_no_py + ".py"

    def generate_init_loc(self, agent_hash):
        try:
            return self.a_locs[agent_hash]
        except:
            return 1

    def generate_full_random_distr(self, vertex_hash):
        if self.MAX_REWARD > 1:
            distr_size = random.randint(2, self.MAX_REWARD + 1)
        else:
            distr_size = random.randint(1, 2)
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
        centers = set()
        while len(centers) != self.NUM_OF_CENTERS:
            centers.add(random.randint(1, self.rows * self.cols))
        return centers

    def each_connected_component_has_a_center(self, centers):
        vertices = set(centers.copy())
        while True:
            new_vertices = set()
            for v in vertices:
                neighbours = set(self.get_neighbours(*self.num_to_xy(v)))
                new_vertices = new_vertices.union(neighbours)
            if new_vertices.issubset(vertices):
                return False
            vertices |= new_vertices
            if len(vertices) == self.rows * self.cols - len(self.unpassable):
                return True

    def generate_dists(self, centers):
        # if not self.each_connected_component_has_a_center(centers):
        #    raise Exception("Some connected component has no center")
        distances = {}
        level = 0
        next_level = centers
        for c in centers:
            distances[c] = level
            if c in self.unpassable or not self.num_is_legal(c):
                raise Exception("Center " + str(c) + " assigned incorectly")

        while len(distances.keys()) != self.rows * self.cols - len(self.unpassable):
            level += 1
            prev_level = next_level.copy()
            next_level = set()
            for c in prev_level:
                ngbrs = self.get_neighbours(*self.num_to_xy(c))
                pass
                for n in ngbrs:
                    next_level.add(int(n))
            for v in next_level:
                if v not in distances:
                    distances[v] = level
        return distances

    def distance_to_center_to_distr(self, x):
        return {1: round(pow(self.decrease, (x + 1)), self.ACC),
                0: round(1 - pow(self.decrease, (x + 1)), self.ACC)}

    def generate_mountain_top_distr(self, vertex_hash):
        if self.centers is None:
            self.generate_centers()
        if not self.dist_to_center:
            self.generate_dists(self.centers)
        return self.distance_to_center_to_distr(self.dist_to_center[vertex_hash])

    def generate_distr(self, vertex_hash):
        match self.type:
            case 'FR':
                return self.generate_full_random_distr(vertex_hash)
            case 'EMPTY':
                return self.generate_empty_distr()
            case 'MT':
                return self.generate_mountain_top_distr(vertex_hash)
            case 'AG':
                return self.generate_anti_greed_distr(vertex_hash)
            case 'SC':
                return self.generate_sc_distr(vertex_hash)

    def generate_sc_distr(self, v):
        x, y = self.num_to_xy(v)
        if x == 0 or y == 0 or x == self.cols or y == self.rows:
            return {1: 1}
        else:
            return {0: 1}

    def generate_anti_greed_distr(self, v):
        if v == self.big_vertex:
            return {self.max_value * 10: 0.1, 0: 0.9}
        if v in self.small_vertices:
            return {self.min_value: 1}
        else:
            return {0: 1}

    def generate_utility_budget(self, agent_hash):
        return max(random.randint(1, self.HORIZON), 3)

    def generate_movement_budget(self, agent_hash):
        if self.type == 'AG':
            return self.HORIZON
        try:
            mb = max(random.randint(int(self.HORIZON * 0.5), self.HORIZON), 2)
        except:
            mb = self.HORIZON
        if self.actual_horizon is None or mb > self.actual_horizon:
            self.actual_horizon = mb
        return mb

    def xy_to_num(self, x, y):
        num = y * self.cols + x + 1
        return num

    def get_neighbours(self, x, y):
        potential_neighbours = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        return [int(self.xy_to_num(m, n)) for (m, n) in potential_neighbours if self.xy_is_legal(m, n)]

    def num_is_legal(self, num):
        return 0 < num <= self.cols * self.rows

    def xy_is_legal(self, x, y):
        if self.unpassable is None:
            raise Exception("Failed to check legality because unpassable is not defined yet")
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
                    f.write(' ' * len(vertex_str) + '  ')
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

        f.write("instance1 = Instance.Instance(\"" + self.name_no_py + "\", map1, agents, " + str(
            self.actual_horizon) + ", source=" + "\"" + self.source + "\"" + ")\n")


'''for type in ['FR', 'SC', 'AG', 'MT']:
    for size in range(2, 25):
        if type == 'AG' and size < 3:
            continue
        cols = max(random.randint(int(size * 0.75), int(size * 1.25)), 2)
        rows = max(random.randint(round(size * 0.75), round(size * 1.25)), 2)
        agents = max((cols + rows) // 5, 1)
        hor = max(random.randint(int(size * 0.9), int(size) * 2), 2)
        mr = max(size // 2, 2)
        G = Generator(str(size), type, rows, cols, agents, hor)
        G.ACC = 4
        G.MAX_REWARD = mr
        f = open("very_ready_maps/" + G.name, "w")
        g = open("instance_collector.py", "a")
        g.write("from very_ready_maps import " + G.name_no_py + "\n")
        g.write("instances.append(" + G.name_no_py + ".instance1)\n")
        g.close()
        G.gen_map(f)
        f.close()
        print(G.name + " added.")'''
for type in ['FR', 'MT']:
    for size in range(3, 27, 6):
        for agents in range(1, 6):
            cols = max(random.randint(int(size * 0.75), int(size * 1.25)), 2)
            rows = max(random.randint(round(size * 0.75), round(size * 1.25)), 2)
            hor = max(random.randint(int(size * 0.9), int(size) * 2), 2)
            mr = max(size // 2, 2)
            G = Generator(
                'i_' + str(size) + '_' + str(cols) + '_' + str(rows) + '_' + str(agents) + '_' + str(hor) + '_', type,
                rows, cols, agents, hor)
            G.ACC = 4
            G.MAX_REWARD = mr
            f = open("ready_maps/" + G.name, "w")
            g = open("THIRD_instance_collector.py", "a")
            g.write("from ready_maps import " + G.name_no_py + "\n")
            g.write("instances.append(" + G.name_no_py + ".instance1)\n")
            g.close()
            G.gen_map(f)
            f.close()
            break
        break
    break
