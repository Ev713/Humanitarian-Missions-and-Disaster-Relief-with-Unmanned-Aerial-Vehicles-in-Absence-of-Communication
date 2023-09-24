import itertools
import random
import copy
import sys

import Agent
import MatricesFunctions
import State
import Vertex


def product_dict(dict):
    """
    :param dict: {a1: [v1_1, v2_1, ... , v_n_1], a2: [v1_2, v2_2, ... , v_n_2], ... }
    :return: [{a1:v1_1, a2: v1_2, ...}, {a1:v2_1, a2: v1_2, ...},{,a1:v1_1, a2: v2_2, ...} {a1:v2_1, a2: v2_2, ...}...]
    """
    mini_dicts = {key: [] for key in dict}
    for key in dict:
        for l in dict[key]:
            mini_dicts[key].append({key: l})
    big_dict = [a for a in itertools.product(*mini_dicts.values())]
    dict_actions = []
    for a in big_dict:
        a_dict = {}
        for mini_dict in a:
            a_dict.update(mini_dict)
        dict_actions.append(a_dict)
    return dict_actions


class Instance:
    def __init__(self, name, map, agents, horizon, source='-'):
        self.name = name
        self.map = map  # list of Vertices
        self.map_map = {v.hash(): v for v in map}
        self.agents = agents  # list of agents
        self.agents_map = {a.hash(): a for a in agents}
        self.horizon = horizon  # int
        self.initial_state = (agents.copy(), map.copy())
        self.flybys = True
        self.check_sums_of_probs_is_0()
        self.distance = {}
        self.source = source

    def map_reduce(self):
        self.calculate_distance_between_vertices()
        useful_vertex = []
        starting_pos = []
        for i in self.agents:
            starting_pos.append(i.loc)
        for i in self.map:
            if (i.distribution[0] < 1) or (i in starting_pos):
                useful_vertex.append(i)

        is_used = set()
        for start in useful_vertex:
            for end in useful_vertex:
                queue = [(start, [])]
                while (queue):
                    cur, prev = queue.pop()
                    if (cur == end):
                        for t in prev:
                            is_used.add(t)
                        queue = []
                    else:
                        for t in cur.neighbours:
                            queue.insert(0, (t, prev + [cur]))

        new_map = []
        for i in self.map:
            if (i in is_used) or (i in useful_vertex):
                ngbr = []
                for j in i.neighbours:
                    if (j in is_used) or (j in useful_vertex):
                        ngbr.append(j)
                i.neighbours = ngbr
                new_map.append(i)

        self.map = new_map

    def check_sums_of_probs_is_0(self):
        for v in self.map:
            try:
                if 0 not in v.distribution:
                    v.distribution[0] = 0
            except: breakpoint()
            if round(sum(v.distribution.values()), 7)!=1:
                raise Exception("Sum of vertex "+str(v)+"'s probabilities is not 0!")



    def make_det_map_and_det_map_map(self):
        det_map = []
        det_map_map = {}
        for v in self.map:
            det_v = Vertex.DetVertex(v.hash())
            det_map.append(det_v)
            det_map_map[v.hash()] = det_v
        for v in self.map:
            det_v = det_map_map[v.hash()]
            for n in v.neighbours:
                det_v.neighbours.append(det_map_map[n.hash()])
        return det_map, det_map_map

    def make_special_map_and_map_map(self, ver_builder):
        map = []
        map_map = {}
        for v in self.map:
            new_v = ver_builder(v.hash())
            map.append(new_v)
            map_map[v.hash()] = new_v
            new_v.distribution = copy.deepcopy(v.distribution)
        for v in self.map:
            det_v = map_map[v.hash()]
            for n in v.neighbours:
                det_v.neighbours.append(map_map[n.hash()])
        return map, map_map

    def make_agents_and_agents_map(self, map_map, agent_builder):
        new_agents = []
        new_agents_map = {}
        for a in self.agents:
            new_a = agent_builder(a.number, map_map[a.loc.hash()], a.movement_budget, a.utility_budget)
            new_agents.append(new_a)
            new_agents_map[a.hash()] = new_a
        return new_agents, new_agents_map

    def check_agents_integrity(self):
        for a in self.agents:
            if a not in self.agents_map.values():
                return False
        for a_hash in self.agents_map:
            if self.agents_map[a_hash] not in self.agents:
                return False
        return True

    def actions(self, state):
        pass

    def make_action(self, action, state):  # Abstract method
        pass
