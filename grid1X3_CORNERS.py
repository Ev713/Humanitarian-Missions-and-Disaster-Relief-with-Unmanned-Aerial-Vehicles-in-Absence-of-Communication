import Instance 
import Vertex
import Agent
vertex0 = Vertex.Vertex(0)
vertex0.distribution = {10: 1}
vertex1 = Vertex.Vertex(1)
vertex1.distribution = {10: 1}
vertex2 = Vertex.Vertex(2)
vertex2.distribution = {10: 1}
vertex0.neighbours = [vertex1]
vertex1.neighbours = [vertex0, vertex2]
vertex2.neighbours = [vertex1]
agent0 = Agent.Agent(0, vertex0, 4.0, 6)
map1 = [vertex0, vertex1, vertex2]
agents = [agent0]
instance1 = Instance.Instance(map1, agents, 6)
