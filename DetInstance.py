import itertools
import random
import copy
import Agent
import MatricesFunctions
import State
import Vertex
import Instance


class DetInstance(Instance.Instance):
    def __init__(self, instance=None):
        super().__init__(instance.file_name, instance.map, instance.agents, instance.horizon)
        self.map, self.map_map = instance.make_special_map_and_map_map(Vertex.DetVertex)
        self.agents, self.agents_map = instance.make_agents_and_agents_map(self.map_map, Agent.DetAgent)
        self.horizon = instance.horizon
        self.initial_state = State.DetState(instance)
        self.flybys = instance.flybys

    def actions(self, state):
        # action: {a1: v_k, a2: v_m, ...  }
        agent_actions = {}
        if self.flybys:
            fly_by_options = [False, True]
        else:
            fly_by_options = [False]
        #time = len(state.path[list(state.path.keys())[0]]) - state.time_left - 1
        time = self.horizon - state.time_left
        for a_hash in state.path:
            if self.agents_map[a_hash].movement_budget <= time:
                agent_actions[a_hash] = [None]
            else:
                a_loc_hash = state.path[a_hash][time].loc
                a_loc = self.map_map[a_loc_hash]
                agent_actions[a_hash] = [State.Position(a_loc_hash, b) for b in fly_by_options] +\
                                        [State.Position(n.hash(), b) for n in a_loc.neighbours for b in fly_by_options]


        actions = [a for a in Instance.product_dict(agent_actions)]
        return actions

    def regenerate_instance(self):
        for v in self.map:
            v.generate_reward()
        for a in self.agents:
            a.current_movement_budget = a.movement_budget
            a.current_utility_budget = a.utility_budget

    def make_action(self, action, state):
        new_state = state.copy()
        new_state.time_left -= 1
        time = self.horizon - new_state.time_left
        for a_hash in action.keys():
            new_state.path[a_hash][time] = action[a_hash]
        return new_state

    def reward(self, state, NUM_OF_SIMS=1):
        raise NotImplementedError


class DetU1Instance(DetInstance):
    def reward(self, state, NUM_OF_SIMS=1):
        tot_reward = 0
        for _ in range(NUM_OF_SIMS):
            self.regenerate_instance()
            round_reward = 0
            for t in range(len(list(state.path.values())[0])):
                for a in self.agents:
                    if a.current_movement_budget + 1 <= t or \
                            a.current_utility_budget < 1 or \
                            state.path[a.hash()][t] is None:
                        continue
                    a_loc_hash = state.path[a.hash()][t].loc
                    if a_loc_hash == -1 or state.path[a.hash()][t].flyby:
                        continue
                    a_loc = self.map_map[a_loc_hash]
                    if a_loc.is_empty:
                        continue
                    a_loc.is_empty = True
                    round_reward += a_loc.reward
                    a.current_utility_budget -= 1
            tot_reward += round_reward
        return tot_reward / NUM_OF_SIMS


class DetUisRInstance(DetInstance):
    def reward(self, state, NUM_OF_SIMS=1):
        tot_reward = 0
        for _ in range(NUM_OF_SIMS):
            self.regenerate_instance()
            round_reward = 0
            for t in range(len(list(state.path.values())[0])):
                for a_hash in self.agents_map:
                    if state.path[a_hash][t] is None:
                        continue
                    a_loc_hash = state.path[a_hash][t].loc
                    if a_loc_hash == -1 or state.path[a_hash][t].flyby:
                        continue
                    a_loc = self.map_map[a_loc_hash]
                    a = self.agents_map[a_hash]
                    if a_loc.reward == 0 or a.current_utility_budget == 0:
                        continue
                    utility_used = min(a_loc.reward, a.current_utility_budget)
                    a_loc.reward -= utility_used
                    a.current_utility_budget -= utility_used
                    round_reward += utility_used

            tot_reward += round_reward
        return tot_reward / NUM_OF_SIMS
