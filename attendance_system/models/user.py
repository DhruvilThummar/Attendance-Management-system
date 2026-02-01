"""Student and Faculty models - Inheritance from User."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from .base import User


class Student(User):
    """Student model - Inherits from User."""

    def __init__(
        self,
        id: int | None = None,
        user_id: int | None = None,
        dept_id: int | None = None,
        division_id: int | None = None,
        enrollment_no: str = "",
        roll_no: int | None = None,
        mentor_id: int | None = None,
        semester_id: int | None = None,
        **kwargs,
    ):
        super().__init__(id=id, **kwargs)
        self.user_id = user_id
        self.dept_id = dept_id
        self.division_id = division_id
        self.enrollment_no = enrollment_no
        self.roll_no = roll_no
        self.mentor_id = mentor_id
        self.semester_id = semester_id

    def validate(self) -> bool:
        """Validate student data."""
        return super().validate() and bool(self.enrollment_no and self.dept_id)

    def to_dict(self) -> dict[str, Any]:
        """Convert student to dictionary."""
        user_dict = super().to_dict()
        user_dict.update(
            {
                "user_id": self.user_id,
                "dept_id": self.dept_id,
                "division_id": self.division_id,
                "enrollment_no": self.enrollment_no,
                "roll_no": self.roll_no,
                "mentor_id": self.mentor_id,
                "semester_id": self.semester_id,
            }
        )
        return user_dict


class Faculty(User):
    """Faculty model - Inherits from User."""

    def __init__(
        self,
        id: int | None = None,
        user_id: int | None = None,
        dept_id: int | None = None,
        short_name: str = "",
        **kwargs,
    ):
        super().__init__(id=id, **kwargs)
        self.user_id = user_id
        self.dept_id = dept_id
        self.short_name = short_name

    def validate(self) -> bool:
        """Validate faculty data."""
        return super().validate() and bool(self.dept_id)

    def to_dict(self) -> dict[str, Any]:
        """Convert faculty to dictionary."""
        user_dict = super().to_dict()
        user_dict.update(
            {
                "user_id": self.user_id,
                "dept_id": self.dept_id,
                "short_name": self.short_name,
            }
        )
        return user_dict


class HOD(User):
    """HOD (Head of Department) model - Inherits from User."""

    def __init__(
        self,
        id: int | None = None,
        user_id: int | None = None,
        faculty_id: int | None = None,
        dept_id: int | None = None,
        **kwargs,
    ):
        super().__init__(id=id, **kwargs)
        self.user_id = user_id
        self.faculty_id = faculty_id
        self.dept_id = dept_id

    def validate(self) -> bool:
        """Validate HOD data."""
        return super().validate() and bool(self.dept_id)

    def to_dict(self) -> dict[str, Any]:
        """Convert HOD to dictionary."""
        user_dict = super().to_dict()
        user_dict.update(
            {
                "user_id": self.user_id,
                "faculty_id": self.faculty_id,
                "dept_id": self.dept_id,
            }
        )
        return user_dict


class Parent(User):
    """Parent model - Inherits from User."""

    def __init__(
        self,
        id: int | None = None,
        user_id: int | None = None,
        student_id: int | None = None,
        **kwargs,
    ):
        super().__init__(id=id, **kwargs)
        self.user_id = user_id
        self.student_id = student_id

    def validate(self) -> bool:
        """Validate parent data."""
        return super().validate() and bool(self.student_id)

    def to_dict(self) -> dict[str, Any]:
        """Convert parent to dictionary."""
        user_dict = super().to_dict()
        user_dict.update(
            {
                "user_id": self.user_id,
                "student_id": self.student_id,
            }
        )
        return user_dict
