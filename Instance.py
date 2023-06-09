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

    def make_det_agents_and_det_agents_map(self, det_map_map):
        det_agents = []
        det_agents_map = {}
        for a in self.agents:
            det_a = Agent.DetAgent(a.number, det_map_map[a.loc.hash()], a.movement_budget, a.utility_budget)
            det_agents.append(det_a)
            det_agents_map[a.hash()] = det_a
        return det_agents, det_agents_map

    def actions(self, state):
        pass

    def make_action(self, action, state):
        pass


class DetInstance(Instance):
    def __init__(self, instance):
        self.map, self.map_map = instance.make_det_map_and_det_map_map()
        self.agents, self.agents_map = instance.make_det_agents_and_det_agents_map(self.map_map)
        self.horizon = instance.horizon
        self.initial_state = State.DetState(self.agents, self.map)
