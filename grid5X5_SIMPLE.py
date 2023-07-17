import Instance 
import Vertex
import Agent
vertex0 = Vertex.Vertex(0)
vertex0.distribution = {4: 0.5, 0: 0.5}
vertex1 = Vertex.Vertex(1)
vertex1.distribution = {3: 0.2, 0: 0.8}
vertex2 = Vertex.Vertex(2)
vertex2.distribution = {0: 1}
vertex3 = Vertex.Vertex(3)
vertex3.distribution = {3: 0.2, 0: 0.8}
vertex4 = Vertex.Vertex(4)
vertex4.distribution = {3: 0.5, 0: 0.5}
vertex5 = Vertex.Vertex(5)
vertex5.distribution = {0: 1}
vertex6 = Vertex.Vertex(6)
vertex6.distribution = {4: 0.8, 0: 0.19999999999999996}
vertex7 = Vertex.Vertex(7)
vertex7.distribution = {2: 0.6, 0: 0.4}
vertex8 = Vertex.Vertex(8)
vertex8.distribution = {3: 0.7, 0: 0.30000000000000004}
vertex9 = Vertex.Vertex(9)
vertex9.distribution = {0: 1}
vertex10 = Vertex.Vertex(10)
vertex10.distribution = {2: 0.9, 0: 0.09999999999999998}
vertex11 = Vertex.Vertex(11)
vertex11.distribution = {3: 0.7, 0: 0.30000000000000004}
vertex12 = Vertex.Vertex(12)
vertex12.distribution = {0: 1}
vertex13 = Vertex.Vertex(13)
vertex13.distribution = {0: 1}
vertex14 = Vertex.Vertex(14)
vertex14.distribution = {4: 0.8, 0: 0.19999999999999996}
vertex15 = Vertex.Vertex(15)
vertex15.distribution = {1: 0.7, 0: 0.30000000000000004}
vertex16 = Vertex.Vertex(16)
vertex16.distribution = {2: 0.2, 0: 0.8}
vertex17 = Vertex.Vertex(17)
vertex17.distribution = {4: 0.1, 0: 0.9}
vertex18 = Vertex.Vertex(18)
vertex18.distribution = {2: 0.7, 0: 0.30000000000000004}
vertex19 = Vertex.Vertex(19)
vertex19.distribution = {2: 0.5, 0: 0.5}
vertex20 = Vertex.Vertex(20)
vertex20.distribution = {2: 0.2, 0: 0.8}
vertex21 = Vertex.Vertex(21)
vertex21.distribution = {1: 1.0, 0: 0.0}
vertex22 = Vertex.Vertex(22)
vertex22.distribution = {3: 0.6, 0: 0.4}
vertex23 = Vertex.Vertex(23)
vertex23.distribution = {1: 0.3, 0: 0.7}
vertex24 = Vertex.Vertex(24)
vertex24.distribution = {1: 0.4, 0: 0.6}
vertex0.neighbours = [vertex5, vertex1]
vertex1.neighbours = [vertex0, vertex6, vertex2]
vertex2.neighbours = [vertex1, vertex7, vertex3]
vertex3.neighbours = [vertex2, vertex8, vertex4]
vertex4.neighbours = [vertex3, vertex9]
vertex5.neighbours = [vertex0, vertex10, vertex6]
vertex6.neighbours = [vertex1, vertex5, vertex11, vertex7]
vertex7.neighbours = [vertex2, vertex6, vertex12, vertex8]
vertex8.neighbours = [vertex3, vertex7, vertex13, vertex9]
vertex9.neighbours = [vertex4, vertex8, vertex14]
vertex10.neighbours = [vertex5, vertex15, vertex11]
vertex11.neighbours = [vertex6, vertex10, vertex16, vertex12]
vertex12.neighbours = [vertex7, vertex11, vertex17, vertex13]
vertex13.neighbours = [vertex8, vertex12, vertex18, vertex14]
vertex14.neighbours = [vertex9, vertex13, vertex19]
vertex15.neighbours = [vertex10, vertex20, vertex16]
vertex16.neighbours = [vertex11, vertex15, vertex21, vertex17]
vertex17.neighbours = [vertex12, vertex16, vertex22, vertex18]
vertex18.neighbours = [vertex13, vertex17, vertex23, vertex19]
vertex19.neighbours = [vertex14, vertex18, vertex24]
vertex20.neighbours = [vertex15, vertex21]
vertex21.neighbours = [vertex16, vertex20, vertex22]
vertex22.neighbours = [vertex17, vertex21, vertex23]
vertex23.neighbours = [vertex18, vertex22, vertex24]
vertex24.neighbours = [vertex19, vertex23]
agent0 = Agent.Agent(0, vertex0, 4, 4)
agent1 = Agent.Agent(1, vertex0, 4, 4)
map1 = [vertex0, vertex1, vertex2, vertex3, vertex4, 
        vertex5, vertex6, vertex7, vertex8, vertex9, 
        vertex10, vertex11, vertex12, vertex13, vertex14, 
        vertex15, vertex16, vertex17, vertex18, vertex19, 
        vertex20, vertex21, vertex22, vertex23, vertex24]
agents = [agent0, agent1]
instance1 = Instance.Instance(map1, agents, 4)
