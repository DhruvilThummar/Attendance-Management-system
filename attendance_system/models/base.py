"""
Base Model Classes - Core OOP Architecture
=========================================

This module contains the base model classes for the Attendance Management System.
Uses OOP principles with abstract base classes and inheritance.

Models:
- BaseModel: Abstract base class with common functionality
- User: Base user class for all system users

Author: Development Team
Version: 1.0
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any


class BaseModel(ABC):
    """
    Abstract Base Model Class
    
    Provides common functionality for all models in the system:
    - Unique identifier (id)
    - Timestamp tracking (created_at)
    - Abstract methods for to_dict() and validate()
    - String representation for debugging
    
    Usage:
        All model classes should inherit from BaseModel
        and implement the abstract methods.
    
    Attributes:
        id (int | None): Unique identifier
        created_at (datetime): Timestamp of creation
    """

    def __init__(self, id: int | None = None, created_at: datetime | None = None):
        """
        Initialize base model.
        
        Args:
            id: Unique identifier (auto-set if None)
            created_at: Creation timestamp (default: now)
        """
        self.id = id
        self.created_at = created_at or datetime.now()

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """
        Convert model instance to dictionary.
        
        Must be implemented by subclasses.
        Used for JSON serialization and data transfer.
        
        Returns:
            dict: Model data as dictionary
        """
        pass

    @abstractmethod
    def validate(self) -> bool:
        """
        Validate model data.
        
        Must be implemented by subclasses.
        Checks if all required fields are valid.
        
        Returns:
            bool: True if valid, False otherwise
        """
        pass

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"{self.__class__.__name__}(id={self.id})"


class User(BaseModel):
    """
    Base User Model Class
    
    Represents a user in the Attendance Management System.
    Base class for Student, Faculty, and HOD models.
    
    Features:
    - User authentication with password hash
    - Role-based access control (role_id)
    - Email and mobile contact info
    - Approval workflow (is_approved)
    - College/Institution affiliation
    
    Inheritance:
        Inherits from BaseModel
        Inherited by: Student, Faculty, HOD
    
    Attributes:
        college_id (int): College/Institution ID
        name (str): Full name of user
        email (str): Email address
        password_hash (str): Hashed password
        mobile (str): Mobile number
        role_id (int): Role ID for RBAC
        is_approved (bool): Approval status
    """

    def __init__(
        self,
        id: int | None = None,
        college_id: int | None = None,
        name: str = "",
        email: str = "",
        password_hash: str = "",
        mobile: str | None = None,
        role_id: int | None = None,
        is_approved: bool = False,
        created_at: datetime | None = None,
    ):
        """
        Initialize user.
        
        Args:
            id: User ID
            college_id: College/Institution ID
            name: User's full name
            email: User's email address
            password_hash: Hashed password
            mobile: User's mobile number
            role_id: User's role ID (for permissions)
            is_approved: Whether user is approved
            created_at: User creation timestamp
        """
        super().__init__(id, created_at)
        self.college_id = college_id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.mobile = mobile
        self.role_id = role_id
        self.is_approved = is_approved

    def validate(self) -> bool:
        """
        Validate user data.
        
        Checks if all required fields are present:
        - name: Not empty
        - email: Not empty (validated separately)
        - password_hash: Not empty
        
        Returns:
            bool: True if all required fields present
        """
        return bool(self.name and self.email and self.password_hash)

    def to_dict(self) -> dict[str, Any]:
        """
        Convert user to dictionary.
        
        Used for JSON serialization and API responses.
        
        Returns:
            dict: User data as dictionary
        """
        return {
            "id": self.id,
            "college_id": self.college_id,
            "name": self.name,
            "email": self.email,
            "mobile": self.mobile,
            "role_id": self.role_id,
            "is_approved": self.is_approved,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Role(BaseModel):
    """
    Role Model for RBAC (Role-Based Access Control)
    
    Defines user roles in the system with predefined constants.
    
    Available Roles:
    - 1: ADMIN - System administrator with full access
    - 2: HOD - Head of Department
    - 3: FACULTY - Teaching faculty
    - 4: STUDENT - Student account
    - 5: PARENT - Parent/Guardian account
    
    Usage:
        Used to determine user permissions and access level.
    
    Attributes:
        role_name (str): Name of the role
    """

    ROLES = {
        1: "ADMIN",
        2: "HOD",
        3: "FACULTY",
        4: "STUDENT",
        5: "PARENT",
    }

    def __init__(self, id: int | None = None, role_name: str = ""):
        """
        Initialize role.
        
        Args:
            id: Role ID (1-5)
            role_name: Role name from ROLES dictionary
        """
        super().__init__(id)
        self.role_name = role_name

    def validate(self) -> bool:
        """
        Validate role.
        
        Checks if role_name is in predefined ROLES.
        
        Returns:
            bool: True if valid role
        """
        return self.role_name in self.ROLES.values()

    def to_dict(self) -> dict[str, Any]:
        """
        Convert role to dictionary.
        
        Returns:
            dict: Role data as dictionary
        """
        return {
            "id": self.id,
            "role_name": self.role_name,
        }


class AttendanceStatus(BaseModel):
    """
    Attendance Status Model
    
    Represents attendance status values in the system.
    
    Available Statuses:
    - 1: PRESENT - Student is present
    - 2: ABSENT - Student is absent
    
    Usage:
        Used to mark and track attendance for lectures.
    
    Attributes:
        status_name (str): Status name from STATUSES dictionary
    """

    STATUSES = {
        1: "PRESENT",
        2: "ABSENT",
    }

    def __init__(self, id: int | None = None, status_name: str = ""):
        """
        Initialize attendance status.
        
        Args:
            id: Status ID (1-2)
            status_name: Status name from STATUSES dictionary
        """
        super().__init__(id)
        self.status_name = status_name

    def validate(self) -> bool:
        """
        Validate attendance status.
        
        Checks if status_name is in predefined STATUSES.
        
        Returns:
            bool: True if valid status
        """
        return self.status_name in self.STATUSES.values()

    def to_dict(self) -> dict[str, Any]:
        """
        Convert status to dictionary.
        
        Returns:
            dict: Status data as dictionary
        """
        return {
            "id": self.id,
            "status_name": self.status_name,
        }

    @property
    def is_present(self) -> bool:
        """
        Check if status is PRESENT.
        
        Returns:
            bool: True if student is present
        """
