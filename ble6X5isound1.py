import Instance 
import Vertex
import Agent
vertex7 = Vertex.Vertex(7)
vertex7.distribution = {0: 1}
vertex8 = Vertex.Vertex(8)
vertex8.distribution = {0: 1}
vertex10 = Vertex.Vertex(10)
vertex10.distribution = {0: 1}
vertex12 = Vertex.Vertex(12)
vertex12.distribution = {0: 1}
vertex13 = Vertex.Vertex(13)
vertex13.distribution = {0: 1}
vertex15 = Vertex.Vertex(15)
vertex15.distribution = {0: 1}
vertex17 = Vertex.Vertex(17)
vertex17.distribution = {0: 1}
vertex18 = Vertex.Vertex(18)
vertex18.distribution = {0: 1}
vertex22 = Vertex.Vertex(22)
vertex22.distribution = {0: 1}
vertex23 = Vertex.Vertex(23)
vertex23.distribution = {0: 1}
vertex25 = Vertex.Vertex(25)
vertex25.distribution = {0: 1}
vertex27 = Vertex.Vertex(27)
vertex27.distribution = {0: 1}
vertex28 = Vertex.Vertex(28)
vertex28.distribution = {0: 1}
vertex30 = Vertex.Vertex(30)
vertex30.distribution = {0: 1}
vertex7.neighbours = [vertex8, vertex12]
vertex8.neighbours = [vertex7, vertex13]
vertex10.neighbours = [vertex15]
vertex12.neighbours = [vertex13, vertex17, vertex7]
vertex13.neighbours = [vertex12, vertex18, vertex8]
vertex15.neighbours = [vertex10]
vertex17.neighbours = [vertex18, vertex22, vertex12]
vertex18.neighbours = [vertex17, vertex23, vertex13]
vertex22.neighbours = [vertex23, vertex27, vertex17]
vertex23.neighbours = [vertex22, vertex28, vertex18]
vertex25.neighbours = [vertex30]
vertex27.neighbours = [vertex28, vertex22]
vertex28.neighbours = [vertex27, vertex23]
vertex30.neighbours = [vertex25]
agent0 = Agent.Agent(0, vertex7, 6, 3)
agent1 = Agent.Agent(1, vertex7, 6, 3)
map1 = [vertex7, vertex8, vertex10, vertex12, vertex13, 
        vertex15, vertex17, vertex18, vertex22, vertex23, 
        vertex25, vertex27, vertex28, vertex30]
agents = [agent0, agent1]
instance1 = Instance.Instance(map1, agents, 6)
'''
■■■■■■
■  ■ ■
■  ■ ■
■  ■■■
■  ■ ■
■  ■ ■

'''