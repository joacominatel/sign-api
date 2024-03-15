from sql.db import db

class Roles(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Role {self.name}>'

    # insert into db default roles (admin with id 1 and user with id 2)
    @staticmethod
    def insert_roles():
        roles = {
            'admin': Roles(name='admin'),
            'user': Roles(name='user')
        }
        # check if roles already exist
        for role in roles:
            if Roles.query.filter_by(name=role).first() is None:
                db.session.add(roles[role])
        db.session.commit()