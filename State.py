import copy

import numpy as np

import MatricesFunctions


class Position:
    def __init__(self, loc=-1, flyby=True):
        self.loc = loc
        self.flyby = flyby

    def __str__(self):
        return "( " + str(self.loc) + ", " + str(self.flyby) + " )"

    def __repr__(self):
        return str(self)


class State:
    # Info held by every node. The info is gathered using agents actions only therefore is deterministic.
    def __init__(self):
        self.time_left = 0  # int

    def is_terminal(self):
        return self.time_left == 0


class DetState(State):
    def __init__(self, instance=None):
        super().__init__()
        self.path = {}  # a.hash(): [pos, pos, -1, ... , -1] -
        # Required to count the reward of the state. Not needed in stochastic state.
        if instance is not None:
            self.time_left = instance.horizon
            for a in instance.agents:
                self.path[a.hash()] = [None for _ in range(instance.horizon + 1)]
                self.path[a.hash()][0] = Position(a.loc.hash(), False)

    def copy(self):
        copy_state = DetState()
        copy_state.path = copy.deepcopy(self.path)
        copy_state.time_left = self.time_left
        return copy_state

    def __str__(self):
        return str((self.path, self.time_left))


class StochState(State):
    def __init__(self, instance=None):
        super().__init__()
        self.a_pos = {}
        self.matrices = {}  # a.hash(): Matrix
        self.distr = {}  # v.hash(): probability
        self.reward = None
        if instance is not None:
            for a in instance.agents:
                self.time_left = instance.horizon
                self.a_pos[a.hash()] = Position(a.loc.hash(), False)  # a.hash(): v.hash()
                self.matrices[a.hash()] = MatricesFunctions.get_starting_matrix(a, a.loc)
            for v_hash in instance.map_map:
                self.distr[v_hash] = 1

    def __str__(self):
        return str((self.a_pos, self.time_left))

    def copy(self):
        copy_state = StochState()
        copy_state.a_pos = copy.deepcopy(self.a_pos)
        copy_state.matrices = copy.deepcopy(self.matrices)
        copy_state.distr = copy.deepcopy(self.distr)
        copy_state.time_left = self.time_left
        return copy_state


class StochUisRState(StochState):
    def __init__(self, instance=None):
        super().__init__(instance)
        self.distr = {}
        if instance is not None:
            for a in instance.agents:
                self.matrices[a.hash()] = MatricesFunctions.get_starting_vector(a, a.loc)
            for v_hash in instance.map_map:
                self.distr[v_hash] = self.dict_to_np_arr(instance.map_map[v_hash].distribution.copy())

    def dict_to_np_arr(self, dict):
        arr = np.zeros((max([k for k in dict if dict[k] != 0])+1))
        for k in dict:
            if round(k) != k:
                raise Exception("Number of targets must be an integer!")
            arr[k] = dict[k]
        return arr

    def copy(self):
        copy_state = StochUisRState()
        copy_state.a_pos = copy.deepcopy(self.a_pos)
        copy_state.matrices = copy.deepcopy(self.matrices)
        copy_state.distr = copy.deepcopy(self.distr)
        copy_state.time_left = self.time_left
        return copy_state
