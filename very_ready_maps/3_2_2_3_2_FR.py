import Instance 
import Vertex
import Agent
vertex1 = Vertex.Vertex(1)
vertex1.distribution = {1: 0.126, 0: 0.874}
vertex2 = Vertex.Vertex(2)
vertex2.distribution = {1: 0.2331, 0: 0.7669}
vertex3 = Vertex.Vertex(3)
vertex3.distribution = {1: 0.6604, 0: 0.3396}
vertex4 = Vertex.Vertex(4)
vertex4.distribution = {1: 0.8543, 0: 0.1457}
vertex1.neighbours = [vertex2, vertex3]
vertex2.neighbours = [vertex1, vertex4]
vertex3.neighbours = [vertex4, vertex1]
vertex4.neighbours = [vertex3, vertex2]
agent0 = Agent.Agent(0, vertex1, 2, 3)
agent1 = Agent.Agent(1, vertex1, 2, 3)
agent2 = Agent.Agent(2, vertex1, 2, 3)
map1 = [
        vertex1, vertex2, 
        vertex3, vertex4, ]
agents = [agent0, agent1, agent2]
instance1 = Instance.Instance("3_2_2_3_2_FR", map1, agents, 2)
