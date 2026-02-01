"""Search service - BST-based efficient student search (Unit 4/5 Data Structures)."""

from __future__ import annotations

from typing import Optional, List, Any

from ..models.user import Student
from ..exceptions import StudentNotFoundError


class BSTNode:
    """Binary Search Tree Node for efficient student search."""

    def __init__(self, student: Student):
        self.student = student
        self.left: Optional[BSTNode] = None
        self.right: Optional[BSTNode] = None

    def __repr__(self) -> str:
        return f"BSTNode({self.student.enrollment_no})"


class StudentBST:
    """Binary Search Tree for efficient O(log n) student search by enrollment number."""

    def __init__(self):
        self.root: Optional[BSTNode] = None
        self.size = 0

    def insert(self, student: Student) -> bool:
        """Insert student into BST. Returns True if inserted, False if duplicate."""
        if not student.validate():
            return False

        if self.root is None:
            self.root = BSTNode(student)
            self.size += 1
            return True

        return self._insert_recursive(self.root, student)

    def _insert_recursive(self, node: BSTNode, student: Student) -> bool:
        """Recursive insertion helper."""
        enrollment_no = student.enrollment_no

        if enrollment_no < node.student.enrollment_no:
            if node.left is None:
                node.left = BSTNode(student)
                self.size += 1
                return True
            return self._insert_recursive(node.left, student)
        elif enrollment_no > node.student.enrollment_no:
            if node.right is None:
                node.right = BSTNode(student)
                self.size += 1
                return True
            return self._insert_recursive(node.right, student)
        else:
            # Duplicate enrollment number
            return False

    def search(self, enrollment_no: str) -> Optional[Student]:
        """Search for student by enrollment number. O(log n) average case."""
        node = self._search_recursive(self.root, enrollment_no)
        return node.student if node else None

    def _search_recursive(self, node: Optional[BSTNode], enrollment_no: str) -> Optional[BSTNode]:
        """Recursive search helper."""
        if node is None:
            return None

        if enrollment_no == node.student.enrollment_no:
            return node
        elif enrollment_no < node.student.enrollment_no:
            return self._search_recursive(node.left, enrollment_no)
        else:
            return self._search_recursive(node.right, enrollment_no)

    def delete(self, enrollment_no: str) -> bool:
        """Delete student by enrollment number."""
        old_size = self.size
        self.root = self._delete_recursive(self.root, enrollment_no)
        return self.size < old_size

    def _delete_recursive(self, node: Optional[BSTNode], enrollment_no: str) -> Optional[BSTNode]:
        """Recursive delete helper."""
        if node is None:
            return None

        if enrollment_no < node.student.enrollment_no:
            node.left = self._delete_recursive(node.left, enrollment_no)
        elif enrollment_no > node.student.enrollment_no:
            node.right = self._delete_recursive(node.right, enrollment_no)
        else:
            # Node to delete found
            self.size -= 1

            # Case 1: No children (leaf node)
            if node.left is None and node.right is None:
                return None

            # Case 2: One child
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            # Case 3: Two children - find in-order successor
            successor_parent = node
            successor = node.right

            while successor.left is not None:
                successor_parent = successor
                successor = successor.left

            # Replace node with successor
            node.student = successor.student
            node.right = self._delete_recursive(node.right, successor.student.enrollment_no)
            self.size += 1  # Compensate for the decrement in recursive call

        return node

    def in_order_traversal(self) -> List[Student]:
        """In-order traversal returns students sorted by enrollment number."""
        result = []
        self._in_order_helper(self.root, result)
        return result

    def _in_order_helper(self, node: Optional[BSTNode], result: List[Student]) -> None:
        """In-order traversal helper."""
        if node is None:
            return
        self._in_order_helper(node.left, result)
        result.append(node.student)
        self._in_order_helper(node.right, result)

    def get_all_students(self) -> List[Student]:
        """Get all students in sorted order."""
        return self.in_order_traversal()

    def __len__(self) -> int:
        return self.size

    def __repr__(self) -> str:
        return f"StudentBST(size={self.size})"


class SearchService:
    """Service for efficient student and staff search."""

    def __init__(self):
        self.student_bst = StudentBST()
        self.search_cache = {}

    def add_student(self, student: Student) -> bool:
        """Add student to search index."""
        return self.student_bst.insert(student)

    def find_student_by_enrollment(self, enrollment_no: str) -> Optional[Student]:
        """Find student by enrollment number (O(log n))."""
        student = self.student_bst.search(enrollment_no)
        if not student:
            raise StudentNotFoundError(
                f"Student with enrollment {enrollment_no} not found"
            )
        return student

    def find_student_by_roll(self, roll_no: int) -> Optional[Student]:
        """Find student by roll number - requires linear search through BST."""
        for student in self.student_bst.get_all_students():
            if student.roll_no == roll_no:
                return student
        raise StudentNotFoundError(f"Student with roll {roll_no} not found")

    def find_students_by_name(self, name: str) -> List[Student]:
        """Find students by name (partial match)."""
        results = []
        for student in self.student_bst.get_all_students():
            if name.lower() in student.name.lower():
                results.append(student)
        return results

    def find_students_by_division(self, division_id: int) -> List[Student]:
        """Find all students in a division."""
        results = []
        for student in self.student_bst.get_all_students():
            if student.division_id == division_id:
                results.append(student)
        return results

    def remove_student(self, enrollment_no: str) -> bool:
        """Remove student from index."""
        return self.student_bst.delete(enrollment_no)

    def get_all_students(self) -> List[Student]:
        """Get all students in sorted order."""
        return self.student_bst.get_all_students()

    def get_student_count(self) -> int:
        """Get total student count."""
        return len(self.student_bst)

    def clear_cache(self) -> None:
        """Clear search cache."""
        self.search_cache.clear()
