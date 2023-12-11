from datetime import datetime
from app import db, login
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ForeignKey
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

#class Post(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    title = db.Column(db.String(150))
#    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#    happiness_level = db.Column(db.Integer, default = 3)


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True)
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    user_type = db.Column(db.String(50))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), unique=True)
    phone_number = db.Column(db.Integer, unique=True)

    __mapper_args__ = {
        "polymorphic_identity": "employee",
        "polymorphic_on": "user_type",
    }

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def check_password(self, password):
        return self.get_password(password)

# major to student association table
majoring_in = db.Table('majoring_in',
    db.Column('id_of_student', db.Integer, db.ForeignKey('student.id')),
    db.Column('id_of_major', db.Integer, db.ForeignKey('major.id'))
)

# programming language to student association table
knows_language = db.Table('knows_language',
    db.Column('id_of_student', db.Integer, db.ForeignKey('student.id')),
    db.Column('id_of_language',db.Integer, db.ForeignKey('proglang.id'))
)

# major to opening association table
expects_major = db.Table('expects_major',
    db.Column('opening_id', db.Integer, db.ForeignKey('opening.id')),
    db.Column('major_id', db.Integer, db.ForeignKey('major.id'))
)

# programming language to opening association table
expects_language = db.Table('expects_language',
    db.Column('opening_id', db.Integer, db.ForeignKey('opening.id')),
    db.Column('language_id',db.Integer, db.ForeignKey('proglang.id'))
)


#created = db.Table('created',
#    db.Column('professor_id', db.Integer, db.ForeignKey('professor.id')),
#    db.Column('opening_id', db.Integer, db.ForeignKey('opening.id'))    
#)
    
class Major(db.Model):
    __tablename__ = 'major'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    students = db.relationship(
        'Student', secondary=majoring_in,
        primaryjoin=(majoring_in.c.id_of_major == id), lazy='dynamic', overlaps="majors")
    openings = db.relationship(
        'Opening', secondary=expects_major,
        primaryjoin=(expects_major.c.major_id == id), lazy='dynamic', overlaps="majors")
    
    def __repr__(self):
        return "<Major {} {}>".format(self.id, self.name) 
    
class ProgLang(db.Model):
    __tablename__ = 'proglang'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    students = db.relationship(
        'Student', secondary=knows_language,
        primaryjoin=(knows_language.c.id_of_language == id), lazy='dynamic', overlaps="programming_languages")
    openings = db.relationship(
        'Opening', secondary=expects_language,
        primaryjoin=(expects_language.c.language_id == id), lazy='dynamic', overlaps="programming_langauges")
    
    def __repr__(self):
        return "<ProgLang {} {}>".format(self.id, self.name)
    

class Student(User):
    __tablename__ = 'student'
    id = db.Column(db.ForeignKey('user.id'), primary_key = True)
    student_id = db.Column(db.Integer, unique=True)
    graduation_date = db.Column(db.DateTime)
    gpa = db.Column(db.Float) # I think float is right here but I'm not sure
    research_history = db.Column(db.String(500)) # There's probably a better way to do this, but we can do that in a later iteration
    majors = db.relationship(
        'Major', secondary=majoring_in,
        primaryjoin=(majoring_in.c.id_of_student == id), lazy='dynamic', overlaps="students")
    programming_languages = db.relationship(
        'ProgLang', secondary=knows_language,
        primaryjoin=(knows_language.c.id_of_student == id), lazy='dynamic', overlaps="students")
    applications = db.relationship('Application', backref = 'applicant', lazy = "dynamic")

    __mapper_args__ = {
        "polymorphic_identity": "Professor",
    }
    
    __mapper_args__ = {
        "polymorphic_identity": "Student",
    }

class Professor(User):
    __tablename__ = 'professor'
    id = db.Column(db.ForeignKey("user.id"), primary_key = True)
    openings = db.relationship('Opening', backref = 'creator', lazy = "dynamic")
    __mapper_args__ = {
        "polymorphic_identity": "Professor",
    }

class Opening(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(800))
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    time_commitment = db.Column(db.Integer)
    creator_id = db.Column(db.Integer,db.ForeignKey('professor.id'))
    majors = db.relationship(
        'Major', secondary=expects_major,
        primaryjoin=(expects_major.c.opening_id == id), lazy='dynamic', overlaps="openings")
    programming_languages = db.relationship(
        'ProgLang', secondary=expects_language,
        primaryjoin=(expects_language.c.opening_id == id), lazy='dynamic', overlaps="openings")
    applications = db.relationship('Application', backref = 'opening', lazy = "dynamic")
    
class Application(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    interest_statement = db.Column(db.String(500))
    reference_name = db.Column(db.String(100))
    reference_email = db.Column(db.String(120), unique=True)
    applicant_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    opening_id = db.Column(db.Integer, db.ForeignKey('opening.id'))