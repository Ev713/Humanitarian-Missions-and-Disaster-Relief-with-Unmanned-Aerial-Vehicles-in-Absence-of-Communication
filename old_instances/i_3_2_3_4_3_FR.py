import Instance 
import Vertex
import Agent
vertex1 = Vertex.Vertex(1)
vertex1.distribution = {1: 0.0668, 0: 0.9332}
vertex2 = Vertex.Vertex(2)
vertex2.distribution = {1: 0.3848, 0: 0.6152}
vertex3 = Vertex.Vertex(3)
vertex3.distribution = {1: 0.7849, 0: 0.2151}
vertex4 = Vertex.Vertex(4)
vertex4.distribution = {1: 0.9034, 0: 0.0966}
vertex5 = Vertex.Vertex(5)
vertex5.distribution = {1: 0.0738, 0: 0.9262}
vertex6 = Vertex.Vertex(6)
vertex6.distribution = {1: 0.3595, 0: 0.6405}
vertex1.neighbours = [vertex2, vertex4]
vertex2.neighbours = [vertex3, vertex1, vertex5]
vertex3.neighbours = [vertex2, vertex6]
vertex4.neighbours = [vertex5, vertex1]
vertex5.neighbours = [vertex6, vertex4, vertex2]
vertex6.neighbours = [vertex5, vertex3]
agent0 = Agent.Agent(0, vertex1, 2, 3)
agent1 = Agent.Agent(1, vertex1, 3, 3)
agent2 = Agent.Agent(2, vertex1, 2, 3)
agent3 = Agent.Agent(3, vertex1, 2, 3)
map1 = [
        vertex1, vertex2, vertex3, 
        vertex4, vertex5, vertex6, ]
agents = [agent0, agent1, agent2, agent3]
instance1 = Instance.Instance("i_3_2_3_4_3_FR", map1, agents, 3)
