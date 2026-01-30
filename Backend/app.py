from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, redirect, url_for, jsonify,make_response
from datetime import datetime, timezone
from flask_restful import Api, Resource, reqparse ,marshal_with,marshal,fields
from werkzeug.security import check_password_hash,generate_password_hash
from flask_jwt_extended import (
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['JWT_SECRET_KEY'] = '834g93gb9ug34u9njscd234kmpiq3jipwuo3v55vu94fpi53foqfm3ipw7vu959uw'
app.config['JWT_TOKEN_LOCATION'] = ['cookies'] 
app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token_cookie'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False  
api = Api(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)

@jwt.unauthorized_loader
def unauthorized_callback(error_string):
    print(" [JWT] Unauthorized:", error_string)
    return jsonify({"message": "Токен отсутствует или недействителен"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error_string):
    print(" [JWT] Invalid token:", error_string)
    return jsonify({"message": "Недействительный токен"}), 401

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    print(" [JWT] Token expired:", jwt_payload)
    return jsonify({"message": "Срок действия токена истёк"}), 401

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    print(" [JWT] Token revoked:", jwt_payload)
    return jsonify({"message": "Токен отозван"}), 401

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
    recipient = db.relationship('Notification',foreign_keys = 'Notification.recipient_user_id',backref = 'recipient_user')
    sender = db.relationship('Notification',foreign_keys = 'Notification.sender_user_id',backref = 'sender_user')
    sign_appointment = db.relationship('Sign_appointment', foreign_keys='Sign_appointment.applicant_id', backref='applicant_user')
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
    is_active = db.Column(db.Boolean, default = True)
    comment_vacancy = db.relationship('Comment_vacancy',backref = 'vacancy')
    sign_vacancy = db.relationship('Sign_vacancy',backref = 'vacancy')
    category = db.Column(db.String(50))

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
    category = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default = True)
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
    is_read = db.Column(db.Boolean, default=False)

class Sign_appointment(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    applicant_id = db.Column(db.Integer,db.ForeignKey('user.id'))                       
    event_id = db.Column(db.Integer,db.ForeignKey('event.id'))
    date = db.Column(db.DateTime, default = datetime.utcnow)
    status = db.Column(db.String(20), default = 'pending')

class Sign_vacancy(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    applicant_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    vacancy_id = db.Column(db.Integer,db.ForeignKey('vacancy.id'))
    date = db.Column(db.DateTime, default = datetime.utcnow)
    status = db.Column(db.String(20), default = 'pending')

@jwt.token_in_blocklist_loader
def check(jwt_header,jwt_payload):
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
            return {'message': 'Данные пользователя для регистрации JSON не были получены сервером'},400
        else:
            if User.query.filter_by(email = data_user['email']).first():
                return {'message':'Вы уже зарегистрированы на сайте'},400
            else:
                psw_hash = generate_password_hash(data_user['password'])
                new_user = User(first_name = data_user['first_name'],
                                second_name = data_user['second_name'],
                                last_name = data_user['last_name'],
                                age = data_user['age'],
                                contact_phone = data_user['contact_phone'],
                                email = data_user['email'],
                                password = psw_hash,
                                role = data_user.get('role', 'applicant'))
                try:
                    db.session.add(new_user)
                    db.session.commit()
                    return {'message':'Вы успешно зарегистрировались в БД'},201
                except Exception as e:
                    db.session.rollback()
                    return {'message': 'При регистрации произошла ошибка на стороне БД','error': str(e)},500
api.add_resource(Register,'/api/register')

class Login(Resource):
    def post(self):
        data_login = request.get_json()
        if not data_login:
            return {'message': 'Данные пользователя для аунтификации JSON не были получены сервером'},400
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
                return {'message': 'Пользователья не существует или неверный пароль'},404
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
            return {'message': 'Произошла ошибка выхода из профиля на стороне БД', 'error': str(e)},500
api.add_resource(Logout,'/api/logout')

class Profile(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        current_user = User.query.get(user_id)
        if not current_user:
             return {'message': 'Пользователь не найден'}, 404
        data_user = {
            'first_name': current_user.first_name,
            'second_name': current_user.second_name,
            'last_name': current_user.last_name,
            'age': current_user.age,
            'contact_phone': current_user.contact_phone,
            'email': current_user.email,
            'role': current_user.role
        }

        if current_user.role == 'employer':
            employer_info = None
            if current_user.employer:
                employer_info = {
                    'company_name': current_user.employer.company_name,
                    'contact_website': current_user.employer.contact_website
                }
            return {'information': employer_info, 'data_user': data_user}, 200
        
        elif current_user.role == 'applicant':
            applicant_info = None
            if current_user.applicant:
                applicant_info = {
                    'resume': current_user.applicant.resume,
                    'education': current_user.applicant.education
                }
            return {'information': applicant_info, 'data_user': data_user}, 200
        
        else:
            return {'data_user': data_user}, 200
    @jwt_required()
    def post(self):
        data_user = request.get_json()
        if not data_user:
            return {'message': 'Данные пользователя для добавления JSON не были получены сервером'},400
        else:
            user_id = int(get_jwt_identity())
            current_user = User.query.filter_by(id = user_id).first()
            if current_user.role == 'employer':
                employer_information = Employer(user_id = user_id, company_name = data_user.get('company_name'),
                                                contact_website = data_user.get('contact_website'))
                try:
                    db.session.add(employer_information)
                    db.session.commit()
                    return {'message': 'Данные работодателя обновлены'}, 201
                except Exception as e:
                    db.session.rollback()
                    return {'message': 'Ошибка при добавлении данных работодателя', 'error': str(e)}, 500
            elif current_user.role == 'applicant':
                applicant_information = Applicant(user_id = user_id, resume = data_user.get('resume'), education = data_user.get('education'))
                try:
                    db.session.add(applicant_information)
                    db.session.commit()
                    return {'message': 'Данные соискателя обновлены'}, 201
                except Exception as e:
                    db.session.rollback()
                    return {'message': 'Ошибка при добавлении данных соискателя', 'error': str(e)}, 500  
    @jwt_required()
    def put(self):
        data_user = request.get_json()
        if not data_user:
            return {'message': 'Данные для изменения не получены'}, 400

        user_id = int(get_jwt_identity())
        current_user = User.query.get(user_id)
        if not current_user:
            return {'message': 'Пользователь не найден'}, 404

        user_fields = ['first_name', 'second_name', 'last_name', 'age', 'contact_phone']
        employer_fields = ['company_name', 'contact_website']
        applicant_fields = ['resume', 'education']

        for key, value in data_user.items():
            if key in user_fields:
                setattr(current_user, key, value)

        if current_user.role == 'employer':
            if not current_user.employer:
                current_user.employer = Employer(user_id=current_user.id)
            for key, value in data_user.items():
                if key in employer_fields:
                    setattr(current_user.employer, key, value)

        elif current_user.role == 'applicant':
            if not current_user.applicant:
                current_user.applicant = Applicant(user_id=current_user.id)
            for key, value in data_user.items():
                if key in applicant_fields:
                    setattr(current_user.applicant, key, value)

        try:
            db.session.commit()
            return {'message': 'Данные пользователя успешно обновлены'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': 'Ошибка при обновлении данных пользователя в БД', 'error': str(e)}, 500
api.add_resource(Profile, '/api/profile')

class VacancyResource(Resource):
    def get(self, vacancy_id=None):
        if vacancy_id is None:
            # Список всех вакансий
            active_vacancies = Vacancy.query.filter_by(is_active=True).all()
            result = []
            for v in active_vacancies:
                result.append({
                    'id': v.id,
                    'title': v.title,
                    'salary_min': v.salary_min,
                    'salary_max': v.salary_max,
                    'company_name': v.employer.company_name if v.employer else "Unknown",
                    'category': v.category,
                    'location': v.location,
                    'date': v.date.isoformat() if v.date else None
                })
            return {'vacancies': result}, 200
        else:
            v = Vacancy.query.get(vacancy_id)
            if not v or not v.is_active:
                return {'message': 'Вакансия не найдена'}, 404

            return {
                'id': v.id,
                'title': v.title,
                'intro': v.intro,
                'description': v.description,
                'requirements': v.requirements,
                'salary_min': v.salary_min,
                'salary_max': v.salary_max,
                'location': v.location,
                'company_name': v.employer.company_name if v.employer else "Unknown",
                'category': v.category,
                'date': v.date.isoformat() if v.date else None
            }, 200

    @jwt_required()
    def post(self):
        try:
            user_id = int(get_jwt_identity())
            print("User ID from token:", user_id)  
        except Exception as e:
            print("JWT error:", e)
            return {'message': 'Invalid token'}, 401
        data = request.get_json()
        user_id = int(get_jwt_identity())
        current_user = User.query.get(user_id)
        
        if current_user.role != 'employer':
            return {'message': 'Только работодатель может создавать вакансии'}, 403
        
        if not current_user.employer:
            return {
                'message': 'Заполните информацию о компании в личном кабинете перед созданием вакансии'
            }, 400

        employer = current_user.employer
        if not employer.company_name or not employer.company_name.strip():
            return {
                'message': 'Укажите название компании в личном кабинете перед созданием вакансии'
            }, 400
        try:
            salary_min = int(data.get('salary_min', 0))
            salary_max = int(data.get('salary_max', 0))

            if salary_min < 0 or salary_max < 0:
                return {'message': 'Зарплата не может быть отрицательной'}, 400
            
            if salary_min > salary_max:
                return {'message': 'Минимальная зарплата не может быть больше максимальной'}, 400
                
        except (ValueError, TypeError):
             return {'message': 'Зарплата должна быть числом'}, 400

        new_vacancy = Vacancy(
            employer_id = user_id,
            title = data.get('title'),
            description = data.get('description'),
            requirements=data.get('requirements', ''),
            location=data.get('location', ''),
            salary_min = data.get('salary_min'),
            salary_max = data.get('salary_max'),
            is_active = True,
            category = data.get('category')
        )
        try:
            db.session.add(new_vacancy)
            db.session.commit()
            return {'message': 'Вакансия создана'}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': 'Ошибка создания вакансии', 'error': str(e)}, 500

    @jwt_required()
    def delete(self):
        data = request.get_json()
        vacancy_id = data.get('id')
        user_id = int(get_jwt_identity())
        
        vacancy = Vacancy.query.get(vacancy_id)
        if not vacancy:
            return {'message': 'Вакансия не найдена'}, 404
            
        if vacancy.employer_id != user_id:
            return {'message': 'Вы не можете удалить чужую вакансию'}, 403

        vacancy.is_active = False
        try:
            db.session.commit()
            return {'message': 'Вакансия удалена (перемещена в архив)'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': 'Ошибка удаления', 'error': str(e)}, 500

api.add_resource(VacancyResource, '/api/vacancy', '/api/vacancy/<int:vacancy_id>')

class EventResource(Resource):
    def get(self, event_id=None):
        if event_id is None:
            now = datetime.utcnow()
            active_events = Event.query.filter(
                Event.is_active == True,
                Event.date >= now
            ).all()
            # active_events = Event.query.filter_by(is_active = True).all()
            result = []
            for e in active_events:
                organizer = User.query.get(e.organizer_id)
                result.append({
                    'id': e.id,
                    'title': e.title,
                    'date': str(e.date),
                    'location': e.location,
                    'description': e.description,
                    'category': e.category,
                    'organizer_name': f"{organizer.first_name} {organizer.last_name}" if organizer else "Неизвестен"
                })
            return {'events': result}, 200
        else:
            event = Event.query.filter_by(id=event_id, is_active=True).first()
            if not event:
                return {'message': 'Мероприятие не найдено или удалено'}, 404
        
            organizer = User.query.get(event.organizer_id)
            organizer_info = {
                'first_name': organizer.first_name if organizer else None,
                'last_name': organizer.last_name if organizer else None
            }

            return {
                'id': event.id,
                'title': event.title,
                'date': event.date.isoformat() if event.date else None,
                'location': event.location,
                'description': event.description,
                'requirements': event.requirements,
                'category': event.category,
                'organizer': organizer_info
            }, 200

    @jwt_required()
    def post(self):
        data = request.get_json()
        user_id = int(get_jwt_identity())

        required_fields = ['title', 'description', 'requirements', 'location', 'date', 'capacity', 'category']
        for field in required_fields:
            if not data.get(field):
                return {'message': f'Поле "{field}" обязательно'}, 400
        try:
            date_str = data['date']
            if date_str.endswith('Z'):
                event_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                event_date = event_date.replace(tzinfo=timezone.utc).astimezone().replace(tzinfo=None)
            else:
                event_date = datetime.fromisoformat(date_str)
        except ValueError as e:
            print("Ошибка парсинга даты:", e)
            return {'message': 'Неверный формат даты'}, 400  
        
        new_event = Event(
            organizer_id = user_id,
            title = data.get('title'),
            description = data.get('description'),
            requirements=data['requirements'], 
            location = data.get('location'),
            date = event_date,
            capacity=data['capacity'],  
            category=data['category'],  
            is_active = True
        )
        try:
            db.session.add(new_event)
            db.session.commit()
            return {'message': 'Мероприятие создано'}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': 'Ошибка создания мероприятия', 'error': str(e)}, 500

    @jwt_required()
    def delete(self):
        data = request.get_json()
        event_id = data.get('id')
        user_id = int(get_jwt_identity())
        
        event = Event.query.get(event_id)
        if not event:
            return {'message': 'Мероприятие не найдено'}, 404
            
        if event.organizer_id != user_id:
            return {'message': 'Вы не можете удалить чужое мероприятие'}, 403

        event.is_active = False
        try:
            db.session.commit()
            return {'message': 'Мероприятие удалено'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': 'Ошибка удаления', 'error': str(e)}, 500

api.add_resource(EventResource, '/api/event', '/api/event/<int:event_id>')

class ApplyVacancy(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        vacancy_id = data.get('vacancy_id')
        user_id = int(get_jwt_identity())

        applicant_profile = Applicant.query.get(user_id)
        if not applicant_profile or not applicant_profile.resume or not applicant_profile.education:
            return {
                'message': 'Чтобы откликнуться, необходимо заполнить «Резюме» и «Образование» в личном кабинете.'
            }, 400
        
        exists = Sign_vacancy.query.filter_by(applicant_id = user_id, vacancy_id = vacancy_id).first()
        if exists:
            return {'message': 'Вы уже откликнулись на эту вакансию'}, 409
            
        new_sign = Sign_vacancy(
            applicant_id = user_id,
            vacancy_id = vacancy_id,
            status = 'pending'
        )
        try:
            db.session.add(new_sign)
            vacancy = Vacancy.query.get(vacancy_id)
            applicant = User.query.get(user_id)

            # Создаём уведомление для работодателя
            notif = Notification(
                recipient_user_id=vacancy.employer_id,
                sender_user_id=user_id,
                title="Новый отклик на вакансию",
                message=f"Пользователь {applicant.first_name} {applicant.last_name} откликнулся на вакансию «{vacancy.title}»."
            )
            db.session.add(notif)
            db.session.commit()
            return {'message': 'Отклик отправлен работодателю'}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': 'Ошибка при отклике', 'error': str(e)}, 500

api.add_resource(ApplyVacancy, '/api/vacancy/apply')

class JoinEvent(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        event_id = data.get('event_id')
        user_id = int(get_jwt_identity())
        
        exists = Sign_appointment.query.filter_by(applicant_id = user_id, event_id = event_id).first()
        if exists:
            return {'message': 'Вы уже записаны на это мероприятие'}, 409
            
        new_sign = Sign_appointment(
            applicant_id=user_id,
            event_id = event_id,
            status = 'pending'
        )
        try:
            db.session.add(new_sign)
            event = Event.query.get(event_id)
            applicant = User.query.get(user_id)

            # Уведомление для организатора
            notif = Notification(
                recipient_user_id=event.organizer_id,
                sender_user_id=user_id,
                title="Новая запись на мероприятие",
                message=f"Пользователь {applicant.first_name} {applicant.last_name} записался на мероприятие «{event.title}»."
            )
            db.session.add(notif)
            db.session.commit()
            return {'message': 'Вы записались на мероприятие'}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': 'Ошибка записи', 'error': str(e)}, 500

api.add_resource(JoinEvent, '/api/event/join')

class EmployerDashboard(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        current_user = User.query.get(user_id)
        
        if current_user.role != 'employer':
            return {'message': 'Доступ запрещен'}, 403
            
        if not current_user.employer:
             return {'message': 'Профиль работодателя не заполнен'}, 404

        vacancies_data = []
        for vac in current_user.employer.vacancy:
            applicants = []
            for sign in vac.sign_vacancy:
                applicant_user = User.query.get(sign.applicant_id)
                applicants.append({
                    'sign_id': sign.id,
                    'applicant_name': f"{applicant_user.first_name} {applicant_user.last_name}",
                    'age': applicant_user.age,
                    'contact_phone': applicant_user.contact_phone,
                    'email': applicant_user.email,
                    'resume': applicant_user.applicant.resume if applicant_user.applicant else "Нет резюме",
                    'education': applicant_user.applicant.education if applicant_user.applicant else None,
                    'status': sign.status,
                    'date': str(sign.date)
                })
            
            vacancies_data.append({
                'vacancy_id': vac.id,
                'title': vac.title,
                'is_active': vac.is_active,
                'applicants': applicants
            })
            
        return {'my_vacancies': vacancies_data}, 200

    @jwt_required()
    def put(self):
        data = request.get_json()
        sign_id = data.get('sign_id')
        new_status = data.get('status') 
        user_id = int(get_jwt_identity())
        
        sign = Sign_vacancy.query.get(sign_id)
        if not sign:
            return {'message': 'Отклик не найден'}, 404
            
        if sign.vacancy.employer_id != user_id:
            return {'message': 'Это не ваш отклик'}, 403
            
        sign.status = new_status
        # Получаем соискателя
        applicant = User.query.get(sign.applicant_id)
        vacancy = sign.vacancy

        # Определяем текст статуса
        status_labels = {
            'pending': 'в ожидании',
            'accepted': 'подтверждён',
            'rejected': 'отклонён'
        }
        status_text = status_labels.get(new_status, new_status)

        # Уведомление для соискателя
        notif = Notification(
            recipient_user_id=sign.applicant_id,
            sender_user_id=user_id,
            title="Изменён статус отклика",
            message=f"Ваш отклик на вакансию «{vacancy.title}» теперь {status_text}."
        )
        db.session.add(notif)
        try:
            db.session.commit()
            return {'message': f'Статус изменен на {new_status}'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': 'Ошибка обновления статуса', 'error': str(e)}, 500

api.add_resource(EmployerDashboard, '/api/employer/dashboard')

class ApplicantDashboard(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        current_user = User.query.get(user_id)
        
        my_applications = []
        for sign in current_user.sign_vacancy:
            vacancy = sign.vacancy
            employer_website = None
            if sign.status == 'accepted' and vacancy.employer:
                employer_website = vacancy.employer.contact_website

            my_applications.append({
                'vacancy_title': vacancy.title,
                'company': vacancy.employer.company_name if vacancy.employer else "Не указана",
                'my_status': sign.status,
                'vacancy_state': "Активна" if vacancy.is_active else "Вакансия удалена",
                'employer_website': employer_website,
            })
                    
        my_events = []
        for sign in current_user.sign_appointment:
            event_obj = Event.query.get(sign.event_id)
            event_state = "Активно" if event_obj.is_active else "Отменено"
            my_events.append({
                'sign_id': sign.id,
                'event_title': event_obj.title,
                'event_date': event_obj.date.isoformat() if event_obj.date else None,
                'location': event_obj.location,
                'my_status': sign.status,  # pending / confirmed / rejected
                'event_state': "Активно" if event_obj.is_active else "Отменено"
            })
            
        return {'applications': my_applications, 'events': my_events}, 200

api.add_resource(ApplicantDashboard, '/api/applicant/dashboard')

class OrganizerDashboard(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        current_user = User.query.get(user_id)

        if current_user.role != 'organizer':
            return {'message': 'Доступ запрещён'}, 403

        events = Event.query.filter_by(organizer_id=user_id).all()

        result = []
        for event in events:
            applicants = []
            for sign in event.sign_appointment:
                applicant = User.query.get(sign.applicant_id)
                applicants.append({
                    'sign_id': sign.id,
                    'applicant_name': f"{applicant.first_name} {applicant.last_name}" if applicant else "Удалён",
                    'contact_phone': applicant.contact_phone if applicant else None,
                    'email': applicant.email if applicant else None,
                    'status': sign.status,
                    'date_applied': sign.date.isoformat() if sign.date else None
                })

            result.append({
                'event_id': event.id,
                'event_title': event.title,
                'applicants': applicants
            })

        return {'my_events': result}, 200

    @jwt_required()
    def put(self):
        data = request.get_json()
        sign_id = data.get('sign_id')
        new_status = data.get('status')

        if new_status not in ['pending', 'confirmed', 'rejected']:
            return {'message': 'Недопустимый статус'}, 400

        user_id = int(get_jwt_identity())

        sign = Sign_appointment.query.get(sign_id)
        if not sign:
            return {'message': 'Заявка не найдена'}, 404
        
        event = Event.query.get(sign.event_id)
        if not event or event.organizer_id != user_id:
            return {'message': 'Это не ваше мероприятие'}, 403

        sign.status = new_status
        applicant = User.query.get(sign.applicant_id)
        event = sign.event

        status_labels = {
            'pending': 'в ожидании',
            'confirmed': 'подтверждена',
            'rejected': 'отклонена'
        }
        status_text = status_labels.get(new_status, new_status)

        notif = Notification(
            recipient_user_id=sign.applicant_id,
            sender_user_id=user_id,
            title="Изменён статус заявки на мероприятие",
            message=f"Ваша заявка на мероприятие «{event.title}» теперь {status_text}."
        )
        db.session.add(notif)
        try:
            db.session.commit()
            return {'message': f'Статус изменён на "{new_status}"'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': 'Ошибка обновления статуса', 'error': str(e)}, 500

api.add_resource(OrganizerDashboard, '/api/organizer/dashboard')

class CommentResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        user_id = int(get_jwt_identity())
        text = data.get('text')
        
        if 'vacancy_id' in data:
            new_comment = Comment_vacancy(user_id = user_id, vacancy_id = data['vacancy_id'], text = text)
        elif 'event_id' in data:
            new_comment = Comment_event(user_id = user_id, event_id = data['event_id'], text = text)
        else:
            return {'message': 'Не указан ID вакансии или мероприятия'}, 400
            
        try:
            db.session.add(new_comment)
            db.session.commit()
            return {'message': 'Комментарий добавлен'}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': 'Ошибка добавления комментария', 'error': str(e)}, 500

    @jwt_required()
    def delete(self):
        data = request.get_json()
        comment_id = data.get('id')
        type_comment = data.get('type') 
        user_id = int(get_jwt_identity())
        
        if type_comment == 'vacancy':
            comment = Comment_vacancy.query.get(comment_id)
        elif type_comment == 'event':
            comment = Comment_event.query.get(comment_id)
        else:
            return {'message': 'Неверный тип комментария'}, 400
            
        if not comment:
            return {'message': 'Комментарий не найден'}, 404
            
        if comment.user_id != user_id:
            return {'message': 'Вы можете удалять только свои комментарии'}, 403
            
        try:
            db.session.delete(comment)
            db.session.commit()
            return {'message': 'Комментарий удален'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': 'Ошибка удаления', 'error': str(e)}, 500
        
    def get(self):
        vacancy_id = request.args.get('vacancy_id', type=int)
        event_id = request.args.get('event_id', type=int)

        if not vacancy_id and not event_id:
            return {'message': 'Укажите vacancy_id или event_id'}, 400

        comments = []
        if vacancy_id:
            comments = Comment_vacancy.query.filter_by(vacancy_id=vacancy_id).all()
            result = []
            for c in comments:
                user = User.query.get(c.user_id) if c.user_id else None
                result.append({
                    'id': c.id,
                    'text': c.text,
                    'date': c.date.isoformat() if c.date else None,
                    'user_id': c.user_id,
                    'author_name': f"{user.first_name} {user.last_name}" if user else "Аноним"
                })
            return {'comments': result}, 200

        elif event_id:
            comments = Comment_event.query.filter_by(event_id=event_id).all()
            result = []
            for c in comments:
                user = User.query.get(c.user_id) if c.user_id else None
                result.append({
                    'id': c.id,
                    'text': c.text,
                    'date': c.date.isoformat() if c.date else None,
                    'user_id': c.user_id,
                    'author_name': f"{user.first_name} {user.last_name}" if user else "Аноним"
                })
            return {'comments': result}, 200

api.add_resource(CommentResource, '/api/comment')

class NotificationsResource(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        notifications = Notification.query.filter_by(recipient_user_id=user_id)\
                                         .order_by(Notification.date.desc())\
                                         .limit(20).all()
        result = []
        for n in notifications:
            sender = User.query.get(n.sender_user_id) if n.sender_user_id else None
            result.append({
                'id': n.id,
                'title': n.title,
                'message': n.message,
                'date': n.date.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'is_read': n.is_read,
                'sender_name': f"{sender.first_name} {sender.last_name}" if sender else "Система"
            })
        return {'notifications': result}, 200

    @jwt_required()
    def post(self):
        user_id = int(get_jwt_identity())
        unread = Notification.query.filter_by(
            recipient_user_id=user_id,
            is_read=False
        ).all()
        for n in unread:
            n.is_read = True
        try:
            db.session.commit()
            return {'message': f'Отмечено {len(unread)} уведомлений как прочитанных'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': 'Ошибка при обновлении уведомлений', 'error': str(e)}, 500
api.add_resource(NotificationsResource, '/api/notifications')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)