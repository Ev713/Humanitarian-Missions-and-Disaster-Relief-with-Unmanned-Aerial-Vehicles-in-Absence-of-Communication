import Instance 
import Vertex
import Agent
vertex1 = Vertex.Vertex(1)
vertex1.distribution = {1: 0.2489, 0: 0.7511}
vertex2 = Vertex.Vertex(2)
vertex2.distribution = {1: 0.5501, 0: 0.4499}
vertex3 = Vertex.Vertex(3)
vertex3.distribution = {1: 0.2695, 0: 0.7305}
vertex4 = Vertex.Vertex(4)
vertex4.distribution = {1: 0.3476, 0: 0.6524}
vertex5 = Vertex.Vertex(5)
vertex5.distribution = {1: 0.7124, 0: 0.2876}
vertex6 = Vertex.Vertex(6)
vertex6.distribution = {1: 0.0185, 0: 0.9815}
vertex1.neighbours = [vertex2, vertex3]
vertex2.neighbours = [vertex1, vertex4]
vertex3.neighbours = [vertex4, vertex5, vertex1]
vertex4.neighbours = [vertex3, vertex6, vertex2]
vertex5.neighbours = [vertex6, vertex3]
vertex6.neighbours = [vertex5, vertex4]
agent0 = Agent.Agent(0, vertex1, 2, 3)
map1 = [
        vertex1, vertex2, 
        vertex3, vertex4, 
        vertex5, vertex6, ]
agents = [agent0]
instance1 = Instance.Instance("i_3_3_2_1_2_FR", map1, agents, 2)
