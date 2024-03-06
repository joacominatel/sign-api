from backend.db import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profile_image_url = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.TIMESTAMP, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

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

    @classmethod
    def insert_admin_user(cls):
        from backend.models.Roles import Roles
        from backend.models.UserRoles import UserRoles
        from backend.models.User import User
        from backend.db import db
        from datetime import datetime

        admin = User.query.filter_by(username='admin').first()
        if admin is None:
            admin = User(
                username='admin',
                name='Admin',
                email='admin@admin.com',
                password='admin',
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            db.session.add(admin)
            db.session.commit()

        else:
            print('Username: admin')
            print('Password: admin')