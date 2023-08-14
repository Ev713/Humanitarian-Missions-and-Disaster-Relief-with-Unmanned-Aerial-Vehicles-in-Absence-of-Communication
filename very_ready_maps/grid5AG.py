import Instance 
import Vertex
import Agent
vertex1 = Vertex.Vertex(1)
vertex1.distribution = {0: 1}
vertex2 = Vertex.Vertex(2)
vertex2.distribution = {0: 1}
vertex3 = Vertex.Vertex(3)
vertex3.distribution = {1: 1}
vertex4 = Vertex.Vertex(4)
vertex4.distribution = {1: 1}
vertex5 = Vertex.Vertex(5)
vertex5.distribution = {0: 1}
vertex6 = Vertex.Vertex(6)
vertex6.distribution = {1: 1}
vertex7 = Vertex.Vertex(7)
vertex7.distribution = {1: 1}
vertex8 = Vertex.Vertex(8)
vertex8.distribution = {1: 1}
vertex9 = Vertex.Vertex(9)
vertex9.distribution = {0: 1}
vertex10 = Vertex.Vertex(10)
vertex10.distribution = {0: 1}
vertex11 = Vertex.Vertex(11)
vertex11.distribution = {1: 1}
vertex12 = Vertex.Vertex(12)
vertex12.distribution = {0: 1}
vertex13 = Vertex.Vertex(13)
vertex13.distribution = {0: 1}
vertex14 = Vertex.Vertex(14)
vertex14.distribution = {0: 1}
vertex15 = Vertex.Vertex(15)
vertex15.distribution = {0: 1}
vertex16 = Vertex.Vertex(16)
vertex16.distribution = {0: 1}
vertex17 = Vertex.Vertex(17)
vertex17.distribution = {0: 1}
vertex18 = Vertex.Vertex(18)
vertex18.distribution = {0: 1}
vertex19 = Vertex.Vertex(19)
vertex19.distribution = {0: 1}
vertex20 = Vertex.Vertex(20)
vertex20.distribution = {0: 1}
vertex21 = Vertex.Vertex(21)
vertex21.distribution = {0: 1}
vertex22 = Vertex.Vertex(22)
vertex22.distribution = {0: 1}
vertex23 = Vertex.Vertex(23)
vertex23.distribution = {0: 1}
vertex24 = Vertex.Vertex(24)
vertex24.distribution = {0: 1}
vertex25 = Vertex.Vertex(25)
vertex25.distribution = {7: 1}
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
vertex16.neighbours = [vertex17, vertex21, vertex11]
vertex17.neighbours = [vertex18, vertex16, vertex22, vertex12]
vertex18.neighbours = [vertex19, vertex17, vertex23, vertex13]
vertex19.neighbours = [vertex20, vertex18, vertex24, vertex14]
vertex20.neighbours = [vertex19, vertex25, vertex15]
vertex21.neighbours = [vertex22, vertex16]
vertex22.neighbours = [vertex23, vertex21, vertex17]
vertex23.neighbours = [vertex24, vertex22, vertex18]
vertex24.neighbours = [vertex25, vertex23, vertex19]
vertex25.neighbours = [vertex24, vertex20]
agent0 = Agent.Agent(0, vertex1, 6, 2)
agent1 = Agent.Agent(1, vertex1, 7, 1)
map1 = [
        vertex1 , vertex2 , vertex3 , vertex4 , vertex5 , 
        vertex6 , vertex7 , vertex8 , vertex9 , vertex10, 
        vertex11, vertex12, vertex13, vertex14, vertex15, 
        vertex16, vertex17, vertex18, vertex19, vertex20, 
        vertex21, vertex22, vertex23, vertex24, vertex25, ]
agents = [agent0, agent1]
instance1 = Instance.Instance("grid5AG", map1, agents, 7)
