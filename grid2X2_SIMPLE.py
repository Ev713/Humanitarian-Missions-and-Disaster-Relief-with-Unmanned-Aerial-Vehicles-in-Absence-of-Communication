import Instance 
import Vertex
import Agent
vertex0 = Vertex.Vertex(0)
vertex0.distribution = {1: 0, 0: 1}
vertex1 = Vertex.Vertex(1)
vertex1.distribution = {1: 1.0, 0: 0.0}
vertex2 = Vertex.Vertex(2)
vertex2.distribution = {1: 1.0, 0: 0.0}
vertex3 = Vertex.Vertex(3)
vertex3.distribution = {0: 1}
vertex0.neighbours = [vertex2, vertex1]
vertex1.neighbours = [vertex0, vertex3]
vertex2.neighbours = [vertex0, vertex3]
vertex3.neighbours = [vertex1, vertex2]
agent0 = Agent.Agent(0, vertex0, 3, 1)
agent1 = Agent.Agent(1, vertex3, 3, 1)
map1 = [vertex0, vertex1, 
        vertex2, vertex3]
agents = [agent0, agent1]
instance1 = Instance.Instance(map1, agents, 3)
