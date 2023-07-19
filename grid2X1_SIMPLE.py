import Instance 
import Vertex
import Agent
vertex0 = Vertex.Vertex(0)
vertex0.distribution = {1: 0.4, 0: 0.6}
vertex1 = Vertex.Vertex(1)
vertex1.distribution = {3: 0.0, 0: 1.0}
vertex0.neighbours = [vertex1]
vertex1.neighbours = [vertex0]
agent0 = Agent.Agent(0, vertex0, 1, 2)
map1 = [vertex0, 
        vertex1]
agents = [agent0]
instance1 = Instance.Instance(map1, agents, 2)
