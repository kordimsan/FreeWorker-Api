from run import db
from passlib.hash import pbkdf2_sha256 as sha256
import datetime

class UserModel(db.Model):
    __tablename__ = 't_users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(120), nullable = False)
    
    email = db.Column(db.String(255), unique=True)
    registered_on = db.Column(db.DateTime,default=datetime.datetime.utcnow)
    admin = db.Column(db.Boolean, nullable=False,default=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(50))
    latitude = db.Column(db.String(50))
    longitude = db.Column(db.String(50))
    area = db.Column(db.Integer, default=30)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()
    
    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'user_id': x.user_id,
                'username': x.username,
                'password': x.password,
                'email': x.email,
                'admin': x.admin,
                'first_name': x.first_name,
                'last_name': x.last_name,
                'phone_number': x.phone_number,
                'latitude': x.latitude,
                'longitude': x.longitude,
                'area': x.area,
            }
        return {'users': list(map(lambda x: to_json(x), cls.query.all()))}

    @classmethod
    def del_by_username(cls, username):
        try:
            num_rows_deleted = db.session.query(cls).filter(cls.username == username).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)
    
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))
    
    def add(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)



class Wizard(db.Model):
    __tablename__ = 't_wizard'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idp = db.Column(db.Integer)
    wizard_name = db.Column(db.String(150))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class Skills(db.Model):
    __tablename__ = 'd_skills'

    id = db.Column(db.Integer, primary_key=True)
    wizard_id = db.Column(db.Integer, db.ForeignKey('t_wizard.id'))
    skill_name = db.Column(db.String(150))
    key_words = db.Column(db.Text)
   
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class UsedSkills(db.Model):
    __tablename__ = 't_used_skills'
    
    id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('d_skills.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('t_users.user_id'))
    used = db.Column(db.Integer, default=1)
   
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class WorkersFeedback(db.Model):
    __tablename__ = 't_workers_feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('t_users.user_id'))
    voter_id = db.Column(db.Integer, db.ForeignKey('t_users.user_id'))
    rank = db.Column(db.Integer)
    text = db.Column(db.Text)
   
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()
    
    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'user_id': x.user_id,
                'username': x.username,
                'password': x.password,
                'email': x.email,
                'admin': x.admin,
                'first_name': x.first_name,
                'last_name': x.last_name,
                'phone_number': x.phone_number,
                'latitude': x.latitude,
                'longitude': x.longitude,
                'area': x.area,
            }
        return {'users': list(map(lambda x: to_json(x), cls.query.all()))}

# user = UserModel(
#             username='test',
#             password='test'
#         )
# db.session.add(user)
# db.session.commit()