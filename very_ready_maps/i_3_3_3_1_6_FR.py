import Instance 
import Vertex
import Agent
vertex1 = Vertex.Vertex(1)
vertex1.distribution = {1: 0.1001, 0: 0.8999}
vertex2 = Vertex.Vertex(2)
vertex2.distribution = {1: 0.39, 0: 0.61}
vertex3 = Vertex.Vertex(3)
vertex3.distribution = {1: 0.5279, 0: 0.4721}
vertex4 = Vertex.Vertex(4)
vertex4.distribution = {1: 0.7146, 0: 0.2854}
vertex5 = Vertex.Vertex(5)
vertex5.distribution = {1: 0.6944, 0: 0.3056}
vertex6 = Vertex.Vertex(6)
vertex6.distribution = {1: 0.1904, 0: 0.8096}
vertex7 = Vertex.Vertex(7)
vertex7.distribution = {1: 0.5688, 0: 0.4312}
vertex8 = Vertex.Vertex(8)
vertex8.distribution = {1: 0.4859, 0: 0.5141}
vertex9 = Vertex.Vertex(9)
vertex9.distribution = {1: 0.7833, 0: 0.2167}
vertex1.neighbours = [vertex2, vertex4]
vertex2.neighbours = [vertex3, vertex1, vertex5]
vertex3.neighbours = [vertex2, vertex6]
vertex4.neighbours = [vertex5, vertex7, vertex1]
vertex5.neighbours = [vertex6, vertex4, vertex8, vertex2]
vertex6.neighbours = [vertex5, vertex9, vertex3]
vertex7.neighbours = [vertex8, vertex4]
vertex8.neighbours = [vertex9, vertex7, vertex5]
vertex9.neighbours = [vertex8, vertex6]
agent0 = Agent.Agent(0, vertex1, 3, 3)
map1 = [
        vertex1, vertex2, vertex3, 
        vertex4, vertex5, vertex6, 
        vertex7, vertex8, vertex9, ]
agents = [agent0]
instance1 = Instance.Instance("i_3_3_3_1_6_FR", map1, agents, 3)
