import Instance 
import Vertex
import Agent
vertex0 = Vertex.Vertex(0)
vertex0.distribution = {0: 1}
vertex1 = Vertex.Vertex(1)
vertex1.distribution = {0: 0, 10: 1}
vertex2 = Vertex.Vertex(2)
vertex2.distribution = {0: 1}
vertex3 = Vertex.Vertex(3)
vertex3.distribution = {0: 1}
vertex4 = Vertex.Vertex(4)
vertex4.distribution = {1: 0.5, 0: 0.5}
vertex5 = Vertex.Vertex(5)
vertex5.distribution = {0: 1}
vertex6 = Vertex.Vertex(6)
vertex6.distribution = {0: 1}
vertex7 = Vertex.Vertex(7)
vertex7.distribution = {0: 1}
vertex8 = Vertex.Vertex(8)
vertex8.distribution = {10: 1}
vertex9 = Vertex.Vertex(9)
vertex9.distribution = {0: 1}
vertex10 = Vertex.Vertex(10)
vertex10.distribution = {2: 1, 0: 0}
vertex11 = Vertex.Vertex(11)
vertex11.distribution = {10: 1}
vertex0.neighbours = [vertex3, vertex1]
vertex1.neighbours = [vertex0, vertex4, vertex2]
vertex2.neighbours = [vertex1, vertex5]
vertex3.neighbours = [vertex0, vertex4, vertex6]
vertex3.neighbours = [vertex0, vertex6, vertex4]
vertex4.neighbours = [vertex1, vertex3, vertex7, vertex5]
vertex5.neighbours = [vertex2, vertex4, vertex8]
vertex6.neighbours = [vertex3, vertex9]
vertex7.neighbours = [vertex4]
vertex8.neighbours = [vertex5]
vertex9.neighbours = [vertex6, vertex10]
vertex10.neighbours = [vertex9, vertex11]
vertex11.neighbours = [vertex10]

agent0 = Agent.Agent(0, vertex6, 6, 2)
agent1 = Agent.Agent(1, vertex7, 2, 1)
map1 = [vertex0, vertex1, vertex2, 
        vertex3, vertex4, vertex5, 
        vertex6, vertex7, vertex8, 
        vertex9, vertex10, vertex11]
'''
[0]    [1]     [2]

[3]    [4]     [5]

[6]* | [7]* |  [8] 
     +------+------ 
[9]    [10]    [11]
'''

agents = [agent0, agent1]
instance1 = Instance.Instance(map1, agents, 6)
