import random


class Vertex:
    def __init__(self, number):
        self.number = number  # String name
        self.neighbours = []  # list of Vertices
        self.distribution = {}  # reward: probability dictionary

    def hash(self):
        if self.number == -1:
            raise Exception("-1 is an unusable hash number.")
        return self.number

    def __str__(self):
        return "v" + str(self.number)


class DetVertex(Vertex):
    def __init__(self, number):
        super().__init__(number)
        self.is_empty = False
        self.reward = 0

    def generate_reward(self):
        p = random.random()
        sum_p = 0
        for r in self.distribution:
            sum_p += self.distribution[r]
            if sum_p > p:
                self.reward = r
                if r == 0:
                    self.is_empty = True
                else:
                    self.is_empty = False
                return

    def __str__(self):
        return "det_v" + str(self.number)


class Stoch_Vertex(Vertex):
    def __init__(self, name):
        super().__init__(name)
        self.theta = 1
