import Instance 
import Vertex
import Agent
vertex7 = Vertex.Vertex(7)
vertex7.distribution = {1: 0.12, 0: 0.88}
vertex8 = Vertex.Vertex(8)
vertex8.distribution = {1: 0.25, 0: 0.75}
vertex9 = Vertex.Vertex(9)
vertex9.distribution = {1: 0.12, 0: 0.88}
vertex10 = Vertex.Vertex(10)
vertex10.distribution = {1: 0.06, 0: 0.94}
vertex12 = Vertex.Vertex(12)
vertex12.distribution = {1: 0.25, 0: 0.75}
vertex13 = Vertex.Vertex(13)
vertex13.distribution = {1: 0.5, 0: 0.5}
vertex14 = Vertex.Vertex(14)
vertex14.distribution = {1: 0.25, 0: 0.75}
vertex15 = Vertex.Vertex(15)
vertex15.distribution = {1: 0.12, 0: 0.88}
vertex18 = Vertex.Vertex(18)
vertex18.distribution = {1: 0.25, 0: 0.75}
vertex19 = Vertex.Vertex(19)
vertex19.distribution = {1: 0.12, 0: 0.88}
vertex23 = Vertex.Vertex(23)
vertex23.distribution = {1: 0.12, 0: 0.88}
vertex27 = Vertex.Vertex(27)
vertex27.distribution = {1: 0.25, 0: 0.75}
vertex28 = Vertex.Vertex(28)
vertex28.distribution = {1: 0.12, 0: 0.88}
vertex32 = Vertex.Vertex(32)
vertex32.distribution = {1: 0.5, 0: 0.5}
vertex33 = Vertex.Vertex(33)
vertex33.distribution = {1: 0.25, 0: 0.75}
vertex37 = Vertex.Vertex(37)
vertex37.distribution = {1: 0.25, 0: 0.75}
vertex38 = Vertex.Vertex(38)
vertex38.distribution = {1: 0.12, 0: 0.88}
vertex7.neighbours = [vertex8, vertex12]
vertex8.neighbours = [vertex9, vertex7, vertex13]
vertex9.neighbours = [vertex10, vertex8, vertex14]
vertex10.neighbours = [vertex9, vertex15]
vertex12.neighbours = [vertex13, vertex7]
vertex13.neighbours = [vertex14, vertex12, vertex18, vertex8]
vertex14.neighbours = [vertex15, vertex13, vertex19, vertex9]
vertex15.neighbours = [vertex14, vertex10]
vertex18.neighbours = [vertex19, vertex23, vertex13]
vertex19.neighbours = [vertex18, vertex14]
vertex23.neighbours = [vertex28, vertex18]
vertex27.neighbours = [vertex28, vertex32]
vertex28.neighbours = [vertex27, vertex33, vertex23]
vertex32.neighbours = [vertex33, vertex37, vertex27]
vertex33.neighbours = [vertex32, vertex38, vertex28]
vertex37.neighbours = [vertex38, vertex32]
vertex38.neighbours = [vertex37, vertex33]
agent0 = Agent.Agent(0, vertex7, 6, 4)
agent1 = Agent.Agent(1, vertex7, 6, 4)
map1 = [
                                                          
                  vertex7 , vertex8 , vertex9 , vertex10, 
                  vertex12, vertex13, vertex14, vertex15, 
                            vertex18, vertex19,           
                            vertex23,                     
                  vertex27, vertex28,                     
                  vertex32, vertex33,                     
                  vertex37, vertex38,                     ]
agents = [agent0, agent1]
instance1 = Instance.Instance(map1, agents, 6)
