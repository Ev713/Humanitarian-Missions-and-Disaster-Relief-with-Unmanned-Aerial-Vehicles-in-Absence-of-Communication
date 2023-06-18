import copy

import MatricesFunctions


class State:
    # Info held by every node. The info is gathered using agents actions only therefore is deterministic.
    def __init__(self):
        self.time_left = 0  # int

    def is_terminal(self):
        return self.time_left == 0


class DetState(State):
    def __init__(self, instance=None):
        super().__init__()
        self.path = {}  # a.hash(): [v_1.hash(), ... , v_n.hash(), -1, ... , -1] -
        # Required to count the reward of the state. Not needed in stochastic state.
        if instance is not None:
            self.time_left = instance.horizon
            for a in instance.agents:
                self.path[a.hash()] = [-1 for _ in range(instance.horizon + 1)]
                self.path[a.hash()][0] = a.loc.hash()

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
        self.a_locs = {}  # a.hash(): v.hash()
        self.matrices = {}  # a.hash(): Matrix
        self.thetas = {}  # v.hash(): probability
