from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, redirect, url_for, jsonify,make_response
from datetime import datetime
from flask_restful import Api, Resource, reqparse ,marshal_with,marshal,fields
from werkzeug.security import check_password_hash,generate_password_hash
from flask_jwt_extended import  (
    create_access_token,
    create_refresh_token,
    jwt_required,
    JWTManager,
    get_jwt_identity,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
    get_jwt
)
app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['JWT_SECRET_KEY'] = '834g93gb9ug34u9njscd234kmpiq3jipwuo3v55vu94fpi53foqfm3ipw7vu959uw'

class User (db.Model):
    id = db.Column(db.Integer,primary_key = True)
    first_name = db.Column(db.String(50))
    second_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    contact_phone = db.Column(db.String(20))
    email = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(255))
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

@jwt.token_in_blocklist_loader
def check(jwt_payload):
    jti = jwt_payload['jti']
    token = Token_Black_list.query.filter_by(jti = jti).first()
    return token is not None

class Token_Black_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True)
    revoked_on = db.Column(db.DateTime, default=datetime.utcnow)


class Register(Resource):
    def post(self):
        data_user = request.get_json()
        if not data_user:
            return jsonify({'message': 'Данные пользователя для регистрации JSON не были получены сервером'}),400
        else:
            psw_hash = generate_password_hash(data_user['password'])
            new_user = User(first_name = data_user['first_name'],
                            second_name = data_user['second_name'],
                            last_name = data_user['last_name'],
                            age = data_user['age'],
                            contact_phone = data_user['contact_phone'],
                            email = data_user['email'],
                            password = psw_hash,)
            try:
                db.session.add(new_user)
                db.session.commit()
                return jsonify({'message':'Вы успешно зарегистрировались в БД'}),201
            except Exception as e:
                db.session.rollback()
                return jsonify({'message': 'При регистрации произошла ошибка на стороне БД','error': str(e)}),500
api.add_resource(Register,'/api/register')

class Login(Resource):
    def post(self):
        data_login = request.get_json()
        if not data_login:
            return jsonify({'message': 'Данные пользователя для аунтификации JSON не были получены сервером'}),400
        else:
            email = data_login['email']
            psw = data_login['password']
            user = User.query.filter_by(email = email).first()
            if check_password_hash(user.password, psw) and user:
                claim = {'first_name': user.first_name,'role': user.role}
                access_token = create_access_token(identity=str(user.id),additional_claims=claim)
                refresh_token = create_refresh_token(identity=str(user.id),additional_claims = claim)
                response_data = {'message': 'Вы успешно прошли аунтификацию','first_name': user.first_name,'role': user.role}
                response = make_response(jsonify(response_data),200)
                set_access_cookies(response,access_token)
                set_refresh_cookies(response,refresh_token)
                return response
            else:
                return jsonify({'message': 'Пользователья не существует или неверный пароль'}),404
api.add_resource(Login,'/api/login')

class Logout(Resource):
    @jwt_required(refresh=True)
    def get(self):
        jti = get_jwt()['jti']
        entry = Token_Black_list(jti = jti)
        try:
            db.session.add(entry)
            db.session.commit()
            response = make_response(jsonify({'message': 'Вы успешно вышли из профиля'}),200)
            unset_jwt_cookies(response)
            return response
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Произошла ошибка выхода из профиля на стороне БД', 'error': str(e)}),500
api.add_resource(Logout,'/api/logout')

class Profile(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        user_role = get_jwt()['role']
        current_user = User.query.filter_by(id = user_id).first()
        data_user = {'first_name': current_user.first_name, 'second_name': current_user.second_name, 'last_name': current_user.last_name,
                     'age': current_user.age, 'contact_phone': current_user.contact_phone, 'email': current_user.email,
                          }










        
        














with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)