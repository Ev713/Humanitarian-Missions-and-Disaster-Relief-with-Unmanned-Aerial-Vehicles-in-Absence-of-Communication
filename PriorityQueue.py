import heapq


class PriorityNode:
    def __init__(self, node, priority):
        self.node = node
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority


class PriorityQueue:
    def __init__(self, is_greedy, node=None, ):
        self._queue = []
        self.greedy = is_greedy
        if node is not None:
            self.push(node)

    def push(self, node):
        heapq.heappush(self._queue, PriorityNode(node, - node.value - node.high if self.greedy else node.depth))

    def pop(self):
        if self._queue:
            return heapq.heappop(self._queue).node
        else:
            raise IndexError("pop from an empty priority queue")

    def is_empty(self):
        return len(self._queue) == 0
