import Instance 
import Vertex
import Agent
vertex0 = Vertex.Vertex(0)
vertex0.distribution = {0: 1}
vertex1 = Vertex.Vertex(1)
vertex1.distribution = {0: 1}
vertex2 = Vertex.Vertex(2)
vertex2.distribution = {0: 1}
vertex3 = Vertex.Vertex(3)
vertex3.distribution = {0: 1}
vertex4 = Vertex.Vertex(4)
vertex4.distribution = {0: 1}
vertex5 = Vertex.Vertex(5)
vertex5.distribution = {0: 1}
vertex6 = Vertex.Vertex(6)
vertex6.distribution = {0: 1}
vertex7 = Vertex.Vertex(7)
vertex7.distribution = {4: 0.397, 0: 0.603}
vertex8 = Vertex.Vertex(8)
vertex8.distribution = {2: 0.677, 0: 0.32299999999999995}
vertex0.neighbours = [vertex3, vertex1]
vertex1.neighbours = [vertex0, vertex4, vertex2]
vertex2.neighbours = [vertex1, vertex5]
vertex3.neighbours = [vertex0, vertex6, vertex4]
vertex4.neighbours = [vertex1, vertex3, vertex7, vertex5]
vertex5.neighbours = [vertex2, vertex4, vertex8]
vertex6.neighbours = [vertex3, vertex7]
vertex7.neighbours = [vertex4, vertex6, vertex8]
vertex8.neighbours = [vertex5, vertex7]
agent0 = Agent.Agent(0, vertex0, 3, 3)
agent1 = Agent.Agent(1, vertex0, 3, 3)
map1 = [vertex0, vertex1, vertex2, 
        vertex3, vertex4, vertex5, 
        vertex6, vertex7, vertex8]
agents = [agent0, agent1]
instance1 = Instance.Instance(map1, agents, 3)
