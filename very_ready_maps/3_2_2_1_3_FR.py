import Instance 
import Vertex
import Agent
vertex1 = Vertex.Vertex(1)
vertex1.distribution = {1: 0.1692, 0: 0.8308}
vertex2 = Vertex.Vertex(2)
vertex2.distribution = {1: 0.2174, 0: 0.7826}
vertex3 = Vertex.Vertex(3)
vertex3.distribution = {1: 0.0084, 0: 0.9916}
vertex4 = Vertex.Vertex(4)
vertex4.distribution = {1: 0.0629, 0: 0.9371}
vertex1.neighbours = [vertex2, vertex3]
vertex2.neighbours = [vertex1, vertex4]
vertex3.neighbours = [vertex4, vertex1]
vertex4.neighbours = [vertex3, vertex2]
agent0 = Agent.Agent(0, vertex1, 2, 3)
map1 = [
        vertex1, vertex2, 
        vertex3, vertex4, ]
agents = [agent0]
instance1 = Instance.Instance("3_2_2_1_3_FR", map1, agents, 2)
