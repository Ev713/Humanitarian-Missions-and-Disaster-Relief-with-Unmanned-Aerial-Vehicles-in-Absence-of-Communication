import Agent
import Instance
import Vertex

# instance line

v1 = Vertex.Vertex(1)
v2 = Vertex.Vertex(2)
v3 = Vertex.Vertex(3)
v4 = Vertex.Vertex(4)
v5 = Vertex.Vertex(5)

v1.neighbours = [v2]
v2.neighbours = [v3]
v3.neighbours = [v4]
v4.neighbours = [v5]
v5.neighbours = [v1]

v1.distribution = {0: 1}
v2.distribution = {1: 1}
v3.distribution = {1: 1}
v4.distribution = {1: 1}
v5.distribution = {1: 1}

a1 = Agent.Agent(1, v1, 7, 7)

map = [v1, v2, v3, v4, v5]
agents = [a1]
line = Instance.Instance(map, agents, 4)


# instance 1

v1 = Vertex.Vertex(1)
v2 = Vertex.Vertex(2)
v3 = Vertex.Vertex(3)
v4 = Vertex.Vertex(4)

v1.neighbours = [v2, v3]
v2.neighbours = [v1, v4]
v3.neighbours = [v1, v4]
v4.neighbours = [v2, v3]

v1.distribution = {0: 1}
v2.distribution = {1: 1}
v3.distribution = {0: 0.5, 1: 0.5}
v4.distribution = {3: 0.5, 0: 0.5}

a1 = Agent.Agent(1, v1, 3, 3)
a2 = Agent.Agent(2, v1, 3, 3)

map = [v1, v2, v3, v4]
agents = [a1, a2]
i1 = Instance.Instance(map, agents, 3)


# instance 15
vertex1 = Vertex.Vertex(1)
vertex2 = Vertex.Vertex(2)
vertex3 = Vertex.Vertex(3)
vertex4 = Vertex.Vertex(4)
vertex5 = Vertex.Vertex(5)
vertex6 = Vertex.Vertex(6)
vertex7 = Vertex.Vertex(7)
vertex8 = Vertex.Vertex(8)
vertex9 = Vertex.Vertex(9)
vertex10 = Vertex.Vertex(10)
vertex11 = Vertex.Vertex(11)
vertex12 = Vertex.Vertex(12)
vertex13 = Vertex.Vertex(13)
vertex14 = Vertex.Vertex(14)
vertex15 = Vertex.Vertex(15)

vertex1.neighbours = [vertex2, vertex5, vertex6]
vertex1.distribution = {0: 1}  # {0: 0.8, 1: 0.2}

vertex2.neighbours = [vertex1, vertex3, vertex8]
vertex2.distribution = {2: 1}  # {2: 0.6, 1: 0.3, 0: 0.1}

vertex3.neighbours = [vertex4, vertex2, vertex10]
vertex3.distribution = {4: 0.7, 2: 0.2, 1: 0.05, 0: 0.05}

vertex4.neighbours = [vertex12, vertex3, vertex5]
vertex4.distribution = {3: 0.6, 0: 0.2, 1: 0.1, 2: 0.1}

vertex5.neighbours = [vertex1, vertex4, vertex14]
vertex5.distribution = {0: 0.7, 4: 0.15, 3: 0.1, 5: 0.05}

vertex6.neighbours = [vertex15, vertex7, vertex1]
vertex6.distribution = {1: 0.6, 2: 0.2, 4: 0.1, 5: 0.1}

vertex7.neighbours = [vertex6, vertex8]
vertex7.distribution = {0: 0.5, 3: 0.25, 5: 0.15, 2: 0.1}

vertex8.neighbours = [vertex7, vertex2, vertex9]
vertex8.distribution = {1: 0.4, 5: 0.2, 3: 0.2, 0: 0.2}

vertex9.neighbours = [vertex10, vertex8]
vertex9.distribution = {3: 0.5, 1: 0.2, 0: 0.15, 5: 0.15}

vertex10.neighbours = [vertex11, vertex3, vertex9]
vertex10.distribution = {4: 0.5, 2: 0.3, 1: 0.15, 0: 0.05}

vertex11.neighbours = [vertex10, vertex12]
vertex11.distribution = {2: 0.5, 4: 0.2, 0: 0.15, 1: 0.15}

vertex12.neighbours = [vertex4, vertex13, vertex11]
vertex12.distribution = {5: 0.5, 3: 0.25, 1: 0.1, 0: 0.15}

vertex13.neighbours = [vertex12, vertex14]
vertex13.distribution = {4: 0.5, 3: 0.2, 2: 0.15, 1: 0.15}

vertex14.neighbours = [vertex13, vertex5, vertex15]
vertex14.distribution = {0: 0.45, 1: 0.3, 4: 0.15, 5: 0.1}

vertex15.neighbours = [vertex14, vertex6]
vertex15.distribution = {5: 0.5, 4: 0.15, 2: 0.15, 1: 0.2}

agent1 = Agent.Agent(1, vertex1, 3, 6)

agent2 = Agent.Agent(2, vertex1, 3, 6)

map1 = [vertex1, vertex2, vertex3, vertex4, vertex5, vertex6, vertex7, vertex8, vertex9, vertex10, vertex11, vertex12,
        vertex13, vertex14, vertex15]
agents = [agent1, agent2]

i15 = Instance.Instance(map1, agents, 4)
