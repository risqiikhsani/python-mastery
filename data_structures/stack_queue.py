"""
Python Stacks and Queues using lists/collections
"""

# ---- STACK (LIFO) ----
# Use list as a stack - append/pop are O(1) at the end
stack = []
stack.append(1)  # push
stack.append(2)
stack.append(3)
print(f"Stack: {stack}")

top = stack.pop()  # pop from top
print(f"Popped: {top}, remaining: {stack}")  # [1, 2]

# Check without modifying
print(f"Peek: {stack[-1]}")  # 2

# ---- QUEUE (FIFO) ----
# For queues, use collections.deque for O(1) popleft()
from collections import deque

queue = deque()
queue.append("first")
queue.append("second")
queue.append("third")
print(f"Queue: {queue}")

first = queue.popleft()
print(f"Dequeued: {first}, remaining: {queue}")  # ['second', 'third']

# ---- PRIORITY QUEUE ----
import heapq

# Min-heap (smallest first)
heap = []
heapq.heappush(heap, 5)
heapq.heappush(heap, 1)
heapq.heappush(heap, 3)
print(f"Heap: {heap}")  # [1, 5, 3]

# Pop smallest
smallest = heapq.heappop(heap)
print(f"Smallest: {smallest}, remaining: {heap}")  # [3, 5]

# Build heap from list
data = [5, 1, 3, 7, 2]
heapq.heapify(data)
print(f"Heapified: {data}")  # [1, 2, 3, 7, 5]

# ---- BFS with deque ----
# Classic use: breadth-first search
graph = {
    "A": ["B", "C"],
    "B": ["A", "D"],
    "C": ["A", "D"],
    "D": ["B", "C"],
}

def bfs(start):
    visited = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        print(f"Visit: {node}")
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

bfs("A")