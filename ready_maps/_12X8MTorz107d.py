import Instance 
import Vertex
import Agent
vertex10 = Vertex.Vertex(10)
vertex10.distribution = {1: 0.06, 0: 0.94}
vertex11 = Vertex.Vertex(11)
vertex11.distribution = {1: 0.12, 0: 0.88}
vertex12 = Vertex.Vertex(12)
vertex12.distribution = {1: 0.06, 0: 0.94}
vertex13 = Vertex.Vertex(13)
vertex13.distribution = {1: 0.03, 0: 0.97}
vertex18 = Vertex.Vertex(18)
vertex18.distribution = {1: 0.12, 0: 0.88}
vertex19 = Vertex.Vertex(19)
vertex19.distribution = {1: 0.25, 0: 0.75}
vertex20 = Vertex.Vertex(20)
vertex20.distribution = {1: 0.12, 0: 0.88}
vertex21 = Vertex.Vertex(21)
vertex21.distribution = {1: 0.06, 0: 0.94}
vertex23 = Vertex.Vertex(23)
vertex23.distribution = {1: 0.12, 0: 0.88}
vertex27 = Vertex.Vertex(27)
vertex27.distribution = {1: 0.12, 0: 0.88}
vertex28 = Vertex.Vertex(28)
vertex28.distribution = {1: 0.06, 0: 0.94}
vertex29 = Vertex.Vertex(29)
vertex29.distribution = {1: 0.06, 0: 0.94}
vertex30 = Vertex.Vertex(30)
vertex30.distribution = {1: 0.12, 0: 0.88}
vertex31 = Vertex.Vertex(31)
vertex31.distribution = {1: 0.25, 0: 0.75}
vertex32 = Vertex.Vertex(32)
vertex32.distribution = {1: 0.12, 0: 0.88}
vertex36 = Vertex.Vertex(36)
vertex36.distribution = {1: 0.03, 0: 0.97}
vertex37 = Vertex.Vertex(37)
vertex37.distribution = {1: 0.03, 0: 0.97}
vertex43 = Vertex.Vertex(43)
vertex43.distribution = {1: 0.02, 0: 0.98}
vertex44 = Vertex.Vertex(44)
vertex44.distribution = {1: 0.02, 0: 0.98}
vertex45 = Vertex.Vertex(45)
vertex45.distribution = {1: 0.02, 0: 0.98}
vertex51 = Vertex.Vertex(51)
vertex51.distribution = {1: 0.03, 0: 0.97}
vertex52 = Vertex.Vertex(52)
vertex52.distribution = {1: 0.02, 0: 0.98}
vertex58 = Vertex.Vertex(58)
vertex58.distribution = {1: 0.03, 0: 0.97}
vertex59 = Vertex.Vertex(59)
vertex59.distribution = {1: 0.06, 0: 0.94}
vertex60 = Vertex.Vertex(60)
vertex60.distribution = {1: 0.03, 0: 0.97}
vertex61 = Vertex.Vertex(61)
vertex61.distribution = {1: 0.02, 0: 0.98}
vertex66 = Vertex.Vertex(66)
vertex66.distribution = {1: 0.06, 0: 0.94}
vertex67 = Vertex.Vertex(67)
vertex67.distribution = {1: 0.12, 0: 0.88}
vertex68 = Vertex.Vertex(68)
vertex68.distribution = {1: 0.06, 0: 0.94}
vertex69 = Vertex.Vertex(69)
vertex69.distribution = {1: 0.03, 0: 0.97}
vertex74 = Vertex.Vertex(74)
vertex74.distribution = {1: 0.12, 0: 0.88}
vertex75 = Vertex.Vertex(75)
vertex75.distribution = {1: 0.25, 0: 0.75}
vertex76 = Vertex.Vertex(76)
vertex76.distribution = {1: 0.12, 0: 0.88}
vertex77 = Vertex.Vertex(77)
vertex77.distribution = {1: 0.06, 0: 0.94}
vertex83 = Vertex.Vertex(83)
vertex83.distribution = {1: 0.12, 0: 0.88}
vertex84 = Vertex.Vertex(84)
vertex84.distribution = {1: 0.06, 0: 0.94}
vertex10.neighbours = [vertex11, vertex18]
vertex11.neighbours = [vertex12, vertex10, vertex19]
vertex12.neighbours = [vertex13, vertex11, vertex20]
vertex13.neighbours = [vertex12, vertex21]
vertex18.neighbours = [vertex19, vertex10]
vertex19.neighbours = [vertex20, vertex18, vertex27, vertex11]
vertex20.neighbours = [vertex21, vertex19, vertex28, vertex12]
vertex21.neighbours = [vertex20, vertex29, vertex13]
vertex23.neighbours = [vertex31]
vertex27.neighbours = [vertex28, vertex19]
vertex28.neighbours = [vertex29, vertex27, vertex36, vertex20]
vertex29.neighbours = [vertex30, vertex28, vertex37, vertex21]
vertex30.neighbours = [vertex31, vertex29]
vertex31.neighbours = [vertex32, vertex30, vertex23]
vertex32.neighbours = [vertex31]
vertex36.neighbours = [vertex37, vertex44, vertex28]
vertex37.neighbours = [vertex36, vertex45, vertex29]
vertex43.neighbours = [vertex44, vertex51]
vertex44.neighbours = [vertex45, vertex43, vertex52, vertex36]
vertex45.neighbours = [vertex44, vertex37]
vertex51.neighbours = [vertex52, vertex59, vertex43]
vertex52.neighbours = [vertex51, vertex60, vertex44]
vertex58.neighbours = [vertex59, vertex66]
vertex59.neighbours = [vertex60, vertex58, vertex67, vertex51]
vertex60.neighbours = [vertex61, vertex59, vertex68, vertex52]
vertex61.neighbours = [vertex60, vertex69]
vertex66.neighbours = [vertex67, vertex74, vertex58]
vertex67.neighbours = [vertex68, vertex66, vertex75, vertex59]
vertex68.neighbours = [vertex69, vertex67, vertex76, vertex60]
vertex69.neighbours = [vertex68, vertex77, vertex61]
vertex74.neighbours = [vertex75, vertex66]
vertex75.neighbours = [vertex76, vertex74, vertex83, vertex67]
vertex76.neighbours = [vertex77, vertex75, vertex84, vertex68]
vertex77.neighbours = [vertex76, vertex69]
vertex83.neighbours = [vertex84, vertex75]
vertex84.neighbours = [vertex83, vertex76]
agent0 = Agent.Agent(0, vertex10, 10, 3)
agent1 = Agent.Agent(1, vertex10, 10, 3)
map1 = [
                                                                                        
                  vertex10, vertex11, vertex12, vertex13,                               
                  vertex18, vertex19, vertex20, vertex21,           vertex23,           
                            vertex27, vertex28, vertex29, vertex30, vertex31, vertex32, 
                                      vertex36, vertex37,                               
                            vertex43, vertex44, vertex45,                               
                            vertex51, vertex52,                                         
                  vertex58, vertex59, vertex60, vertex61,                               
                  vertex66, vertex67, vertex68, vertex69,                               
                  vertex74, vertex75, vertex76, vertex77,                               
                            vertex83, vertex84,                                         
                                                                                        ]
agents = [agent0, agent1]
instance1 = Instance.Instance(map1, agents, 10)
