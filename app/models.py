import datetime

from flask_login import UserMixin

from app import db, manager


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    __table_args__ = {'extend_existing': True}
    login = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    attempts = db.Column(db.Integer, default=0, nullable=False)

    def get_login(self):
        return str(User.login)


class Notebook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), default="My Notebook")
    __table_args__ = {'extend_existing': True}
    password = db.Column(db.String(100), default=None)
    last_modified = db.Column(db.DateTime, default=datetime.datetime.today())
    is_public = db.Column(db.Boolean, nullable=False, default=False)
    shared_uid = db.Column(db.String(100), default=None)


class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), default="New Note")
    __table_args__ = {'extend_existing': True}
    content = db.Column(db.Text, default=" ")
    notes_notebook = db.Column(db.Integer, nullable=False)
    last_modified = db.Column(db.DateTime, default=datetime.datetime.today())
    font = db.Column(db.String(25))
    color = db.Column(db.String(6))


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
