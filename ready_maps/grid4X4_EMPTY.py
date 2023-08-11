import Instance 
import Vertex
import Agent
vertex0 = Vertex.Vertex(0)
vertex0.distribution = {0: 1}
vertex1 = Vertex.Vertex(1)
vertex1.distribution = {1: 1}
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
vertex7.distribution = {0: 1}
vertex8 = Vertex.Vertex(8)
vertex8.distribution = {0: 1}
vertex9 = Vertex.Vertex(9)
vertex9.distribution = {0: 1}
vertex10 = Vertex.Vertex(10)
vertex10.distribution = {0: 1}
vertex11 = Vertex.Vertex(11)
vertex11.distribution = {0: 1}
vertex12 = Vertex.Vertex(12)
vertex12.distribution = {100000: 0.00005, 0: 0.99995}
vertex13 = Vertex.Vertex(13)
vertex13.distribution = {0: 1}
vertex14 = Vertex.Vertex(14)
vertex14.distribution = {0: 1}
vertex15 = Vertex.Vertex(15)
vertex15.distribution = {0: 1}
vertex0.neighbours = [vertex4, vertex1]
vertex1.neighbours = [vertex0, vertex5, vertex2]
vertex2.neighbours = [vertex1, vertex6, vertex3]
vertex3.neighbours = [vertex2, vertex7]
vertex4.neighbours = [vertex0, vertex8, vertex5]
vertex5.neighbours = [vertex1, vertex4, vertex9, vertex6]
vertex6.neighbours = [vertex2, vertex5, vertex10, vertex7]
vertex7.neighbours = [vertex3, vertex6, vertex11]
vertex8.neighbours = [vertex4, vertex12, vertex9]
vertex9.neighbours = [vertex5, vertex8, vertex13, vertex10]
vertex10.neighbours = [vertex6, vertex9, vertex14, vertex11]
vertex11.neighbours = [vertex7, vertex10, vertex15]
vertex12.neighbours = [vertex8, vertex13]
vertex13.neighbours = [vertex9, vertex12, vertex14]
vertex14.neighbours = [vertex10, vertex13, vertex15]
vertex15.neighbours = [vertex11, vertex14]
agent0 = Agent.Agent(0, vertex0, 3, 2)
map1 = [vertex0, vertex1, vertex2, vertex3, 
        vertex4, vertex5, vertex6, vertex7, 
        vertex8, vertex9, vertex10, vertex11, 
        vertex12, vertex13, vertex14, vertex15]
agents = [agent0]
instance1 = Instance.Instance(map1, agents, 3)
