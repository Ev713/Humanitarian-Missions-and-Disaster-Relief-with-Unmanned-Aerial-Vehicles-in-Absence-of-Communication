from abc import ABC

import numpy as np

import State
import Instance
import Vertex
import Agent
import Instance
import copy
import MatricesFunctions


class VectorInstance(Instance.Instance):
    def __init__(self, instance):
        super().__init__(instance.name, instance.map, instance.agents, instance.horizon)
        self.map, self.map_map = instance.make_special_map_and_map_map(Vertex.Stoch_Vertex)
        self.agents, self.agents_map = instance.make_agents_and_agents_map(self.map_map, Agent.StochAgent)
        self.horizon = instance.horizon
        self.initial_state = self.make_action(self.action_zero(State.VectorState(instance)), State.VectorState(instance))
        self.initial_state.time_left = self.horizon
        self.flybys = instance.flybys

    def action_zero(self, zero_state):
        action_zero = {}
        for a_hash in zero_state.a_pos:
            action_zero[a_hash] = State.Position(zero_state.a_pos[a_hash].loc, False)
        return action_zero

    def make_action(self, action, state):
        new_state = state.copy()
        new_state.time_left -= 1
        new_state.a_pos = copy.deepcopy(action)

        for a_hash in self.agents_map:
            if action[a_hash] is None or action[a_hash].flyby or \
                    self.agents_map[a_hash].movement_budget < self.horizon - new_state.time_left:
                continue
            vertex_hash = action[a_hash].loc
            try:
                new_matrix = MatricesFunctions.new_matrix(state.matrices[a_hash], state.dynamic_distrs[vertex_hash])
            except:
                breakpoint()
            new_distr = MatricesFunctions.update_distr(state.matrices[a_hash], state.dynamic_distrs[vertex_hash])
            new_state.matrices[a_hash] = new_matrix
            new_state.dynamic_distrs[vertex_hash] = new_distr
        return new_state

    def reward(self, state):
        if state.reward is not None:
            return state.reward
        state.reward = MatricesFunctions.get_matrices_reward(state.matrices)
        return state.reward

