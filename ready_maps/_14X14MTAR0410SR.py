import Instance 
import Vertex
import Agent
vertex20 = Vertex.Vertex(20)
vertex20.distribution = {1: 0.01562, 0: 0.98438}
vertex35 = Vertex.Vertex(35)
vertex35.distribution = {1: 0.00098, 0: 0.99902}
vertex49 = Vertex.Vertex(49)
vertex49.distribution = {1: 0.00098, 0: 0.99902}
vertex63 = Vertex.Vertex(63)
vertex63.distribution = {1: 0.00024, 0: 0.99976}
vertex65 = Vertex.Vertex(65)
vertex65.distribution = {1: 0.00391, 0: 0.99609}
vertex76 = Vertex.Vertex(76)
vertex76.distribution = {1: 0.00024, 0: 0.99976}
vertex77 = Vertex.Vertex(77)
vertex77.distribution = {1: 0.00098, 0: 0.99902}
vertex78 = Vertex.Vertex(78)
vertex78.distribution = {1: 0.00391, 0: 0.99609}
vertex79 = Vertex.Vertex(79)
vertex79.distribution = {1: 0.01562, 0: 0.98438}
vertex80 = Vertex.Vertex(80)
vertex80.distribution = {1: 0.00391, 0: 0.99609}
vertex90 = Vertex.Vertex(90)
vertex90.distribution = {1: 0.00391, 0: 0.99609}
vertex91 = Vertex.Vertex(91)
vertex91.distribution = {1: 0.00098, 0: 0.99902}
vertex92 = Vertex.Vertex(92)
vertex92.distribution = {1: 0.00391, 0: 0.99609}
vertex94 = Vertex.Vertex(94)
vertex94.distribution = {1: 0.0625, 0: 0.9375}
vertex95 = Vertex.Vertex(95)
vertex95.distribution = {1: 0.01562, 0: 0.98438}
vertex100 = Vertex.Vertex(100)
vertex100.distribution = {1: 0.01562, 0: 0.98438}
vertex101 = Vertex.Vertex(101)
vertex101.distribution = {1: 0.0, 0: 1.0}
vertex102 = Vertex.Vertex(102)
vertex102.distribution = {1: 2e-05, 0: 0.99998}
vertex104 = Vertex.Vertex(104)
vertex104.distribution = {1: 6e-05, 0: 0.99994}
vertex105 = Vertex.Vertex(105)
vertex105.distribution = {1: 0.00024, 0: 0.99976}
vertex106 = Vertex.Vertex(106)
vertex106.distribution = {1: 0.00098, 0: 0.99902}
vertex107 = Vertex.Vertex(107)
vertex107.distribution = {1: 0.00391, 0: 0.99609}
vertex118 = Vertex.Vertex(118)
vertex118.distribution = {1: 0.0625, 0: 0.9375}
vertex119 = Vertex.Vertex(119)
vertex119.distribution = {1: 0.25, 0: 0.75}
vertex120 = Vertex.Vertex(120)
vertex120.distribution = {1: 0.0625, 0: 0.9375}
vertex121 = Vertex.Vertex(121)
vertex121.distribution = {1: 0.01562, 0: 0.98438}
vertex122 = Vertex.Vertex(122)
vertex122.distribution = {1: 0.00391, 0: 0.99609}
vertex123 = Vertex.Vertex(123)
vertex123.distribution = {1: 0.00098, 0: 0.99902}
vertex124 = Vertex.Vertex(124)
vertex124.distribution = {1: 0.00098, 0: 0.99902}
vertex132 = Vertex.Vertex(132)
vertex132.distribution = {1: 0.0625, 0: 0.9375}
vertex133 = Vertex.Vertex(133)
vertex133.distribution = {1: 0.01562, 0: 0.98438}
vertex134 = Vertex.Vertex(134)
vertex134.distribution = {1: 0.00391, 0: 0.99609}
vertex135 = Vertex.Vertex(135)
vertex135.distribution = {1: 0.00391, 0: 0.99609}
vertex136 = Vertex.Vertex(136)
vertex136.distribution = {1: 0.00098, 0: 0.99902}
vertex137 = Vertex.Vertex(137)
vertex137.distribution = {1: 0.00024, 0: 0.99976}
vertex138 = Vertex.Vertex(138)
vertex138.distribution = {1: 0.00098, 0: 0.99902}
vertex147 = Vertex.Vertex(147)
vertex147.distribution = {1: 0.00391, 0: 0.99609}
vertex148 = Vertex.Vertex(148)
vertex148.distribution = {1: 0.01562, 0: 0.98438}
vertex149 = Vertex.Vertex(149)
vertex149.distribution = {1: 0.00391, 0: 0.99609}
vertex150 = Vertex.Vertex(150)
vertex150.distribution = {1: 0.00098, 0: 0.99902}
vertex151 = Vertex.Vertex(151)
vertex151.distribution = {1: 0.00024, 0: 0.99976}
vertex152 = Vertex.Vertex(152)
vertex152.distribution = {1: 6e-05, 0: 0.99994}
vertex161 = Vertex.Vertex(161)
vertex161.distribution = {1: 0.01562, 0: 0.98438}
vertex162 = Vertex.Vertex(162)
vertex162.distribution = {1: 0.00391, 0: 0.99609}
vertex163 = Vertex.Vertex(163)
vertex163.distribution = {1: 0.00098, 0: 0.99902}
vertex164 = Vertex.Vertex(164)
vertex164.distribution = {1: 0.00391, 0: 0.99609}
vertex175 = Vertex.Vertex(175)
vertex175.distribution = {1: 0.00098, 0: 0.99902}
vertex189 = Vertex.Vertex(189)
vertex189.distribution = {1: 0.00391, 0: 0.99609}
vertex20.neighbours = []
vertex35.neighbours = [vertex49]
vertex49.neighbours = [vertex63, vertex35]
vertex63.neighbours = [vertex77, vertex49]
vertex65.neighbours = [vertex79]
vertex76.neighbours = [vertex77, vertex90]
vertex77.neighbours = [vertex78, vertex76, vertex91, vertex63]
vertex78.neighbours = [vertex79, vertex77, vertex92]
vertex79.neighbours = [vertex80, vertex78, vertex65]
vertex80.neighbours = [vertex79, vertex94]
vertex90.neighbours = [vertex91, vertex104, vertex76]
vertex91.neighbours = [vertex92, vertex90, vertex105, vertex77]
vertex92.neighbours = [vertex91, vertex106, vertex78]
vertex94.neighbours = [vertex95, vertex80]
vertex95.neighbours = [vertex94]
vertex100.neighbours = [vertex101]
vertex101.neighbours = [vertex102, vertex100]
vertex102.neighbours = [vertex101]
vertex104.neighbours = [vertex105, vertex118, vertex90]
vertex105.neighbours = [vertex106, vertex104, vertex119, vertex91]
vertex106.neighbours = [vertex107, vertex105, vertex120, vertex92]
vertex107.neighbours = [vertex106, vertex121]
vertex118.neighbours = [vertex119, vertex132, vertex104]
vertex119.neighbours = [vertex120, vertex118, vertex133, vertex105]
vertex120.neighbours = [vertex121, vertex119, vertex134, vertex106]
vertex121.neighbours = [vertex122, vertex120, vertex135, vertex107]
vertex122.neighbours = [vertex123, vertex121, vertex136]
vertex123.neighbours = [vertex124, vertex122, vertex137]
vertex124.neighbours = [vertex123, vertex138]
vertex132.neighbours = [vertex133, vertex118]
vertex133.neighbours = [vertex134, vertex132, vertex147, vertex119]
vertex134.neighbours = [vertex135, vertex133, vertex148, vertex120]
vertex135.neighbours = [vertex136, vertex134, vertex149, vertex121]
vertex136.neighbours = [vertex137, vertex135, vertex150, vertex122]
vertex137.neighbours = [vertex138, vertex136, vertex151, vertex123]
vertex138.neighbours = [vertex137, vertex152, vertex124]
vertex147.neighbours = [vertex148, vertex161, vertex133]
vertex148.neighbours = [vertex149, vertex147, vertex162, vertex134]
vertex149.neighbours = [vertex150, vertex148, vertex163, vertex135]
vertex150.neighbours = [vertex151, vertex149, vertex164, vertex136]
vertex151.neighbours = [vertex152, vertex150, vertex137]
vertex152.neighbours = [vertex151, vertex138]
vertex161.neighbours = [vertex162, vertex175, vertex147]
vertex162.neighbours = [vertex163, vertex161, vertex148]
vertex163.neighbours = [vertex164, vertex162, vertex149]
vertex164.neighbours = [vertex163, vertex150]
vertex175.neighbours = [vertex189, vertex161]
vertex189.neighbours = [vertex175]
agent0 = Agent.Agent(0, vertex20, 5, 3)
agent1 = Agent.Agent(1, vertex20, 5, 4)
map1 = [
                                                                                                                                                                  
                                                               vertex20 ,                                                                                         
                                                                          vertex35 ,                                                                              
                                                                          vertex49 ,                                                                              
                                                                          vertex63 ,            vertex65 ,                                                        
                                                               vertex76 , vertex77 , vertex78 , vertex79 , vertex80 ,                                             
                                                               vertex90 , vertex91 , vertex92 ,            vertex94 , vertex95 ,                                  
                   vertex100, vertex101, vertex102,            vertex104, vertex105, vertex106, vertex107,                                                        
                                                               vertex118, vertex119, vertex120, vertex121, vertex122, vertex123, vertex124,                       
                                                               vertex132, vertex133, vertex134, vertex135, vertex136, vertex137, vertex138,                       
                                                                          vertex147, vertex148, vertex149, vertex150, vertex151, vertex152,                       
                                                                          vertex161, vertex162, vertex163, vertex164,                                             
                                                                          vertex175,                                                                              
                                                                          vertex189,                                                                              ]
agents = [agent0, agent1]
instance1 = Instance.Instance("gridAR410SRMT", map1, agents, 5)
