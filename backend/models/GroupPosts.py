from backend.db import db

class GroupPosts(db.Model):
    __tablename__ = 'group_posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, nullable=False)
    
    def __init__(self, group_id, user_id, title, content, created_at, updated_at):
        self.group_id = group_id
        self.user_id = user_id
        self.title = title
        self.content = content
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f'<GroupPosts {self.group_id} {self.user_id} {self.title}>'