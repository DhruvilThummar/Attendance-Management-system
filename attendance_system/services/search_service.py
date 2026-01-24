"""BST-based student search implementation."""
from __future__ import annotations
import logging
from typing import Optional
from ..models.student import Student

logger = logging.getLogger(__name__)

class Node:
    def __init__(self, key: str, value: int):
        self.key = key  # enrollment_no
        self.value = value  # student_id
        self.left: Node | None = None
        self.right: Node | None = None

class BST:
    def __init__(self):
        self.root: Node | None = None

    def insert(self, key: str, value: int) -> None:
        self.root = self._insert_recursive(self.root, key, value)

    def _insert_recursive(self, node: Node | None, key: str, value: int) -> Node:
        if node is None:
            return Node(key, value)
        if key < node.key:
            node.left = self._insert_recursive(node.left, key, value)
        elif key > node.key:
            node.right = self._insert_recursive(node.right, key, value)
        else:
            node.value = value  # Update existing
        return node

    def search(self, key: str) -> int | None:
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node: Node | None, key: str) -> int | None:
        if node is None:
            return None
        if key == node.key:
            return node.value
        if key < node.key:
            return self._search_recursive(node.left, key)
        return self._search_recursive(node.right, key)

    def delete(self, key: str) -> None:
        self.root = self._delete_recursive(self.root, key)

    def _delete_recursive(self, node: Node | None, key: str) -> Node | None:
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.key:
            node.right = self._delete_recursive(node.right, key)
        else:
            # Node with only one child or no child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            # Node with two children: Get the inorder successor (smallest in the right subtree)
            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.value = temp.value
            node.right = self._delete_recursive(node.right, temp.key)
        return node

    def _min_value_node(self, node: Node) -> Node:
        current = node
        while current.left is not None:
            current = current.left
        return current

# Global BST instance
student_bst = BST()

def init_bst() -> None:
    """Initialize BST from the database."""
    logger.info("Initializing Student BST...")
    students = Student.get_all()
    count = 0
    for s in students:
        if s.enrollment_no and s.id:
            student_bst.insert(s.enrollment_no, s.id)
            count += 1
    logger.info(f"BST initialized with {count} students.")

def search_student(enrollment_no: str) -> int | None:
    """Search for a student ID by enrollment number."""
    return student_bst.search(enrollment_no)

def update_student_index(enrollment_no: str, student_id: int) -> None:
    """Update BST when a student is added or updated."""
    student_bst.insert(enrollment_no, student_id)

def remove_student_index(enrollment_no: str) -> None:
    """Remove from BST when a student is deleted."""
    student_bst.delete(enrollment_no)
