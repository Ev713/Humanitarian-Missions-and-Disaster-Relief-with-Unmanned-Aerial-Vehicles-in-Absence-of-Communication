import Instance 
import Vertex
import Agent
vertex0 = Vertex.Vertex(0)
vertex0.distribution = {0: 1}
vertex5 = Vertex.Vertex(5)
vertex5.distribution = {1: 1, 0: 0}
vertex6 = Vertex.Vertex(6)
vertex6.distribution = {1: 1}
vertex7 = Vertex.Vertex(7)
vertex7.distribution = {1: 1}
vertex8 = Vertex.Vertex(8)
vertex8.distribution = {1: 1, 0: 0}
vertex9 = Vertex.Vertex(9)
vertex9.distribution = {1: 1, 0: 0}
vertex10 = Vertex.Vertex(10)
vertex10.distribution = {1: 1, 0: 0}
vertex15 = Vertex.Vertex(15)
vertex15.distribution = {0: 1}
vertex0.neighbours = [vertex5]
vertex5.neighbours = [vertex0, vertex10, vertex6]
vertex6.neighbours = [vertex5, vertex7]
vertex7.neighbours = [vertex6,  vertex8]
vertex8.neighbours = [ vertex7]
vertex10.neighbours = [vertex5, vertex15, ]
vertex15.neighbours = [vertex10]
agent0 = Agent.Agent(0, vertex0, 3, 2)
agent1 = Agent.Agent(1, vertex15, 3, 2)
map1 = [vertex0,
        vertex5, vertex6, vertex7, vertex8, vertex9, 
        vertex10,
        vertex15, ]
agents = [agent0, agent1]
instance1 = Instance.Instance(map1, agents, 3)
