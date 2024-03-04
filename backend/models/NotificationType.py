from datetime import datetime
from backend.db import db

class NotificationType(db.Model):
    __tablename__ = 'notification_type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<NotificationType(name='{self.name}')>"
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }
    
    @staticmethod
    def insert_types():
        types = ['New Group', 'New Upvote', 'New Post', 'Deleted from Group', 'Admin privileges', 'System Notification']
        for type in types:
            notification_type = NotificationType.query.filter_by(name=type).first()
            if notification_type is None:
                notification_type = NotificationType(type)
                db.session.add(notification_type)
        db.session.commit()