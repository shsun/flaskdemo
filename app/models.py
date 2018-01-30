# http://docs.sqlalchemy.org/en/latest/core/type_basics.html#generic-types

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

import redis
import pickle


class User(UserMixin, db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))

    subject_id = db.Column(db.Integer, db.ForeignKey('careers.id'))
    subject = db.relationship('Career', backref='career')

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)

    notes = db.relationship('Note', lazy='select', backref=db.backref('user', lazy='joined'))

    def __repr__(self):
        return '<Career Field: {}>'.format(self.name)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Name: {}>'.format(self.username)

    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'User ID': self.id,
            'Email': self.email,
            'Username': self.username,
            'First Name': self.first_name,
            'Last Name': self.last_name,
            'CareerField': self.career.name,
            'Role': self.role.name
        }


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Career(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'careers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    users = db.relationship('User', backref='career', lazy='dynamic')

    def __repr__(self):
        return '<Career Field: {}>'.format(self.name)

    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'Career ID': self.id,
            'name': self.name,
            'Description': self.description,
            'Roles Included': [u.role.name for u in self.users],
            'Users': [u.username for u in self.users]
        }


class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)

    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'Role ID': self.id,
            'name': self.name,
            'Description': self.description,
            'Users': [u.username for u in self.users]
        }


class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    body = db.Column(db.Text)

    def __init__(self, title, body):
        self.title = title
        self.body = body

    def __repr__(self):
        return '<Note: {0}\n{1}>'.format(self.title, self.body)

    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'Note ID': self.id,
            'Title': self.title,
            'Description': self.body,
            'User': self.user.username
        }


class Redis:
    '''

    '''
    @staticmethod
    def new_connection(configObject):
        '''
        new connection
        :return:
        '''
        r = redis.StrictRedis(host=configObject['REDIS_HOST'], port=configObject['REDIS_PORT'], db=0)
        return r

    @staticmethod
    def set_data(r, key, data, ex=None):
        r.set(key, pickle.dumps(data), ex)

    @staticmethod
    def get_data(r, key):
        data = r.get(key)
        if data is None:
            return None
        return pickle.loads(data)
