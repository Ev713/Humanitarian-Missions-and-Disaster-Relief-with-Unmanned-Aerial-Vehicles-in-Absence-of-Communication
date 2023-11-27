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

    def expectation(self):
        return sum([r * self.distribution[r] for r in self.distribution])

    def q(self):
        return 1 - self.distribution[0]

    def p(self):
        return self.distribution[0]

    def bernoulli(self):
        return 0 if self.q() == 0 else sum([r * self.distribution[r] for r in self.distribution]) / self.q()


class EmpVertex(Vertex):
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

    def generate_semi_emp_reward(self):
        if random.random() > self.p():
            self.reward = self.bernoulli()
            if self.reward == 0:
                self.is_empty = True
            else:
                self.is_empty = False
            return


    def __str__(self):
        return "det_v" + str(self.number) + " " + str(self.reward) + " " + str(self.is_empty)


class Stoch_Vertex(Vertex):
    def __init__(self, name):
        super().__init__(name)
