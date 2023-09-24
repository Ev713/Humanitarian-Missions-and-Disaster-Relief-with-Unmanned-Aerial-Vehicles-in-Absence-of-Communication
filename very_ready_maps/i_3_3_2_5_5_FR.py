import Instance 
import Vertex
import Agent
vertex1 = Vertex.Vertex(1)
vertex1.distribution = {1: 0.3704, 0: 0.6296}
vertex2 = Vertex.Vertex(2)
vertex2.distribution = {1: 0.9906, 0: 0.0094}
vertex3 = Vertex.Vertex(3)
vertex3.distribution = {1: 0.914, 0: 0.086}
vertex4 = Vertex.Vertex(4)
vertex4.distribution = {1: 0.7716, 0: 0.2284}
vertex5 = Vertex.Vertex(5)
vertex5.distribution = {1: 0.561, 0: 0.439}
vertex6 = Vertex.Vertex(6)
vertex6.distribution = {1: 0.4469, 0: 0.5531}
vertex1.neighbours = [vertex2, vertex3]
vertex2.neighbours = [vertex1, vertex4]
vertex3.neighbours = [vertex4, vertex5, vertex1]
vertex4.neighbours = [vertex3, vertex6, vertex2]
vertex5.neighbours = [vertex6, vertex3]
vertex6.neighbours = [vertex5, vertex4]
agent0 = Agent.Agent(0, vertex1, 4, 4)
agent1 = Agent.Agent(1, vertex1, 3, 3)
agent2 = Agent.Agent(2, vertex1, 4, 4)
agent3 = Agent.Agent(3, vertex1, 5, 4)
agent4 = Agent.Agent(4, vertex1, 5, 3)
map1 = [
        vertex1, vertex2, 
        vertex3, vertex4, 
        vertex5, vertex6, ]
agents = [agent0, agent1, agent2, agent3, agent4]
instance1 = Instance.Instance("i_3_3_2_5_5_FR", map1, agents, 5)
