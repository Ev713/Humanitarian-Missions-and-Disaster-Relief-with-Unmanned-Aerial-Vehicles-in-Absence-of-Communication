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

    def hash(self):
        return self.loc, self.flyby


class State:
    # Info held by every node. The info is gathered using agents actions only therefore is deterministic.
    def __init__(self):
        self.time_left = 0  # int

    def is_terminal(self):
        return self.time_left == 0

    def get_a_pos(self, a_hash):
        pass


class EmpState(State):
    def __init__(self, instance=None):
        super().__init__()
        self.path = {}  # a.hash(): [pos, pos, -1, ... , -1] -
        # Required to count the reward of the state. Not needed in stochastic state.
        if instance is not None:
            self.time_left = instance.horizon
            for a in instance.agents:
                self.path[a.hash()] = [None for _ in range(instance.horizon + 1)]
                self.path[a.hash()][0] = Position(a.loc.hash(), False)

    def get_a_pos(self, a_hash):
        if self.path[a_hash][-1] is not None:
            return self.path[a_hash][-1]
        first_none = 0
        while self.path[a_hash][first_none] is not None:
            first_none += 1
        return self.path[a_hash][first_none - 1]

    def copy(self):
        copy_state = EmpState()
        copy_state.path = copy.deepcopy(self.path)
        copy_state.time_left = self.time_left
        return copy_state

    def __str__(self):
        return str((self.path, self.time_left))


class VectorState(State):
    def __init__(self, instance=None):
        super().__init__()
        self.a_pos = {}
        self.reward = None
        if instance is not None:
            for a in instance.agents:
                self.time_left = instance.horizon
                self.a_pos[a.hash()] = Position(a.loc.hash(), False)  # a.hash(): v.hash()
        self.dynamic_distrs = {}  # v_hash: { r : p }
        self.matrices = {}  # a_hash: np.array((max_r, max_u))
        if instance is not None:
            for a in instance.agents:
                self.matrices[a.hash()] = MatricesFunctions.get_starting_matrix(a, a.loc)
            for v_hash in instance.map_map:
                self.dynamic_distrs[v_hash] = instance.map_map[v_hash].distribution.copy()

    def calculate_vertex_estimate(self, vrtx):
        probs = self.dynamic_distrs[vrtx.hash()]
        return sum([probs[i] * i for i in probs.keys()])

    def copy(self):
        copy_state = VectorState()
        copy_state.a_pos = copy.deepcopy(self.a_pos)
        copy_state.matrices = copy.deepcopy(self.matrices)
        copy_state.dynamic_distrs = copy.deepcopy(self.dynamic_distrs)
        copy_state.time_left = self.time_left
        return copy_state

    def hash(self):
        return (pos.hash() for pos in self.a_pos), ((a, str(self.matrices[a])) for a in self.matrices), \
               (v, str(self.dynamic_distrs[v]) for v in self.dynamic_distrs)

    def get_a_pos(self, a_hash):
        return self.a_pos[a_hash]

    def __str__(self):
        return str(self.a_pos)


def dict_to_np_arr(dict):
    if round(sum(dict.values()), 5) != 1:
        raise Exception("Sum of probabilities in distribution must be 1")
    arr = np.zeros((max([k for k in dict if dict[k] != 0]) + 1))
    for k in dict:
        if round(k) != k:
            raise Exception("Number of targets must be an integer!")
        if dict[k] != 0:
            arr[k] = dict[k]
    return arr
