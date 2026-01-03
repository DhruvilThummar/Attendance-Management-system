"""BST-based student search stub."""
from __future__ import annotations


class Node:
    def __init__(self, key: str, value: int):
        self.key = key
        self.value = value
        self.left: Node | None = None
        self.right: Node | None = None


def insert(root: Node | None, key: str, value: int) -> Node:
    if root is None:
        return Node(key, value)
    if key < root.key:
        root.left = insert(root.left, key, value)
    elif key > root.key:
        root.right = insert(root.right, key, value)
    else:
        root.value = value
    return root


def search(root: Node | None, key: str) -> int | None:
    if root is None:
        return None
    if key == root.key:
        return root.value
    if key < root.key:
        return search(root.left, key)
    return search(root.right, key)
