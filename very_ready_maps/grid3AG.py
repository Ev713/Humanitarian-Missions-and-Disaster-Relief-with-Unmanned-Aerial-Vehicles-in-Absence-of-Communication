import Instance 
import Vertex
import Agent
vertex1 = Vertex.Vertex(1)
vertex1.distribution = {0: 1}
vertex2 = Vertex.Vertex(2)
vertex2.distribution = {1: 1}
vertex3 = Vertex.Vertex(3)
vertex3.distribution = {1: 1}
vertex4 = Vertex.Vertex(4)
vertex4.distribution = {1: 1}
vertex5 = Vertex.Vertex(5)
vertex5.distribution = {1: 1}
vertex6 = Vertex.Vertex(6)
vertex6.distribution = {0: 1}
vertex7 = Vertex.Vertex(7)
vertex7.distribution = {1: 1}
vertex8 = Vertex.Vertex(8)
vertex8.distribution = {1: 1}
vertex9 = Vertex.Vertex(9)
vertex9.distribution = {70: 0.1, 0: 0.9}
vertex1.neighbours = [vertex2, vertex4]
vertex2.neighbours = [vertex3, vertex1, vertex5]
vertex3.neighbours = [vertex2, vertex6]
vertex4.neighbours = [vertex5, vertex7, vertex1]
vertex5.neighbours = [vertex6, vertex4, vertex8, vertex2]
vertex6.neighbours = [vertex5, vertex9, vertex3]
vertex7.neighbours = [vertex8, vertex4]
vertex8.neighbours = [vertex9, vertex7, vertex5]
vertex9.neighbours = [vertex8, vertex6]
agent0 = Agent.Agent(0, vertex1, 4, 3)
map1 = [
        vertex1, vertex2, vertex3, 
        vertex4, vertex5, vertex6, 
        vertex7, vertex8, vertex9, ]
agents = [agent0]
instance1 = Instance.Instance("grid3AG", map1, agents, 4)
