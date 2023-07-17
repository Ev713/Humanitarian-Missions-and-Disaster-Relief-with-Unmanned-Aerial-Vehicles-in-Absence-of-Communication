import Instance 
import Vertex
import Agent
vertex0 = Vertex.Vertex(0)
vertex0.distribution = {3: 0.9, 0: 0.1}
vertex1 = Vertex.Vertex(1)
vertex1.distribution = {10: 1}
vertex2 = Vertex.Vertex(2)
vertex2.distribution = {1: 0.8, 0: 0.2}
vertex3 = Vertex.Vertex(3)
vertex3.distribution = {10: 1}
vertex4 = Vertex.Vertex(4)
vertex4.distribution = {10: 1}
vertex5 = Vertex.Vertex(5)
vertex5.distribution = {10: 1}
vertex0.neighbours = [vertex3, vertex1]
vertex1.neighbours = [vertex0, vertex4]
vertex3.neighbours = [vertex0, vertex6, vertex4]
vertex4.neighbours = [vertex1, vertex3, vertex7]
vertex6.neighbours = [vertex3, vertex7]
vertex7.neighbours = [vertex4, vertex6]
agent0 = Agent.Agent(0, vertex0, 2.6666666666666665, 4)
map1 = [vertex0, vertex1, vertex2, 
        vertex3, vertex4, vertex5]
agents = [agent0]
instance1 = Instance.Instance(map1, agents, 4)
