"""
Algorithm: Searching - linear, binary, BFS, DFS
"""

# Linear search - O(n)
def linear_search(arr: list, target) -> int:
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1


# Binary search - O(log n), requires sorted array
def binary_search(arr: list, target) -> int:
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


# BFS - Breadth-First Search (level by level)
from collections import deque

def bfs(graph: dict, start) -> list:
    visited = set()
    queue = deque([start])
    result = []

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            result.append(node)
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    queue.append(neighbor)

    return result


# DFS - Depth-First Search (go deep first)
def dfs(graph: dict, start, visited: set = None) -> list:
    if visited is None:
        visited = set()

    visited.add(start)
    result = [start]

    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            result.extend(dfs(graph, neighbor, visited))

    return result


# Graph for testing
graph = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F", "G"],
    "D": [],
    "E": [],
    "F": [],
    "G": [],
}

print(f"BFS: {bfs(graph, 'A')}")  # ['A', 'B', 'C', 'D', 'E', 'F', 'G']
print(f"DFS: {dfs(graph, 'A')}")  # ['A', 'B', 'D', 'E', 'C', 'F', 'G']

# Binary search test
sorted_nums = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
print(f"Linear search for 7: {linear_search(sorted_nums, 7)}")  # 3
print(f"Binary search for 7: {binary_search(sorted_nums, 7)}")  # 3
print(f"Binary search for 8: {binary_search(sorted_nums, 8)}")  # -1