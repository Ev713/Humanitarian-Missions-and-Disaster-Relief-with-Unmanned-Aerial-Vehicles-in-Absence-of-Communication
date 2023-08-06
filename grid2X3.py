import Instance 
import Vertex
import Agent
vertex0 = Vertex.Vertex(0)
vertex0.distribution = {0: 0.9, 1:0.1}
vertex1 = Vertex.Vertex(1)
vertex1.distribution = {0: 0.9, 1:0.1}
vertex2 = Vertex.Vertex(2)
vertex2.distribution = {0: 0.9, 1:0.1}
vertex3 = Vertex.Vertex(3)
vertex3.distribution = {0: 0.9, 1:0.1}
vertex4 = Vertex.Vertex(4)
vertex4.distribution = {0: 0.9, 1:0.1}
vertex5 = Vertex.Vertex(5)
vertex5.distribution = {6: 1}

vertex0.neighbours = [vertex3, vertex1]
vertex1.neighbours = [vertex0, vertex2, vertex4]
vertex2.neighbours = [vertex1, vertex5]
vertex3.neighbours = [vertex0, vertex4]
vertex4.neighbours = [vertex1, vertex3, vertex5]
vertex5.neighbours = [vertex3, vertex5]

agent0 = Agent.Agent(0, vertex0, 4, 3)
agent1 = Agent.Agent(1, vertex0, 4, 3)

map1 = [vertex0, vertex1, vertex2, 
        vertex3, vertex4, vertex5]
agents = [agent0, agent1]
instance1 = Instance.Instance(map1, agents, 5)
