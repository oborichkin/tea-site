from tea_site import db, login_manager
from flask import current_app
from datetime import datetime
from flask_login import UserMixin


test_to_questions = db.Table('test_to_questions', db.Model.metadata,
    db.Column('test_id', db.Integer, db.ForeignKey('test.id')),
    db.Column('q_id', db.Integer, db.ForeignKey('question.id'))
)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(60), nullable=False)
    middle_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60), nullable=False)
    university = db.Column(db.String(120))
    group_id = db.Column(db.String(36))
    password = db.Column(db.String(128), nullable=False)

    answers = db.relationship('Answer', backref='author', lazy=True)
    questions = db.relationship('Question', backref='author', lazy=True)
    tests = db.relationship('Test', backref='author', lazy=True)
    results = db.relationship('TestResult', backref='author', lazy=True)

    def __repr__(self):
        return f"User({self.first_name} {self.middle_name} {self.last_name})"


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)

    tests = db.relationship('Test', secondary=test_to_questions, backref='questions')
    answers = db.relationship('Answer', backref='question')

    def __repr__(self):
        return f"Question ({self.id})"


# TODO: Add images and description to categories
class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)

    tests = db.relationship('Test', backref='category', lazy=True)

    def __repr__(self):
        return f"Category ({self.name})"


class Test(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cat_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    draft = db.Column(db.Boolean, default=True, nullable=False)

    results = db.relationship('TestResult', backref='test', lazy=True)

    def __repr__(self):
        return f"Test ({self.id})"


class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    q_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    text = db.Column(db.Text)
    grade = db.Column(db.Float)
    flagged = db.Column(db.Boolean, default=False)
    reviewed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Answer ({self.id})"

class TestResult(db.Model):
    __tablename__ = 'test_result'
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Test Result ({self.id})"
