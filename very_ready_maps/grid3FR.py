import Instance 
import Vertex
import Agent
vertex1 = Vertex.Vertex(1)
vertex1.distribution = {1: 0.4289, 0: 0.5711}
vertex2 = Vertex.Vertex(2)
vertex2.distribution = {1: 0.7974, 0: 0.2026}
vertex3 = Vertex.Vertex(3)
vertex3.distribution = {1: 0.7824, 0: 0.2176}
vertex4 = Vertex.Vertex(4)
vertex4.distribution = {1: 0.1351, 0: 0.8649}
vertex5 = Vertex.Vertex(5)
vertex5.distribution = {1: 0.4124, 0: 0.5876}
vertex6 = Vertex.Vertex(6)
vertex6.distribution = {1: 0.4826, 0: 0.5174}
vertex7 = Vertex.Vertex(7)
vertex7.distribution = {1: 0.1992, 0: 0.8008}
vertex8 = Vertex.Vertex(8)
vertex8.distribution = {1: 0.6513, 0: 0.3487}
vertex9 = Vertex.Vertex(9)
vertex9.distribution = {1: 0.0193, 0: 0.9807}
vertex10 = Vertex.Vertex(10)
vertex10.distribution = {1: 0.3918, 0: 0.6082}
vertex11 = Vertex.Vertex(11)
vertex11.distribution = {1: 0.7148, 0: 0.2852}
vertex12 = Vertex.Vertex(12)
vertex12.distribution = {1: 0.0889, 0: 0.9111}
vertex1.neighbours = [vertex2, vertex5]
vertex2.neighbours = [vertex3, vertex1, vertex6]
vertex3.neighbours = [vertex4, vertex2, vertex7]
vertex4.neighbours = [vertex3, vertex8]
vertex5.neighbours = [vertex6, vertex9, vertex1]
vertex6.neighbours = [vertex7, vertex5, vertex10, vertex2]
vertex7.neighbours = [vertex8, vertex6, vertex11, vertex3]
vertex8.neighbours = [vertex7, vertex12, vertex4]
vertex9.neighbours = [vertex10, vertex5]
vertex10.neighbours = [vertex11, vertex9, vertex6]
vertex11.neighbours = [vertex12, vertex10, vertex7]
vertex12.neighbours = [vertex11, vertex8]
agent0 = Agent.Agent(0, vertex1, 6, 3)
map1 = [
        vertex1 , vertex2 , vertex3 , vertex4 , 
        vertex5 , vertex6 , vertex7 , vertex8 , 
        vertex9 , vertex10, vertex11, vertex12, ]
agents = [agent0]
instance1 = Instance.Instance("grid3FR", map1, agents, 6)
