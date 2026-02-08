"""
Proxy Status model for Proxy Lectures
"""

from .user import db


class ProxyStatus(db.Model):
    """Proxy lecture status lookup table (PENDING, ACCEPTED, REJECTED, COMPLETED)"""
    
    __tablename__ = 'proxy_status'
    
    status_id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String(50), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<ProxyStatus {self.status_name}>'
