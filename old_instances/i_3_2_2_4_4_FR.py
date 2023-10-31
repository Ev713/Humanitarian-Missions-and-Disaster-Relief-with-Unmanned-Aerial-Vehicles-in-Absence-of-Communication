import Instance 
import Vertex
import Agent
vertex1 = Vertex.Vertex(1)
vertex1.distribution = {1: 0.7993, 0: 0.2007}
vertex2 = Vertex.Vertex(2)
vertex2.distribution = {1: 0.1495, 0: 0.8505}
vertex3 = Vertex.Vertex(3)
vertex3.distribution = {1: 0.2543, 0: 0.7457}
vertex4 = Vertex.Vertex(4)
vertex4.distribution = {1: 0.361, 0: 0.639}
vertex1.neighbours = [vertex2, vertex3]
vertex2.neighbours = [vertex1, vertex4]
vertex3.neighbours = [vertex4, vertex1]
vertex4.neighbours = [vertex3, vertex2]
agent0 = Agent.Agent(0, vertex1, 4, 4)
agent1 = Agent.Agent(1, vertex1, 2, 3)
agent2 = Agent.Agent(2, vertex1, 2, 3)
agent3 = Agent.Agent(3, vertex1, 3, 3)
map1 = [
        vertex1, vertex2, 
        vertex3, vertex4, ]
agents = [agent0, agent1, agent2, agent3]
instance1 = Instance.Instance("i_3_2_2_4_4_FR", map1, agents, 4)
