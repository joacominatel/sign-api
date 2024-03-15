from sql.db import db

class GroupMembers(db.Model):
    __tablename__ = 'group_members'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __init__(self, group_id, user_id):
        self.group_id = group_id
        self.user_id = user_id

    def __repr__(self):
        return f'<GroupMembers {self.group_id} {self.user_id}>'