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

    def actions(self, state):
        pass

    def make_action(self, action, state):
        pass


class DetInstance(Instance):
    def __init__(self, instance):
        super().__init__(instance.map, instance.agents, instance.horizon)
        self.map, self.map_map = instance.make_special_map_and_map_map(Vertex.DetVertex)
        self.agents, self.agents_map = instance.make_agents_and_agents_map(self.map_map, Agent.DetAgent)
        self.horizon = instance.horizon
        self.initial_state = State.DetState(self.agents, self.map)

    def regenerate_instance(self):
        for v in self.map:
            v.generate_reward()
        for a in self.agents:
            a = Agent.DetAgent(a.number, a.loc, a.movement_budget, a.utility_budget)


class StochInstance(Instance):
    def __init__(self, instance):
        super().__init__(instance.map, instance.agents, instance.horizon)
        self.map, self.map_map = instance.make_special_map_and_map_map(Vertex.Stoch_Vertex)
        self.agents, self.agents_map = instance.make_agents_and_agents_map(self.map_map, Agent.StochAgent)
        self.horizon = instance.horizon
        self.initial_state = State.StochState(self.agents, self.map)
