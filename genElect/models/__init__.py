from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from genElect.utils.crypto import hash_password
from sqlalchemy.orm import validates

# create a new SQLAlchemy object

db = SQLAlchemy()


# Base model that for other models to inherit from
class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
            onupdate=db.func.current_timestamp())


class Notifications(Base):
    notification = db.Column(db.String(1000))

class Roles(Base): 
    role = db.Column(db.String(100))

class Users(Base): 
    username = db.Column(db.String(100))
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    role = db.relationship('Roles', lazy=True)
    password = db.Column(db.String(128))


    @validates('password')
    def validate_password(self, key, plaintext):
        return hash_password(str(plaintext))

    # Future VIP registration option
    early_reg = db.Column(db.Boolean)

    def __init__(self, role_id):
        self.role_id = role_id
        self.early_reg = True

class Registrations(Base):
    user_id = db.relationship('Users', lazy=True)
    offering_id = db.relationship('Offerings', lazy=True)

    def __init__(self, username, offering_id):
        self.user_id = username
        self.offering_id = offering_id

class Offerings(Base):
    day = db.Column(db.Date)
    period_start = db.Column(db.Integer)
    period_length = db.Column(db.Integer)
    building = db.Column(db.String(100))
    room = db.Column(db.String(100))
    elective_id = db.relationship('Electives', lazy=True)

    def __init__(self, elective_id):
        self.elective_id  = elective_id

class Electives(Base):
    name = db.Column(db.String(100))
    instructor = db.Column(db.String(100)) 
    description = db.Column(db.String(500))
    prerequisites = db.Column(db.String(500))
    capacity = db.Column(db.Integer)