from backend.db import db

class PostUpVotes(db.Model):
    __tablename__ = 'post_upvotes'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('group_posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __init__(self, post_id, user_id):
        self.post_id = post_id
        self.user_id = user_id

    def __repr__(self):
        return f'<PostUpVotes {self.post_id} {self.user_id}>'