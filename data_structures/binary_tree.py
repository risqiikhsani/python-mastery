"""
Binary Tree and Binary Search Tree
"""

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def __repr__(self):
        return f"TreeNode({self.value})"


class BST:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if not self.root:
            self.root = TreeNode(value)
        else:
            self._insert(self.root, value)

    def _insert(self, node, value):
        if value < node.value:
            if node.left:
                self._insert(node.left, value)
            else:
                node.left = TreeNode(value)
        else:
            if node.right:
                self._insert(node.right, value)
            else:
                node.right = TreeNode(value)

    def search(self, value):
        return self._search(self.root, value)

    def _search(self, node, value):
        if not node:
            return False
        if node.value == value:
            return True
        elif value < node.value:
            return self._search(node.left, value)
        else:
            return self._search(node.right, value)

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.value)
            self._inorder(node.right, result)

    def height(self, node=None):
        if node is None:
            node = self.root
        if not node:
            return 0
        return 1 + max(self.height(node.left), self.height(node.right))


# Usage
bst = BST()
for val in [5, 3, 7, 1, 4, 6, 8]:
    bst.insert(val)

print(f"Inorder (sorted): {bst.inorder()}")  # [1, 3, 4, 5, 6, 7, 8]
print(f"Search 4: {bst.search(4)}")   # True
print(f"Search 9: {bst.search(9)}")   # False
print(f"Height: {bst.height()}")     # 3

# Visualize tree
#        5
#       / \
#      3   7
#     / \ / \
#    1  4 6  8