import itertools
import random
import copy
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
    def __init__(self, map, agents, horizon):
        self.map = map  # list of Vertices
        self.map_map = {v.hash(): v for v in map}
        self.agents = agents  # list of agents
        self.agents_map = {a.hash(): a for a in agents}
        self.horizon = horizon  # int
        self.initial_state = (agents.copy(), map.copy())

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

    def actions(self, state):
        pass

    def make_action(self, action, state):  # Abstract method
        pass


class DetInstance(Instance):
    def __init__(self, instance=None):
        super().__init__(instance.map, instance.agents, instance.horizon)
        self.map, self.map_map = instance.make_special_map_and_map_map(Vertex.DetVertex)
        self.agents, self.agents_map = instance.make_agents_and_agents_map(self.map_map, Agent.DetAgent)
        self.horizon = instance.horizon
        self.initial_state = State.DetState(instance)

    def get_agent_location(self, state, a_hash, time):
        return self.map_map[state.path[a_hash][time]]

    def actions(self, state):
        # action: {p1: v_k, p2: v_m, ...  }
        agent_movements = {}
        time = len(state.path[list(state.path.keys())[0]]) - state.time_left - 1
        for a_hash in state.path:
            a_loc = self.get_agent_location(state, a_hash, time)
            agent_movements[a_hash] =[n.hash() for n in a_loc.neighbours]
        actions = [a for a in product_dict(agent_movements)]
        return actions

    def regenerate_instance(self):
        for v in self.map:
            v.generate_reward()
        new_agents = []
        for a in self.agents:
            new_agents.append(Agent.DetAgent(a.number, a.loc, a.movement_budget, a.utility_budget))
        self.agents = new_agents

    def make_action(self, action, state):
        new_state = state.copy()
        new_state.time_left -= 1
        time = self.horizon - new_state.time_left
        for a_hash in action.keys():
            if self.agents_map[a_hash].movement_budget < time:
                new_state.path[a_hash][time] = -1  # chosen action cannot be done due to insufficient movement budget
            else:
                new_state.path[a_hash][time] = action[a_hash]
        return new_state

    def reward(self, state):
        self.regenerate_instance()
        tot_reward = 0
        for t in range(self.horizon):
            for a in self.agents:
                if state.path[a.hash()][t] == -1 or a.utility_budget < 1:
                    continue
                a_loc = self.get_agent_location(state, a.hash(), t)
                if a_loc.is_empty:
                    continue
                a_loc.is_empty = True
                tot_reward += a_loc.reward
                a.current_utility_budget -= 1
        return tot_reward


class StochInstance(Instance):
    def __init__(self, instance):
        super().__init__(instance.map, instance.agents, instance.horizon)
        self.map, self.map_map = instance.make_special_map_and_map_map(Vertex.Stoch_Vertex)
        self.agents, self.agents_map = instance.make_agents_and_agents_map(self.map_map, Agent.StochAgent)
        self.horizon = instance.horizon
        self.initial_state = State.StochState(instance)

    def actions(self, state):
        agent_movements = {}
        for a_hash in state.a_locs:
            a_loc = self.map_map[state.a_locs[a_hash]]
            agent_movements[a_hash] = [n.hash() for n in a_loc.neighbours]
        actions = [a for a in product_dict(agent_movements)]
        return actions

    def make_action(self, action, state):

        new_state = state.copy()
        new_state.time_left -= 1
        new_state.a_locs = copy.deepcopy(action)
        for a_hash in self.agents_map:
            if action[a_hash] == -1:
                continue
            vertex_hash = action[a_hash]
            new_matrix = MatricesFunctions.new_matrix(state.matrices[a_hash], self.map_map[vertex_hash].distribution,
                                                      new_state.thetas[vertex_hash])
            new_theta = MatricesFunctions.update_theta(state.matrices[a_hash], new_state.thetas[vertex_hash])
            new_state.matrices[a_hash] = new_matrix
            new_state.thetas[vertex_hash] = new_theta
        return new_state

    def reward(self, state):
        return MatricesFunctions.get_tot_reward(state.matrices)
