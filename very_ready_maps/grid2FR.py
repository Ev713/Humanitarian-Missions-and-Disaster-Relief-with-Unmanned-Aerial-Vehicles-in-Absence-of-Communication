import Instance 
import Vertex
import Agent
vertex1 = Vertex.Vertex(1)
vertex1.distribution = {1: 0.0861, 0: 0.9139}
vertex2 = Vertex.Vertex(2)
vertex2.distribution = {1: 0.8559, 0: 0.1441}
vertex3 = Vertex.Vertex(3)
vertex3.distribution = {1: 0.3506, 0: 0.6494}
vertex4 = Vertex.Vertex(4)
vertex4.distribution = {1: 0.9886, 0: 0.0114}
vertex1.neighbours = [vertex2, vertex3]
vertex2.neighbours = [vertex1, vertex4]
vertex3.neighbours = [vertex4, vertex1]
vertex4.neighbours = [vertex3, vertex2]
agent0 = Agent.Agent(0, vertex1, 2, 3)
map1 = [
        vertex1, vertex2, 
        vertex3, vertex4, ]
agents = [agent0]
instance1 = Instance.Instance("grid2FR", map1, agents, 2)
