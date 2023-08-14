import Instance 
import Vertex
import Agent
vertex43 = Vertex.Vertex(43)
vertex43.distribution = {1: 0.01562, 0: 0.98438}
vertex44 = Vertex.Vertex(44)
vertex44.distribution = {1: 0.01562, 0: 0.98438}
vertex45 = Vertex.Vertex(45)
vertex45.distribution = {1: 0.0625, 0: 0.9375}
vertex54 = Vertex.Vertex(54)
vertex54.distribution = {1: 0.01562, 0: 0.98438}
vertex57 = Vertex.Vertex(57)
vertex57.distribution = {1: 0.25, 0: 0.75}
vertex58 = Vertex.Vertex(58)
vertex58.distribution = {1: 0.0625, 0: 0.9375}
vertex59 = Vertex.Vertex(59)
vertex59.distribution = {1: 0.01562, 0: 0.98438}
vertex65 = Vertex.Vertex(65)
vertex65.distribution = {1: 0.0625, 0: 0.9375}
vertex66 = Vertex.Vertex(66)
vertex66.distribution = {1: 0.01562, 0: 0.98438}
vertex67 = Vertex.Vertex(67)
vertex67.distribution = {1: 0.0625, 0: 0.9375}
vertex68 = Vertex.Vertex(68)
vertex68.distribution = {1: 0.25, 0: 0.75}
vertex69 = Vertex.Vertex(69)
vertex69.distribution = {1: 0.0625, 0: 0.9375}
vertex71 = Vertex.Vertex(71)
vertex71.distribution = {1: 0.0625, 0: 0.9375}
vertex72 = Vertex.Vertex(72)
vertex72.distribution = {1: 0.01562, 0: 0.98438}
vertex77 = Vertex.Vertex(77)
vertex77.distribution = {1: 0.0625, 0: 0.9375}
vertex78 = Vertex.Vertex(78)
vertex78.distribution = {1: 0.25, 0: 0.75}
vertex80 = Vertex.Vertex(80)
vertex80.distribution = {1: 0.0625, 0: 0.9375}
vertex81 = Vertex.Vertex(81)
vertex81.distribution = {1: 0.0625, 0: 0.9375}
vertex82 = Vertex.Vertex(82)
vertex82.distribution = {1: 0.01562, 0: 0.98438}
vertex83 = Vertex.Vertex(83)
vertex83.distribution = {1: 0.00391, 0: 0.99609}
vertex88 = Vertex.Vertex(88)
vertex88.distribution = {1: 0.01562, 0: 0.98438}
vertex89 = Vertex.Vertex(89)
vertex89.distribution = {1: 0.01562, 0: 0.98438}
vertex90 = Vertex.Vertex(90)
vertex90.distribution = {1: 0.00391, 0: 0.99609}
vertex91 = Vertex.Vertex(91)
vertex91.distribution = {1: 0.00098, 0: 0.99902}
vertex92 = Vertex.Vertex(92)
vertex92.distribution = {1: 0.00391, 0: 0.99609}
vertex94 = Vertex.Vertex(94)
vertex94.distribution = {1: 0.00391, 0: 0.99609}
vertex99 = Vertex.Vertex(99)
vertex99.distribution = {1: 0.0625, 0: 0.9375}
vertex101 = Vertex.Vertex(101)
vertex101.distribution = {1: 0.00098, 0: 0.99902}
vertex103 = Vertex.Vertex(103)
vertex103.distribution = {1: 0.01562, 0: 0.98438}
vertex104 = Vertex.Vertex(104)
vertex104.distribution = {1: 0.0625, 0: 0.9375}
vertex105 = Vertex.Vertex(105)
vertex105.distribution = {1: 0.01562, 0: 0.98438}
vertex106 = Vertex.Vertex(106)
vertex106.distribution = {1: 0.0625, 0: 0.9375}
vertex112 = Vertex.Vertex(112)
vertex112.distribution = {1: 0.0625, 0: 0.9375}
vertex113 = Vertex.Vertex(113)
vertex113.distribution = {1: 0.25, 0: 0.75}
vertex114 = Vertex.Vertex(114)
vertex114.distribution = {1: 0.0625, 0: 0.9375}
vertex115 = Vertex.Vertex(115)
vertex115.distribution = {1: 0.01562, 0: 0.98438}
vertex116 = Vertex.Vertex(116)
vertex116.distribution = {1: 0.0625, 0: 0.9375}
vertex117 = Vertex.Vertex(117)
vertex117.distribution = {1: 0.25, 0: 0.75}
vertex118 = Vertex.Vertex(118)
vertex118.distribution = {1: 0.0625, 0: 0.9375}
vertex123 = Vertex.Vertex(123)
vertex123.distribution = {1: 0.01562, 0: 0.98438}
vertex124 = Vertex.Vertex(124)
vertex124.distribution = {1: 0.00391, 0: 0.99609}
vertex126 = Vertex.Vertex(126)
vertex126.distribution = {1: 0.00391, 0: 0.99609}
vertex128 = Vertex.Vertex(128)
vertex128.distribution = {1: 0.00098, 0: 0.99902}
vertex135 = Vertex.Vertex(135)
vertex135.distribution = {1: 0.25, 0: 0.75}
vertex136 = Vertex.Vertex(136)
vertex136.distribution = {1: 0.0625, 0: 0.9375}
vertex137 = Vertex.Vertex(137)
vertex137.distribution = {1: 0.25, 0: 0.75}
vertex43.neighbours = [vertex44]
vertex44.neighbours = [vertex45, vertex43]
vertex45.neighbours = [vertex44, vertex57]
vertex54.neighbours = [vertex66]
vertex57.neighbours = [vertex58, vertex69, vertex45]
vertex58.neighbours = [vertex59, vertex57]
vertex59.neighbours = [vertex58, vertex71]
vertex65.neighbours = [vertex66, vertex77]
vertex66.neighbours = [vertex67, vertex65, vertex78, vertex54]
vertex67.neighbours = [vertex68, vertex66]
vertex68.neighbours = [vertex69, vertex67, vertex80]
vertex69.neighbours = [vertex68, vertex81, vertex57]
vertex71.neighbours = [vertex72, vertex83, vertex59]
vertex72.neighbours = [vertex71]
vertex77.neighbours = [vertex78, vertex89, vertex65]
vertex78.neighbours = [vertex77, vertex90, vertex66]
vertex80.neighbours = [vertex81, vertex92, vertex68]
vertex81.neighbours = [vertex82, vertex80, vertex69]
vertex82.neighbours = [vertex83, vertex81, vertex94]
vertex83.neighbours = [vertex82, vertex71]
vertex88.neighbours = [vertex89]
vertex89.neighbours = [vertex90, vertex88, vertex101, vertex77]
vertex90.neighbours = [vertex91, vertex89, vertex78]
vertex91.neighbours = [vertex92, vertex90, vertex103]
vertex92.neighbours = [vertex91, vertex104, vertex80]
vertex94.neighbours = [vertex106, vertex82]
vertex99.neighbours = []
vertex101.neighbours = [vertex113, vertex89]
vertex103.neighbours = [vertex104, vertex115, vertex91]
vertex104.neighbours = [vertex105, vertex103, vertex116, vertex92]
vertex105.neighbours = [vertex106, vertex104, vertex117]
vertex106.neighbours = [vertex105, vertex118, vertex94]
vertex112.neighbours = [vertex113, vertex124]
vertex113.neighbours = [vertex114, vertex112, vertex101]
vertex114.neighbours = [vertex115, vertex113, vertex126]
vertex115.neighbours = [vertex116, vertex114, vertex103]
vertex116.neighbours = [vertex117, vertex115, vertex128, vertex104]
vertex117.neighbours = [vertex118, vertex116, vertex105]
vertex118.neighbours = [vertex117, vertex106]
vertex123.neighbours = [vertex124, vertex135]
vertex124.neighbours = [vertex123, vertex136, vertex112]
vertex126.neighbours = [vertex114]
vertex128.neighbours = [vertex116]
vertex135.neighbours = [vertex136, vertex123]
vertex136.neighbours = [vertex137, vertex135, vertex124]
vertex137.neighbours = [vertex136]
agent0 = Agent.Agent(0, vertex43, 8, 8)
agent1 = Agent.Agent(1, vertex43, 8, 3)
map1 = [
                                                                                                                                            
                                                                                                                                            
                                                                                                                                            
                                                                          vertex43 , vertex44 , vertex45 ,                                  
                                                               vertex54 ,                       vertex57 , vertex58 , vertex59 ,            
                                                    vertex65 , vertex66 , vertex67 , vertex68 , vertex69 ,            vertex71 , vertex72 , 
                                                    vertex77 , vertex78 ,            vertex80 , vertex81 , vertex82 , vertex83 ,            
                                         vertex88 , vertex89 , vertex90 , vertex91 , vertex92 ,            vertex94 ,                       
                              vertex99 ,            vertex101,            vertex103, vertex104, vertex105, vertex106,                       
                                         vertex112, vertex113, vertex114, vertex115, vertex116, vertex117, vertex118,                       
                              vertex123, vertex124,            vertex126,            vertex128,                                             
                              vertex135, vertex136, vertex137,                                                                              ]
agents = [agent0, agent1]
instance1 = Instance.Instance("gridAR509SRMT", map1, agents, 8)
