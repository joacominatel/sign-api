from backend.db import db
import datetime

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=True)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.TIMESTAMP, nullable=True)
    priority = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Boolean, nullable=False)

    user = db.relationship('User', backref=db.backref('tasks', lazy=True))
    group = db.relationship('Group', backref=db.backref('tasks', lazy=True))


    def __init__(self,
                    user_id,
                    title,
                    description,
                    due_date=datetime.datetime.now(),
                    priority=1,
                    completed=False):
            

            self.user_id = user_id
            self.title = title
            self.description = description
            self.due_date = due_date
            self.priority = priority
            self.completed = completed

    def __repr__(self):
        return f'<Task {self.title}>'