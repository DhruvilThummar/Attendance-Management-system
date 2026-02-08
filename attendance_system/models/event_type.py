"""
Event Type model for Academic Calendar
"""

from .user import db


class EventType(db.Model):
    """Event type lookup table (REGULAR, EXAM, HOLIDAY)"""
    
    __tablename__ = 'event_type'
    
    event_type_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(50), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<EventType {self.event_name}>'
