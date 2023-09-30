import Instance 
import Vertex
import Agent
vertex1 = Vertex.Vertex(1)
vertex1.distribution = {1: 0.3408, 0: 0.6592}
vertex2 = Vertex.Vertex(2)
vertex2.distribution = {1: 0.509, 0: 0.491}
vertex3 = Vertex.Vertex(3)
vertex3.distribution = {1: 0.0318, 0: 0.9682}
vertex4 = Vertex.Vertex(4)
vertex4.distribution = {1: 0.0783, 0: 0.9217}
vertex5 = Vertex.Vertex(5)
vertex5.distribution = {1: 0.3653, 0: 0.6347}
vertex6 = Vertex.Vertex(6)
vertex6.distribution = {1: 0.0343, 0: 0.9657}
vertex1.neighbours = [vertex2, vertex3]
vertex2.neighbours = [vertex1, vertex4]
vertex3.neighbours = [vertex4, vertex5, vertex1]
vertex4.neighbours = [vertex3, vertex6, vertex2]
vertex5.neighbours = [vertex6, vertex3]
vertex6.neighbours = [vertex5, vertex4]
agent0 = Agent.Agent(0, vertex1, 3, 6)
map1 = [
        vertex1, vertex2, 
        vertex3, vertex4, 
        vertex5, vertex6, ]
agents = [agent0]
instance1 = Instance.Instance("i_3_3_2_1_6_FR", map1, agents, 3, source="-")
