import math
import os
import random
import warnings

import numpy as np

import Agent
import Instance
import StringInstanceManager
import Vertex


class ConnectedComponentsException(Exception):
    pass


class Generator:
    def __init__(self, type, cols, rows, num_of_agents, horizon, ag_p=None, source='X', name=None, unpassable=None):

        # types:
        # FR - Full Random - the rewards in each vertex are generated randomly.
        # MT - Mountain Top - multiple "centers" with high probabilities
        # with decreasing probabilities when going away from a center
        # AG - anti-greedy - one big reward far away from starting point and many small ones near the starting point.
        # It is more rewarding to go for the big one but it is tempting to go for the small ones.
        # SC - Sanity Check - borders and only borders have reward, designed to check that 2 agents will follow the
        # expected paths by the border. (grid only)
        # EMPTY - Empty - empty.

        self.file_name = None
        self.name = None
        self.max_reward = 7
        self.source = source
        self.cols = cols
        self.rows = rows
        self.num_of_agents = num_of_agents
        self.horizon = horizon
        self.ACC = 5  # accuracy
        self.type = type
        self.unpassable = [] if unpassable is None else unpassable  # Hashes of vertices that are not in the final map.
        match self.type:
            case 'MT':
                self.num_of_centers = self.generate_num_of_centers()
                self.decrease = 0.25
                while True:
                    try:
                        self.centers = self.generate_centers()
                        self.dist_to_center = self.generate_distances(self.centers)
                    except ConnectedComponentsException:
                        continue
                    break
            case 'AG':
                if ag_p is None:
                    raise Exception("Type is anti-greedy but no probability parameter is given.")
                self.ag_p = ag_p
                if self.source != 'X':
                    raise Exception("Parsing into AG is not supported.")
                if self.horizon != self.rows:
                    self.horizon = self.rows
                    warnings.warn("Horizon was adjusted to be equal to number of rows as per definition"
                                  " of anti-greedy.", UserWarning)
                if self.max_reward != math.ceil(self.cols / self.ag_p):
                    self.max_reward = math.ceil(self.cols / self.ag_p)
                    warnings.warn("Mximum reward was adjusted as per definition"
                                  " of anti-greedy.", UserWarning)
                self.unpassable = [self.xy_to_num(x, y) for x in range(rows) for y in range(cols) if x != 0 and y != 0]
            case 'SC':
                if self.horizon != self.rows + self.cols - 3:
                    self.horizon = self.rows + self.cols - 3
                    warnings.warn("Horizon was adjusted to be equal to number of rows plus columns minus 3 as per "
                                  "definition of sanity-check.", UserWarning)
                if self.num_of_agents != 2:
                    self.num_of_agents = 2
                    warnings.warn("Number of agents was adjusted to be equal to 2 as per the definition of sanity "
                                  "check.", UserWarning)
        self.gen_names(name)

    def generate_num_of_centers(self):
        return math.ceil(self.get_map_size() / 20)

    def get_map_size(self):
        return self.rows * self.cols - len(self.unpassable)

    def gen_names(self, name=None):
        if name is None:
            type = self.type if self.type != 'AG' else 'AG' + "".join(str(self.ag_p).split('.'))
            self.name = 'i_' + str(self.rows * self.cols - len(self.unpassable)) + \
                        '_' + str(self.num_of_agents) + '_' + str(self.horizon) + '_' + type + '_' + self.source
        else:
            self.name = name
        self.file_name = self.name + ".py"

    def generate_init_loc_hash(self, agent_hash):
        for l in range(self.rows * self.cols):
            if self.num_is_legal(l):
                return l
        raise Exception("No legal squares")

    def generate_full_random_distr(self, vertex_hash):
        if self.max_reward > 1:
            distr_size = random.randint(2, self.max_reward + 1)
        else:
            distr_size = random.randint(1, 2)
        distr = {}
        if distr_size == 1:
            return {0: 1}
        for _ in range(distr_size - 1):
            distr[np.random.randint(1, self.max_reward)] = round(
                random.uniform(pow(1 / 10, self.ACC), 1 - sum(distr.values())), self.ACC)
        distr[0] = round(1 - sum(distr.values()), self.ACC)
        return distr

    def generate_empty_distr(self):
        return {0: 1}

    def generate_centers(self):
        centers = set()
        while len(centers) != self.num_of_centers:
            center = random.randint(1, self.rows * self.cols)
            if self.num_is_legal(center):
                centers.add(center)
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

    def generate_distances(self, centers):
        # if not self.each_connected_component_has_a_center(centers):
        #    raise Exception("Some connected component has no center")
        distances = {}
        level = 0
        next_level = centers
        for c in centers:
            distances[c] = level
            if not self.num_is_legal(c):
                raise Exception("Center " + str(c) + " assigned incorectly")

        while len(distances.keys()) != self.get_map_size():
            level += 1
            prev_level = next_level.copy()
            next_level = set()
            for c in prev_level:
                ngbrs = self.get_neighbours(*self.num_to_xy(c))
                for n in ngbrs:
                    if n not in distances:
                        next_level.add(int(n))
                        distances[n] = level
            if len(next_level) == 0:
                for i in range(self.cols * self.rows):
                    if self.num_is_legal(i) and i not in distances:
                        distances[i] = -1
                break
        return distances

    def distance_to_center_to_distr(self, x):
        prob_of_zero = min(x * self.decrease, 1) if x != -1 else 1
        return {1: round(1 - prob_of_zero, self.ACC),
                0: round(prob_of_zero, self.ACC)}

    def generate_mountain_top_distr(self, vertex_hash):
        if self.centers is None:
            self.generate_centers()
        if not self.dist_to_center:
            while True:
                try:
                    self.generate_distances(self.centers)
                except ConnectedComponentsException:
                    continue
                break

        return self.distance_to_center_to_distr(self.dist_to_center[vertex_hash])

    def generate_distr(self, vertex_hash):
        distr = None
        match self.type:
            case 'FR':
                distr = self.generate_full_random_distr(vertex_hash)
            case 'EMPTY':
                distr = self.generate_empty_distr()
            case 'MT':
                distr = self.generate_mountain_top_distr(vertex_hash)
            case 'AG':
                distr = self.generate_anti_greed_distr(vertex_hash)
            case 'SC':
                distr = self.generate_sanity_check_distr(vertex_hash)

        if self.distr_is_legal(distr):
            return distr
        fixed_distr = self.fixed_distr(distr)
        warnings.warn(
            f"Illegal distribution was created in: {self.name}\nIllegal distribution: {distr}\n Fixed distribution: {fixed_distr}\n",
            UserWarning)
        return fixed_distr  # This line is reachable

    def fixed_distr(self, distr):
        distr_sum = sum(list(distr.values()))
        new_distr = {}
        if distr_sum == 0:
            return {0: 1}
        for r in distr:
            new_distr[r] = distr[r] / distr_sum
        return new_distr

    def distr_is_legal(self, distr):
        return round(sum(list(distr.values())), self.ACC) == 1

    def generate_sanity_check_distr(self, v):
        x, y = self.num_to_xy(v)
        if ((x == 0) ^ (y == 0)) or ((x == self.cols-1) ^ (y == self.rows-1)):
            return {1: 1, 0: 0}
        else:
            return {0: 1}

    def generate_anti_greed_distr(self, v):
        x, y = self.num_to_xy(v)
        if x == 0:
            if y == self.rows - 1:
                distr = {math.ceil(self.cols / self.ag_p): self.ag_p, 0: 1 - self.ag_p}
                return distr
            else:
                return {0: 1}
        if y == 0:
            return {1: 1, 0: 0}

    def generate_utility_budget(self, agent_hash):
        return max(random.randint(1, self.horizon), 3)

    def generate_movement_budget(self, agent_hash):
        if self.type == 'AG' or self.type == 'SC':
            return self.horizon
        if self.horizon <= 2:
            return 2
        return random.randint(int(self.horizon * 0.5), self.horizon)

    def xy_to_num(self, x, y):
        num = y * self.cols + x + 1
        return num

    def get_neighbours(self, x, y):
        potential_neighbours = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        return [int(self.xy_to_num(m, n)) for (m, n) in potential_neighbours if self.xy_is_legal(m, n)]

    def num_is_legal(self, num):
        return 0 < num <= self.cols * self.rows and not num in self.unpassable

    def xy_is_legal(self, x, y):
        if self.unpassable is None:
            raise Exception("Failed to check legality because unpassable is not defined")
        return 0 <= x < self.cols and 0 <= y < self.rows and self.xy_to_num(x, y) not in self.unpassable

    def num_to_xy(self, num):
        x, y = (num - 1) % self.cols, (num - 1) // self.cols
        return x, y

    def gen_instance(self):
        map = []
        map_map = {}
        neighbours_hashes = {}
        for y in range(self.rows):
            for x in range(self.cols):
                vertex_hash = self.xy_to_num(x, y)
                if vertex_hash in self.unpassable:
                    continue
                v = Vertex.Vertex(vertex_hash)
                v.distribution = self.generate_distr(vertex_hash)
                neighbours_hashes[v] = self.get_neighbours(x, y)
                map_map[vertex_hash] = v
                map.append(v)
        for v in map:
            v.neighbours = [map_map[n_hash] for n_hash in neighbours_hashes[v]]
        agents = []
        for a in range(self.num_of_agents):
            agent = Agent.Agent(a, map_map[self.generate_init_loc_hash(a)], self.generate_movement_budget(a),
                                self.generate_utility_budget(a))
            agents.append(agent)
        return Instance.Instance(self.name, map, agents, self.horizon, self.source)

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
        for y in range(self.num_of_agents):
            f.write(
                "agent" + str(y) + " = Agent.Agent(" + str(y) + ", " + "vertex" + str(
                    self.generate_init_loc_hash(y)) + ", " +
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
        for y in range(self.num_of_agents):
            if y < self.num_of_agents - 1:
                f.write(agents[y] + ", ")
            else:
                f.write(agents[y])
        f.write("]\n")

        f.write("instance1 = Instance.Instance(\"" + self.name + "\", map1, agents, " + str(
            self.horizon) + ", source=" + "\"" + self.source + "\"" + ")\n")

def generate():
    for type in ['SC']:
        if type == 'AG':
            low = 5
            high = 55
            jump = 10
        else:
            low = 3
            high = 20
            jump = 1
        for size in range(low, high, jump):
            if (type == 'AG' and size % 10 != 5) or (type == 'SC' and size % 3 == 4):
                continue
            if type != 'AG' and type != 'SC':
                cols = max(random.randint(int(size * 0.75), int(size * 1.25)), 2)
                rows = max(random.randint(round(size * 0.75), round(size * 1.25)), 2)
            else:
                cols = size
                rows = size
            agents = max((cols + rows) // 5, 1)
            hor = max(random.randint(int(size * 0.9), int(size) * 2), 2)
            mr = max(size // 2, 2)
            if type != 'AG':
                G = Generator(type, cols, rows, agents, hor)
                G.ACC = 4
                G.MAX_REWARD = mr
                StringInstanceManager.to_string(G.gen_instance(), "Generated_encoded_instances/"+type)
                print(G.name + " added.")

            else:
                for p in [0.5, 0.1, 0.01]:
                    G = Generator(type, cols, cols, 1, cols, ag_p=p)
                    G.ACC = 4
                    G.MAX_REWARD = mr
                    StringInstanceManager.to_string(G.gen_instance(), "Generated_encoded_instances/AG")
                    print(G.name + " added.")

#generate()

'''for type in ['FR', 'MT']:
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
            G.max_reward = mr
            f = open("ready_maps/" + G.file_name, "w")
            g = open("THIRD_instance_collector.py", "a")
            g.write("from ready_maps import " + G.name + "\n")
            g.write("old_instances.append(" + G.name + ".instance1)\n")
            g.close()
            G.gen_map(f)
            f.close()
            break
        break
    break
'''
