import Instance 
import Vertex
import Agent
vertex1 = Vertex.Vertex(1)
vertex1.distribution = {1: 0.8264, 0: 0.1736}
vertex2 = Vertex.Vertex(2)
vertex2.distribution = {1: 0.1928, 0: 0.8072}
vertex3 = Vertex.Vertex(3)
vertex3.distribution = {1: 0.1001, 0: 0.8999}
vertex4 = Vertex.Vertex(4)
vertex4.distribution = {1: 0.3035, 0: 0.6965}
vertex5 = Vertex.Vertex(5)
vertex5.distribution = {1: 0.6565, 0: 0.3435}
vertex6 = Vertex.Vertex(6)
vertex6.distribution = {1: 0.0872, 0: 0.9128}
vertex7 = Vertex.Vertex(7)
vertex7.distribution = {1: 0.5057, 0: 0.4943}
vertex8 = Vertex.Vertex(8)
vertex8.distribution = {1: 0.1466, 0: 0.8534}
vertex9 = Vertex.Vertex(9)
vertex9.distribution = {1: 0.0934, 0: 0.9066}
vertex10 = Vertex.Vertex(10)
vertex10.distribution = {1: 0.5588, 0: 0.4412}
vertex11 = Vertex.Vertex(11)
vertex11.distribution = {1: 0.2167, 0: 0.7833}
vertex12 = Vertex.Vertex(12)
vertex12.distribution = {1: 0.5043, 0: 0.4957}
vertex1.neighbours = [vertex2, vertex5]
vertex2.neighbours = [vertex3, vertex1, vertex6]
vertex3.neighbours = [vertex4, vertex2, vertex7]
vertex4.neighbours = [vertex3, vertex8]
vertex5.neighbours = [vertex6, vertex9, vertex1]
vertex6.neighbours = [vertex7, vertex5, vertex10, vertex2]
vertex7.neighbours = [vertex8, vertex6, vertex11, vertex3]
vertex8.neighbours = [vertex7, vertex12, vertex4]
vertex9.neighbours = [vertex10, vertex5]
vertex10.neighbours = [vertex11, vertex9, vertex6]
vertex11.neighbours = [vertex12, vertex10, vertex7]
vertex12.neighbours = [vertex11, vertex8]
agent0 = Agent.Agent(0, vertex1, 2, 3)
agent1 = Agent.Agent(1, vertex1, 2, 3)
agent2 = Agent.Agent(2, vertex1, 2, 3)
map1 = [
        vertex1 , vertex2 , vertex3 , vertex4 , 
        vertex5 , vertex6 , vertex7 , vertex8 , 
        vertex9 , vertex10, vertex11, vertex12, ]
agents = [agent0, agent1, agent2]
instance1 = Instance.Instance("i_3_3_4_3_2_FR", map1, agents, 2)
