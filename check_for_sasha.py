import Instance 
import Vertex
import Agent
vertex1 = Vertex.Vertex(1)
vertex1.distribution = {0: 1}
vertex2 = Vertex.Vertex(2)
vertex2.distribution = {2: 0.25, 1: 0.25, 0: 0.5}
vertex3 = Vertex.Vertex(3)
vertex3.distribution = {2: 0.25, 1: 0.25, 0: 0.5}
vertex4 = Vertex.Vertex(4)
vertex4.distribution = {2: 0.25, 1: 0.25, 0: 0.5}
vertex5 = Vertex.Vertex(5)
vertex5.distribution = {2: 0.25, 1: 0.25, 0: 0.5}
vertex6 = Vertex.Vertex(6)
vertex6.distribution = {2: 0.25, 1: 0.25, 0: 0.5}

vertex1.neighbours = [vertex2]

vertex2.neighbours = [ vertex3]

vertex3.neighbours = [ vertex4]

vertex4.neighbours = [ vertex5]

vertex5.neighbours = [ vertex6]

vertex6.neighbours = [vertex5]


agent0 = Agent.Agent(0, vertex1, 2, 1)
agent1 = Agent.Agent(1, vertex1, 2, 1)

map1 = [vertex1, vertex2, vertex3, vertex4, vertex5, vertex6]
agents = [agent0, agent1]
instance1 = Instance.Instance("check_for_sasha", map1, agents, 2)
