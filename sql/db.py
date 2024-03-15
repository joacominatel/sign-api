# /sql/db.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    """
    Initialize the app with the database
    """
    db.init_app(app)
    
    with app.app_context():
        db.create_all()

        from sql.models.Roles import Roles
        Roles.insert_roles()

        from sql.models.NotificationType import NotificationType
        NotificationType.insert_types()

        from sql.models.User import User
        User.insert_admin_user()

        db.session.commit()
        
    return db