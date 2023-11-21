import heapq


class PriorityNode:
    def __init__(self, node):
        self.node = node
        self.priority = - node.value

    def __lt__(self, other):
        return self.priority < other.priority


class MaxPriorityQueue:
    def __init__(self):
        self._queue = []

    def push(self, node):
        heapq.heappush(self._queue, PriorityNode(node))

    def pop(self):
        if self._queue:
            return heapq.heappop(self._queue).node
        else:
            raise IndexError("pop from an empty priority queue")

    def is_empty(self):
        return len(self._queue) == 0

