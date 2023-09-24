import Instance 
import Vertex
import Agent
vertex1 = Vertex.Vertex(1)
vertex1.distribution = {1: 0.673, 0: 0.327}
vertex2 = Vertex.Vertex(2)
vertex2.distribution = {1: 0.8673, 0: 0.1327}
vertex3 = Vertex.Vertex(3)
vertex3.distribution = {1: 0.0217, 0: 0.9783}
vertex4 = Vertex.Vertex(4)
vertex4.distribution = {1: 0.4927, 0: 0.5073}
vertex5 = Vertex.Vertex(5)
vertex5.distribution = {1: 0.7027, 0: 0.2973}
vertex6 = Vertex.Vertex(6)
vertex6.distribution = {1: 0.1097, 0: 0.8903}
vertex1.neighbours = [vertex2, vertex4]
vertex2.neighbours = [vertex3, vertex1, vertex5]
vertex3.neighbours = [vertex2, vertex6]
vertex4.neighbours = [vertex5, vertex1]
vertex5.neighbours = [vertex6, vertex4, vertex2]
vertex6.neighbours = [vertex5, vertex3]
agent0 = Agent.Agent(0, vertex1, 2, 3)
agent1 = Agent.Agent(1, vertex1, 2, 3)
map1 = [
        vertex1, vertex2, vertex3, 
        vertex4, vertex5, vertex6, ]
agents = [agent0, agent1]
instance1 = Instance.Instance("i_3_2_3_2_2_FR", map1, agents, 2)
