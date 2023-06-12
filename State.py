class State:
    # Info held by every node. The info is gathered using agents actions only therefore is deterministic.
    def __init__(self):
        self.a_locs = {}  # a.hash(): v.hash()
        self.time_left = 0  # int

    def is_terminal(self):
        return self.time_left > 0


class DetState(State):
    def __init__(self):
        super().__init__()
        self.path = {}  # a.hash(): [v_1, ... , v_n, -1, ... , -1] - Required to count the reward of the state.
                                                                    # Not needed in stochastic state.


class StochState(State):
    def __init__(self):
        super().__init__()
        self.matrices = {}  # a.hash(): Matrix
        self.thetas = {}  # v.hash(): probability
