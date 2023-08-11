import Instance 
import Vertex
import Agent
vertex1 = Vertex.Vertex(1)
vertex1.distribution = {0: 1}
vertex1.neighbours = []
agent0 = Agent.Agent(0, vertex1, 4, 3)
agent1 = Agent.Agent(1, vertex1, 4, 3)
map1 = [vertex1]
agents = [agent0, agent1]
instance1 = Instance.Instance(map1, agents, 4)
