from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
db = SQLAlchemy(app)

class User (db.Model):
    id = db.Column(db.Integer,primary_key = True)
    first_name = db.Column(db.String(50))
    second_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    contact_phone = db.Column(db.String(20))
    email = db.Column(db.String(120), unique = True)
    password_hash = db.Column(db.String(255))
    role = db.Column(db.String(20), default = 'applicant')
    date = db.Column(db.DateTime, default = datetime.utcnow)
    employer = db.relationship('Employer', backref = 'user', uselist = False)
    applicant = db.relationship('Applicant', backref = 'user', uselist = False)
    event = db.relationship('Event', backref='organizer')
    comment_vacancy = db.relationship('Comment_vacancy',backref = 'user')
    comment_event = db.relationship('Comment_event',backref = 'user')
    recipient = db.relationship('Notification',foreign_keys = [('Notification.recipient_user_id')],backref = 'recipient_user')
    sender = db.relationship('Notification',foreign_keys = [('Notification.sender_user_id')],backref = 'sender_user')
    sign_appointment = db.relationship('Sign_appointment',backref = 'user')
    sign_vacancy = db.relationship('Sign_vacancy', backref = 'user')
    
    
class Employer(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    company_name = db.Column(db.String(100))
    contact_website = db.Column(db.String(120),default = 'Сайта нет')
    vacancy = db.relationship('Vacancy', backref = 'employer')
    
class Applicant(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    resume = db.Column(db.Text)
    education = db.Column(db.String(150))

class Vacancy(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    employer_id = db.Column(db.Integer, db.ForeignKey('employer.user_id'))
    title = db.Column(db.String(100))
    intro = db.Column(db.String(200))
    description = db.Column(db.Text)
    requirements = db.Column(db.Text)
    salary_min = db.Column(db.Integer)
    salary_max = db.Column(db.Integer)
    location = db.Column(db.String(100))
    date = db.Column(db.DateTime, default = datetime.utcnow)
    comment_vacancy = db.relationship('Comment_vacancy',backref = 'vacancy')
    sign_vacancy = db.relationship('Sign_vacancy',backref = 'vacancy')

class Event(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(100))
    intro = db.Column(db.String(200))
    description = db.Column(db.Text)
    requirements = db.Column(db.Text)
    location = db.Column(db.String(100))
    capacity = db.Column(db.Integer)
    date = db.Column(db.DateTime, default = datetime.utcnow)
    comment_event = db.relationship('Comment_event',backref = 'event')
    sign_appointment = db.relationship('Sign_appointment',backref = 'event')

class Comment_event(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer,db.ForeignKey('event.id'))
    text = db.Column(db.Text)
    date = db.Column(db.DateTime, default = datetime.utcnow)

class Comment_vacancy(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    vacancy_id = db.Column(db.Integer,db.ForeignKey('vacancy.id'))
    text = db.Column(db.Text)
    date = db.Column(db.DateTime, default = datetime.utcnow)

class Notification(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    recipient_user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    sender_user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    title = db.Column(db.String(100))
    message = db.Column(db.Text)
    date = db.Column(db.DateTime, default = datetime.utcnow)

class Sign_appointment(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    organizer_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer,db.ForeignKey('event.id'))
    date = db.Column(db.DateTime, default = datetime.utcnow)

class Sign_vacancy(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    applicant_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    vacancy_id = db.Column(db.Integer,db.ForeignKey('vacancy.id'))
    date = db.Column(db.DateTime, default = datetime.utcnow)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)