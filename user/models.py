from init import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app
from datetime import *


# Permission Constants
class Permission:
    # Can follow other users
    FOLLOW = 0x01
    # Can comment other articles
    COMMENT = 0x02
    # Can post articles
    POST_ARTICLE = 0x04
    # Can manage others' comments
    MODIFY_COMMENT = 0x08
    # Admin
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW | Permission.COMMENT | Permission.POST_ARTICLE, True),
            'Moderator': (Permission.FOLLOW | Permission.COMMENT |
                         Permission.POST_ARTICLE | Permission.MODIFY_COMMENT, False),
            'Admin': (0xff, False)
        }

        for role in roles:
            r = Role.query.filter_by(name=role).first()
            if r is None:
                r = Role()
            # Be able to modify permissions
            r.name = role
            r.default = roles.get(role)[1]
            r.permissions = roles.get(role)[0]
            db.session.add(r)
        db.session.commit()


class User(UserMixin, db.Model):
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config.get('ADMIN_EMAIL'):
                self.role = Role.query.filter_by(name='Admin').first()
            else:
                self.role = Role.query.filter_by(name='User').first()

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    #Profile info
    fullname = db.Column(db.String(64))
    location = db.Column(db.String(64))
    desc = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_visit = db.Column(db.DateTime(), default=datetime.utcnow)

    #Article
    posts = db.relationship('Post', backref='author', lazy='dynamic')


    @property
    def password(self):
        raise AttributeError('password is not readable property')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password=password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    #Check permissions
    def check_permission(self, permission):
        if self.role is not None:
            return (self.role.permissions & permission) == permission
        return False

    def check_admin(self):
        return self.check_permission(Permission.ADMINISTER)

    # Update vist time
    def ping(self):
        self.last_visit = datetime.utcnow()
        db.session.add(self)
        db.session.commit()


    # Generate fake records, Only for test!!
    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     username=forgery_py.internet.user_name(True),
                     password=forgery_py.lorem_ipsum.word(),
                     fullname=forgery_py.name.full_name(),
                     location=forgery_py.address.city(),
                     desc=forgery_py.lorem_ipsum.sentence(),
                     member_since=forgery_py.date.date(True))
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()


class AnonymousUser(AnonymousUserMixin):
    # Check permissions
    def check_permission(self, permission):
        return False

    def check_admin(self):
        return False
