# /backend/db.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    """
    Initialize the app with the database
    """
    db.init_app(app)
    
    with app.app_context():
        db.create_all()

        from backend.models.Roles import Roles
        Roles.insert_roles()

        db.session.commit()
        
    return db