import Instance 
import Vertex
import Agent
vertex1 = Vertex.Vertex(1)
vertex1.distribution = {1: 0.3656, 0: 0.6344}
vertex2 = Vertex.Vertex(2)
vertex2.distribution = {1: 0.3793, 0: 0.6207}
vertex3 = Vertex.Vertex(3)
vertex3.distribution = {1: 0.5976, 0: 0.4024}
vertex4 = Vertex.Vertex(4)
vertex4.distribution = {1: 0.012, 0: 0.988}
vertex5 = Vertex.Vertex(5)
vertex5.distribution = {1: 0.0103, 0: 0.9897}
vertex6 = Vertex.Vertex(6)
vertex6.distribution = {1: 0.0225, 0: 0.9775}
vertex7 = Vertex.Vertex(7)
vertex7.distribution = {1: 0.9939, 0: 0.0061}
vertex8 = Vertex.Vertex(8)
vertex8.distribution = {1: 0.7703, 0: 0.2297}
vertex9 = Vertex.Vertex(9)
vertex9.distribution = {1: 0.3575, 0: 0.6425}
vertex1.neighbours = [vertex2, vertex4]
vertex2.neighbours = [vertex3, vertex1, vertex5]
vertex3.neighbours = [vertex2, vertex6]
vertex4.neighbours = [vertex5, vertex7, vertex1]
vertex5.neighbours = [vertex6, vertex4, vertex8, vertex2]
vertex6.neighbours = [vertex5, vertex9, vertex3]
vertex7.neighbours = [vertex8, vertex4]
vertex8.neighbours = [vertex9, vertex7, vertex5]
vertex9.neighbours = [vertex8, vertex6]
agent0 = Agent.Agent(0, vertex1, 3, 3)
agent1 = Agent.Agent(1, vertex1, 3, 6)
agent2 = Agent.Agent(2, vertex1, 4, 6)
map1 = [
        vertex1, vertex2, vertex3, 
        vertex4, vertex5, vertex6, 
        vertex7, vertex8, vertex9, ]
agents = [agent0, agent1, agent2]
instance1 = Instance.Instance("i_3_3_3_3_6_FR", map1, agents, 4)
