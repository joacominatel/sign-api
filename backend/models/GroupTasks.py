from backend.db import db

class GroupTasks(db.Model):
    __tablename__ = 'group_tasks'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)

    def __init__(self, group_id, task_id):
        self.group_id = group_id
        self.task_id = task_id

    def __repr__(self):
        return f'<GroupTasks {self.id}>'