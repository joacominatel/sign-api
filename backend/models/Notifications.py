from backend.db import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('notification_type.id'), nullable=False)
    message = db.Column(db.String(255))
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('notifications', lazy=True))
    type = db.relationship('NotificationType', backref=db.backref('notifications', lazy=True))

    def __init__(self, user_id, type_id, message):
        self.user_id = user_id
        self.type_id = type_id
        self.message = message

    def __repr__(self):
        return f"<Notification(user_id='{self.user_id}', type_id='{self.type_id}', message='{self.message}', read='{self.read}')>"