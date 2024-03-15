from sql.db import db
import datetime

class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, nullable=False)

    def __init__(
                    self,
                    name,
                    description,
                    owner_id,
                    created_at=datetime.datetime.now(),
                    updated_at=datetime.datetime.now(),
                    **kwargs
                ):
        
        self.name = name
        self.description = description
        self.owner_id = owner_id
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f'<Group {self.name}>'