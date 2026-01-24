from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Any, ClassVar, List, Optional
from ..db_manager import execute, fetch_one

@dataclass
class BaseModel:
    """Base model providing raw SQL CRUD operations (MySQL compatible)."""
    __table__: ClassVar[str]
    id: Optional[int] = None

    @classmethod
    def get_by_id(cls, id: int) -> Optional['BaseModel']:
        """Fetch a single record by ID."""
        query = f"SELECT * FROM {cls.__table__} WHERE id = %s"
        row = fetch_one(query, (id,))
        return cls(*row) if row else None

    @classmethod
    def get_all(cls) -> List['BaseModel']:
        """Fetch all records."""
        query = f"SELECT * FROM {cls.__table__}"
        rows = execute(query)
        return [cls(*row) for row in rows]

    def save(self) -> None:
        """Insert or Update the record."""
        data = asdict(self)
        if 'id' in data and data['id'] is None:
            del data['id']
        
        columns = list(data.keys())
        values = list(data.values())
        
        if self.id:
            # Update
            set_clause = ", ".join([f"{col} = %s" for col in columns])
            query = f"UPDATE {self.__table__} SET {set_clause} WHERE id = %s"
            execute(query, values + [self.id])
        else:
            # Insert
            cols_clause = ", ".join(columns)
            vals_clause = ", ".join(["%s"] * len(values))
            query = f"INSERT INTO {self.__table__} ({cols_clause}) VALUES ({vals_clause})"
            
            # Use the refactored execute which now returns lastrowid for INSERT
            new_id = execute(query, values)
            if new_id:
                self.id = new_id

    def delete(self) -> None:
        """Delete the record."""
        if self.id:
            query = f"DELETE FROM {self.__table__} WHERE id = %s"
            execute(query, (self.id,))
