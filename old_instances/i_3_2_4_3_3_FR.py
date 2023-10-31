import Instance 
import Vertex
import Agent
vertex1 = Vertex.Vertex(1)
vertex1.distribution = {1: 0.0383, 0: 0.9617}
vertex2 = Vertex.Vertex(2)
vertex2.distribution = {1: 0.0314, 0: 0.9686}
vertex3 = Vertex.Vertex(3)
vertex3.distribution = {1: 0.0007, 0: 0.9993}
vertex4 = Vertex.Vertex(4)
vertex4.distribution = {1: 0.0048, 0: 0.9952}
vertex5 = Vertex.Vertex(5)
vertex5.distribution = {1: 0.6463, 0: 0.3537}
vertex6 = Vertex.Vertex(6)
vertex6.distribution = {1: 0.2613, 0: 0.7387}
vertex7 = Vertex.Vertex(7)
vertex7.distribution = {1: 0.0722, 0: 0.9278}
vertex8 = Vertex.Vertex(8)
vertex8.distribution = {1: 0.2697, 0: 0.7303}
vertex1.neighbours = [vertex2, vertex5]
vertex2.neighbours = [vertex3, vertex1, vertex6]
vertex3.neighbours = [vertex4, vertex2, vertex7]
vertex4.neighbours = [vertex3, vertex8]
vertex5.neighbours = [vertex6, vertex1]
vertex6.neighbours = [vertex7, vertex5, vertex2]
vertex7.neighbours = [vertex8, vertex6, vertex3]
vertex8.neighbours = [vertex7, vertex4]
agent0 = Agent.Agent(0, vertex1, 3, 3)
agent1 = Agent.Agent(1, vertex1, 3, 3)
agent2 = Agent.Agent(2, vertex1, 2, 3)
map1 = [
        vertex1, vertex2, vertex3, vertex4, 
        vertex5, vertex6, vertex7, vertex8, ]
agents = [agent0, agent1, agent2]
instance1 = Instance.Instance("i_3_2_4_3_3_FR", map1, agents, 3)
