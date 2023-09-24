import Instance 
import Vertex
import Agent
vertex1 = Vertex.Vertex(1)
vertex1.distribution = {1: 0.0917, 0: 0.9083}
vertex2 = Vertex.Vertex(2)
vertex2.distribution = {1: 0.2208, 0: 0.7792}
vertex3 = Vertex.Vertex(3)
vertex3.distribution = {1: 0.3534, 0: 0.6466}
vertex4 = Vertex.Vertex(4)
vertex4.distribution = {1: 0.0657, 0: 0.9343}
vertex5 = Vertex.Vertex(5)
vertex5.distribution = {1: 0.0613, 0: 0.9387}
vertex6 = Vertex.Vertex(6)
vertex6.distribution = {1: 0.4299, 0: 0.5701}
vertex7 = Vertex.Vertex(7)
vertex7.distribution = {1: 0.2486, 0: 0.7514}
vertex8 = Vertex.Vertex(8)
vertex8.distribution = {1: 0.0556, 0: 0.9444}
vertex9 = Vertex.Vertex(9)
vertex9.distribution = {1: 0.0949, 0: 0.9051}
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
instance1 = Instance.Instance("i_3_3_3_1_6_FR", map1, agents, 4)
