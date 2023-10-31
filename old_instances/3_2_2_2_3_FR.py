import Instance 
import Vertex
import Agent
vertex1 = Vertex.Vertex(1)
vertex1.distribution = {1: 0.0964, 0: 0.9036}
vertex2 = Vertex.Vertex(2)
vertex2.distribution = {1: 0.2065, 0: 0.7935}
vertex3 = Vertex.Vertex(3)
vertex3.distribution = {1: 0.4888, 0: 0.5112}
vertex4 = Vertex.Vertex(4)
vertex4.distribution = {1: 0.1321, 0: 0.8679}
vertex1.neighbours = [vertex2, vertex3]
vertex2.neighbours = [vertex1, vertex4]
vertex3.neighbours = [vertex4, vertex1]
vertex4.neighbours = [vertex3, vertex2]
agent0 = Agent.Agent(0, vertex1, 3, 3)
agent1 = Agent.Agent(1, vertex1, 3, 3)
map1 = [
        vertex1, vertex2, 
        vertex3, vertex4, ]
agents = [agent0, agent1]
instance1 = Instance.Instance("3_2_2_2_3_FR", map1, agents, 3)
