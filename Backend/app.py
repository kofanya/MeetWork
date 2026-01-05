from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
db = SQLAlchemy(app)
class User (db.Model):
    id = db.Column(db.Integer,primary_key = True)
    first_name = db.Column(db.String)
    second_name = db.Column(db.String)
    last_name = db.Column(db.String)
    old = db.Column(db.Integer)
    contact_phone = db.Column(db.String)
    email = db.Column(db.String, unique = True)
    password_hash = db.Column(db.String)
    role = db.Column(db.String, default = 'applicant')
    date_created_at = db.Column(db.DateTime, default = datetime.utcnow)
    employer = db.relationship('Employer', backref = 'user', uselist = False)
    applicant = db.relationship('Applicant', backref = 'user', uselist = False)
    admin = db.relationship('Admin', backref = 'user', uselist = False)
    
class Employer(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    company_name = db.Column(db.String)
    description_vacancy = db.Column(db.Text)
    contact_website = db.Column(db.String)

class Applicant(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    resume = db.Column(db.Text)
    education = db.Column(db.String)

class Admin(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)



if __name__ == '__main__':
    app.run(debug=True)