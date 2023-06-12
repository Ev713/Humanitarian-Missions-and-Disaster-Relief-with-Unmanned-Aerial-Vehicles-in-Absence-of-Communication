import itertools

import Agent
import State
import Vertex


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

    def get_agent_location(self, state, a_hash):
        return self.map_map[state.a_locs[a_hash]]

    def actions(self, state):
        agent_movements = {}
        for a_hash in state.agents:
            a_loc = self.get_agent_location(state, a_hash)
            agent_movements[a_hash] = a_loc.neighbours
        actions = [action for action in itertools.product(agent_movements)]
        return actions

    def make_action(self, action, state):  # Abstract method
        pass

    def make_initial_state(self, is_det):
        raise NotImplementedError


class DetInstance(Instance):
    def __init__(self, instance):
        super().__init__(instance.map, instance.agents, instance.horizon)
        self.map, self.map_map = instance.make_special_map_and_map_map(Vertex.DetVertex)
        self.agents, self.agents_map = instance.make_agents_and_agents_map(self.map_map, Agent.DetAgent)
        self.horizon = instance.horizon
        self.initial_state = self.make_initial_state(True)

    def regenerate_instance(self):
        for v in self.map:
            v.generate_reward()
        for a in self.agents:
            a = Agent.DetAgent(a.number, a.loc, a.movement_budget, a.utility_budget)

    def make_action(self, action, state):
        new_state = state.copy
        new_state.a_locs = action.copy
        new_state.time_left -= 1
        time = self.horizon - state.time_left
        for a_hash in new_state.action:
            new_state.a_locs[a_hash][time] = action[a_hash]
        return new_state

class StochInstance(Instance):
    def __init__(self, instance):
        super().__init__(instance.map, instance.agents, instance.horizon)
        self.map, self.map_map = instance.make_special_map_and_map_map(Vertex.Stoch_Vertex)
        self.agents, self.agents_map = instance.make_agents_and_agents_map(self.map_map, Agent.StochAgent)
        self.horizon = instance.horizon
        self.initial_state = self.make_initial_state(False)

    def make_action(self, action, state):
        raise NotImplementedError
