class State:
    # Info held by every node. The info is gathered using agents actions only therefore is deterministic.
    def __init__(self, agents, map):
        self.a_locs = [{a.hash():a.loc.hash()}for a in agents]
        self.action = None
        self.time_left = 0

    def is_terminal(self):
        return self.time_left > 0


class DetState(State):
    def __init__(self, agents, map):
        super().__init__(agents, map)
        self.reward_collected = 0


class StochState(State):
    def __init__(self, agents, map):
        super().__init__(agents, map)
        self.reward_expectation = 0
