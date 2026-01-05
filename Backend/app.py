from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
db = SQLAlchemy(app)
class User (db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_email = db.Column(db.String, unique = True)
    user_password_hash = db.Column(db.String, unique = True)
    user_role = db.Column(db.String, default = 'user')
    date_created_at = db.Column(db.DateTime, default = datetime.utcnow)
    employer = db.relationship('Employer', backref = 'user', uselist = False)
    

class Employer(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    company_name = db.Column(db.String)
    contact_person = db.Column(db.String)
    description_vacancy = db.Column(db.Text)
    contact_phone = db.Column(db.Integer)
    contact_website = db.Column(db.String)
    user_old = db.Column(db.Integer)
    user_name = db.Column(db.String)





if __name__ == '__main__':
    app.run(debug=True)