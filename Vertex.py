class Vertex:
    def __init__(self, number):
        self.number = number  # String name
        self.neighbours = []  # list of Vertices
        self.distribution = {}  # reward: probability dictionary

    def hash(self):
        return self.number

    def __str__(self):
        return "v"+str(self.number)

class DetVertex(Vertex):
    def __init__(self, number):
        super().__init__(number)
        self.is_visited = False
        self.det_reward = 0

    def generate_reward(self):
        pass

    def __str__(self):
        return "det_v"+str(self.number)


class Stoch_Vertex(Vertex):
    def __init__(self, name):
        super().__init__(name)
        self.theta = 1
