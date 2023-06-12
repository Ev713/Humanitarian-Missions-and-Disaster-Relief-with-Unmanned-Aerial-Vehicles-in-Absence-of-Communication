import Agent
import Instance
import MatricesFunctions
import Node
import State
import Vertex

v1 = Vertex.Vertex(1)
v2 = Vertex.Vertex(2)
v3 = Vertex.Vertex(3)
v4 = Vertex.Vertex(1)

v1.neighbours = [v2, v3]
v2.neighbours = [v1, v4]
v3.neighbours = [v1, v4]
v4.neighbours = [v2, v3]

v1.distribution = {0: 1}
v2.distribution = {0: 0.5}
v1.distribution = {1: 0.5}
v1.distribution = {3: 0.5}

a1 = Agent.Agent(1, v1, 3, 3)
a2 = Agent.Agent(2, v1, 3, 3)

map = [v1, v2, v3, v4]
agents = [a1, a2]
i1 = Instance.Instance(map, agents, 3)
