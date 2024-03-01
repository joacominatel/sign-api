from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Boolean
from backend.db import db

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    name = Column(String(50), nullable=True)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    profile_image_url = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    def __init__(self, username, name, email, password, created_at, updated_at, is_active=True, profile_image_url='../default-user.webp', **kwargs):
        self.username = username
        self.name = name
        self.email = email
        self.password = password
        self.profile_image_url = profile_image_url
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_active = is_active


    def __repr__(self):
        return f'<User {self.username}>'

