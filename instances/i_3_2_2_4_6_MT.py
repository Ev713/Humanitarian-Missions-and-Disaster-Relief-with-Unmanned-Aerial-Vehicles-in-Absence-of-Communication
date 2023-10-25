import Instance 
import Vertex
import Agent
vertex1 = Vertex.Vertex(1)
vertex1.distribution = {1: 0.0625, 0: 0.9375}
vertex2 = Vertex.Vertex(2)
vertex2.distribution = {1: 0.0156, 0: 0.9844}
vertex3 = Vertex.Vertex(3)
vertex3.distribution = {1: 0.25, 0: 0.75}
vertex4 = Vertex.Vertex(4)
vertex4.distribution = {1: 0.0625, 0: 0.9375}
vertex1.neighbours = [vertex2, vertex3]
vertex2.neighbours = [vertex1, vertex4]
vertex3.neighbours = [vertex4, vertex1]
vertex4.neighbours = [vertex3, vertex2]
agent0 = Agent.Agent(0, vertex1, 4, 3)
agent1 = Agent.Agent(1, vertex1, 4, 5)
agent2 = Agent.Agent(2, vertex1, 6, 3)
agent3 = Agent.Agent(3, vertex1, 3, 5)
map1 = [
        vertex1, vertex2, 
        vertex3, vertex4, ]
agents = [agent0, agent1, agent2, agent3]
instance1 = Instance.Instance("i_3_2_2_4_6_MT", map1, agents, 6)
