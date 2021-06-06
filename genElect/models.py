from flask import Flask, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import validates
from genElect import db

# Base model that for other models to inherit from
class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
            onupdate=db.func.current_timestamp())


class Notifications(Base):
    title = db.Column(db.String(100))
    notification = db.Column(db.String(1000))

class Users(Base, UserMixin):
    __tablename__ = 'users'
    username = db.Column(db.String(100), unique=True)
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    role = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(128))
    registrations = db.relationship('Registrations', backref='user', lazy=True)
    core_registrations = db.relationship('CoreRegistrations', backref='user', lazy=True)
    completed_electives = db.relationship('Completions', backref='user', lazy=True)
#    completed_badge_portions = db.relationship('BadgePortions', backref='user', lazy=True) ADD BACK IF BADGES ARE ADDED

    # # Future VIP registration option
    # early_reg = db.Column(db.Boolean)

    # def __init__(self, role_id):
    #     self.role_id = role_id
    #     self.early_reg = True

class Registrations(Base):
    __tablename__ = 'registrations'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    offering_id = db.Column(db.Integer, db.ForeignKey('offerings.id'), nullable=False)

class CoreRegistrations(Base):
    __tablename__ = 'coreregistrations'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    core_id = db.Column(db.Integer, db.ForeignKey('cores.id'), nullable=False)

class Offerings(Base):
    __tablename__ = 'offerings'
    day = db.Column(db.Date)
    period_start = db.Column(db.Integer)
    period_length = db.Column(db.Integer)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    instructor = db.Column(db.String(100))
    current_count = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
    elective_id = db.Column(db.Integer, db.ForeignKey('electives.id'), nullable=False)
    registrations = db.relationship('Registrations', backref='offering', lazy=True)

#     def __init__(self, elective_id):
#         self.elective_id  = elective_id

class Electives(Base):
    __tablename__ = 'electives'
    name = db.Column(db.String(100))
    description = db.Column(db.String(500))
    learning_objective = db.Column(db.String(500))
    prerequisites = db.relationship('Prerequisites', backref='elective', lazy=True)
    offerings = db.relationship('Offerings', backref='elective', lazy=True)
    completed_users = db.relationship('Completions', backref='elective', lazy=True)
    can_retake = db.Column(db.Boolean)
    elective_difficulty = db.Column(db.String(100))

class Cores(Base):
    __tablename__ = 'cores'
    name = db.Column(db.String(100))
    description = db.Column(db.String(500))
    building = db.Column(db.String(100))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    core_period = db.Column(db.Integer)
    core_difficulty = db.Column(db.String(100))
    instructor = db.Column(db.String(100))
    registrations = db.relationship('CoreRegistrations', backref='core', lazy=True)


class Completions(Base):
    __tablename__ = 'completions'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    elective_id = db.Column(db.Integer, db.ForeignKey('electives.id'), nullable=False)


class Prerequisites(Base):
    __tablename__ = 'prerequisites'
    elective_id = db.Column(db.Integer, db.ForeignKey('electives.id'), nullable=False)
    prerequisite_elective_id = db.Column(db.Integer, nullable=False)

class Configs(Base):
    __tablename__ = 'configs'
    key = db.Column(db.Text)
    value = db.Column(db.Text)

class Building(Base):
    __tablename__ = 'buildings'
    name = db.Column(db.String(100), nullable=False, unique=True)
    rooms = db.relationship('Room', backref='building', lazy=True, cascade="all,delete")

    def __repr__(self):
        return self.name

class Room(Base):
    __tablename__ = 'rooms'
    name = db.Column(db.String(50), nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'))
    events = db.relationship('Event', backref='room', lazy=True, cascade="all,delete")
    offerings = db.relationship('Offerings', backref='room', cascade="all,delete")
    cores = db.relationship('Cores', backref='room', cascade="all,delete")

    def __repr__(self):
        return self.building.name + " - " + self.name

class Event(Base):
    __tablename__ = 'events'
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    description = db.Column(db.String(250), nullable=False)

    def jsEvent(self):
        obj = {
            'id': self.id,
            'title': self.title + " @ " + str(self.room),
            'start': self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'end': self.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            'url': url_for('editevent', id=self.id),
            'html': render_template('eventmodal.html', event=self)
        }
        return obj



#### PLAYING WITH THE IDEA OF HAVING BADGES WILL ADD AFTER FIRST YEAR ON NEW
#### COULD BE COOL TO ALSO EXPORT AND IMPORT THE DIFFERENT BADGES THAT STUDENTS EARN

# class Badges(Base):
#     __tablename__ = 'badges'
#     name = db.Column(db.String(100))
#     description = db.Column(db.String(500))
#     portions = db.relationship('BadgePortions', backref='badge', lazy=True)

# #THIS WILL MAP BADGE PARTS (like have to complete python 1 and 2 for the python badge)
# class BadgePortions(Base):
#     __tablename__ = 'badgeportions'
#     badge_id = db.Column(db.Integer, db.ForeignKey('badges.id'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
