import Instance 
import Vertex
import Agent
vertex1 = Vertex.Vertex(1)
vertex1.distribution = {1: 0.1717, 0: 0.8283}
vertex2 = Vertex.Vertex(2)
vertex2.distribution = {1: 0.746, 0: 0.254}
vertex3 = Vertex.Vertex(3)
vertex3.distribution = {1: 0.0799, 0: 0.9201}
vertex4 = Vertex.Vertex(4)
vertex4.distribution = {1: 0.1599, 0: 0.8401}
vertex5 = Vertex.Vertex(5)
vertex5.distribution = {1: 0.2571, 0: 0.7429}
vertex6 = Vertex.Vertex(6)
vertex6.distribution = {1: 0.5585, 0: 0.4415}
vertex7 = Vertex.Vertex(7)
vertex7.distribution = {1: 0.1724, 0: 0.8276}
vertex8 = Vertex.Vertex(8)
vertex8.distribution = {1: 0.9412, 0: 0.0588}
vertex9 = Vertex.Vertex(9)
vertex9.distribution = {1: 0.8736, 0: 0.1264}
vertex10 = Vertex.Vertex(10)
vertex10.distribution = {1: 0.8463, 0: 0.1537}
vertex11 = Vertex.Vertex(11)
vertex11.distribution = {1: 0.1736, 0: 0.8264}
vertex12 = Vertex.Vertex(12)
vertex12.distribution = {1: 0.0117, 0: 0.9883}
vertex13 = Vertex.Vertex(13)
vertex13.distribution = {1: 0.2335, 0: 0.7665}
vertex14 = Vertex.Vertex(14)
vertex14.distribution = {1: 0.2561, 0: 0.7439}
vertex15 = Vertex.Vertex(15)
vertex15.distribution = {1: 0.0433, 0: 0.9567}
vertex16 = Vertex.Vertex(16)
vertex16.distribution = {1: 0.1712, 0: 0.8288}
vertex17 = Vertex.Vertex(17)
vertex17.distribution = {1: 0.8667, 0: 0.1333}
vertex18 = Vertex.Vertex(18)
vertex18.distribution = {1: 0.248, 0: 0.752}
vertex19 = Vertex.Vertex(19)
vertex19.distribution = {1: 0.1741, 0: 0.8259}
vertex20 = Vertex.Vertex(20)
vertex20.distribution = {1: 0.2205, 0: 0.7795}
vertex1.neighbours = [vertex2, vertex6]
vertex2.neighbours = [vertex3, vertex1, vertex7]
vertex3.neighbours = [vertex4, vertex2, vertex8]
vertex4.neighbours = [vertex5, vertex3, vertex9]
vertex5.neighbours = [vertex4, vertex10]
vertex6.neighbours = [vertex7, vertex11, vertex1]
vertex7.neighbours = [vertex8, vertex6, vertex12, vertex2]
vertex8.neighbours = [vertex9, vertex7, vertex13, vertex3]
vertex9.neighbours = [vertex10, vertex8, vertex14, vertex4]
vertex10.neighbours = [vertex9, vertex15, vertex5]
vertex11.neighbours = [vertex12, vertex16, vertex6]
vertex12.neighbours = [vertex13, vertex11, vertex17, vertex7]
vertex13.neighbours = [vertex14, vertex12, vertex18, vertex8]
vertex14.neighbours = [vertex15, vertex13, vertex19, vertex9]
vertex15.neighbours = [vertex14, vertex20, vertex10]
vertex16.neighbours = [vertex17, vertex11]
vertex17.neighbours = [vertex18, vertex16, vertex12]
vertex18.neighbours = [vertex19, vertex17, vertex13]
vertex19.neighbours = [vertex20, vertex18, vertex14]
vertex20.neighbours = [vertex19, vertex15]
agent0 = Agent.Agent(0, vertex1, 3, 4)
map1 = [
        vertex1 , vertex2 , vertex3 , vertex4 , vertex5 , 
        vertex6 , vertex7 , vertex8 , vertex9 , vertex10, 
        vertex11, vertex12, vertex13, vertex14, vertex15, 
        vertex16, vertex17, vertex18, vertex19, vertex20, ]
agents = [agent0]
instance1 = Instance.Instance("grid4FR", map1, agents, 3)
