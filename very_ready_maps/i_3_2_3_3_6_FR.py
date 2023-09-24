import Instance 
import Vertex
import Agent
vertex1 = Vertex.Vertex(1)
vertex1.distribution = {1: 0.4755, 0: 0.5245}
vertex2 = Vertex.Vertex(2)
vertex2.distribution = {1: 0.004, 0: 0.996}
vertex3 = Vertex.Vertex(3)
vertex3.distribution = {1: 0.754, 0: 0.246}
vertex4 = Vertex.Vertex(4)
vertex4.distribution = {1: 0.2458, 0: 0.7542}
vertex5 = Vertex.Vertex(5)
vertex5.distribution = {1: 0.0455, 0: 0.9545}
vertex6 = Vertex.Vertex(6)
vertex6.distribution = {1: 0.0037, 0: 0.9963}
vertex1.neighbours = [vertex2, vertex4]
vertex2.neighbours = [vertex3, vertex1, vertex5]
vertex3.neighbours = [vertex2, vertex6]
vertex4.neighbours = [vertex5, vertex1]
vertex5.neighbours = [vertex6, vertex4, vertex2]
vertex6.neighbours = [vertex5, vertex3]
agent0 = Agent.Agent(0, vertex1, 6, 5)
agent1 = Agent.Agent(1, vertex1, 4, 3)
agent2 = Agent.Agent(2, vertex1, 3, 3)
map1 = [
        vertex1, vertex2, vertex3, 
        vertex4, vertex5, vertex6, ]
agents = [agent0, agent1, agent2]
instance1 = Instance.Instance("i_3_2_3_3_6_FR", map1, agents, 6)
