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


class DataNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class Queue:
    def __init__(self, data):
        self.head = DataNode(data)
        self.tail = self.head

    def is_empty(self):
        return self.head is None

    def push(self, data):
        self.head.next = DataNode(data)
        self.head = self.head.next

    def pop(self):
        tail = self.tail
        self.tail = tail.next
        tail.next = None
        return tail
