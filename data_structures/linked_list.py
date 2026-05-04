"""
Linked List implementation in Python
"""

class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

    def __repr__(self):
        return f"Node({self.value})"


class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def append(self, value):
        new_node = Node(value)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1

    def prepend(self, value):
        new_node = Node(value, self.head)
        self.head = new_node
        self.size += 1

    def find(self, value):
        current = self.head
        index = 0
        while current:
            if current.value == value:
                return index
            current = current.next
            index += 1
        return -1

    def delete(self, value):
        if not self.head:
            return False
        if self.head.value == value:
            self.head = self.head.next
            self.size -= 1
            return True
        current = self.head
        while current.next:
            if current.next.value == value:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        return False

    def __len__(self):
        return self.size

    def __repr__(self):
        values = []
        current = self.head
        while current:
            values.append(str(current.value))
            current = current.next
        return " -> ".join(values) + " -> None"


# Usage
ll = LinkedList()
ll.append(1)
ll.append(2)
ll.append(3)
ll.prepend(0)
print(f"List: {ll}")           # 0 -> 1 -> 2 -> 3 -> None
print(f"Find 2 at index: {ll.find(2)}")  # 2
ll.delete(2)
print(f"After delete 2: {ll}")  # 0 -> 1 -> 3 -> None
print(f"Length: {len(ll)}")    # 3