import Instance 
import Vertex
import Agent
vertex0 = Vertex.Vertex(0)
vertex0.distribution = {2: 0.6, 0: 0.4}
vertex1 = Vertex.Vertex(1)
vertex1.distribution = {1: 0.5, 0: 0.5}
vertex2 = Vertex.Vertex(2)
vertex2.distribution = {4: 0.8, 0: 0.19999999999999996}
vertex0.neighbours = [vertex3]
vertex3.neighbours = [vertex0, vertex6]
vertex6.neighbours = [vertex3]
agent0 = Agent.Agent(0, vertex0, 4.0, 6)
map1 = [vertex0, vertex1, vertex2]
agents = [agent0]
instance1 = Instance.Instance(map1, agents, 6)
