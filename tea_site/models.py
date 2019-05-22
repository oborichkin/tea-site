from datetime import datetime

from tea_site import db, login_manager
from flask import current_app, url_for
from datetime import datetime
from flask_login import UserMixin


test_to_questions = db.Table(
    "test_to_questions",
    db.Model.metadata,
    db.Column("test_id", db.Integer, db.ForeignKey("test.id")),
    db.Column("q_id", db.Integer, db.ForeignKey("question.id")),
)

# TODO: Поревьювить модельки снова, расставить nullable и каскадинг


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(60), nullable=False)
    middle_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60), nullable=False)
    university = db.Column(db.String(120))
    group_id = db.Column(db.String(36))
    password = db.Column(db.String(128), nullable=False)
    image = db.Column(db.String(20), nullable=False, default="default.png")

    answers = db.relationship("Answer", backref="author", lazy=True)
    questions = db.relationship("Question", backref="author", lazy=True)
    tests = db.relationship("Test", backref="author", lazy="dynamic")
    results = db.relationship("TestResult", backref="author", lazy="dynamic")

    def get_need_review(self, limit=None):
        need_review = set()
        for q in self.questions:
            for a in q.answers.filter_by(flagged=True).limit(limit).all():
                need_review.add(a.result)
        return need_review

    def get_user_score(self):
        # TODO: Переписать на запрос
        score = 0
        for a in self.answers:
            if a.grade:
                score += a.grade
        return score

    def __repr__(self):
        return f"User({self.first_name} {self.middle_name} {self.last_name})"


class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    text = db.Column(db.Text, nullable=False)

    tests = db.relationship("Test", secondary=test_to_questions, backref="questions")
    answers = db.relationship("Answer", backref="question", lazy="dynamic")

    def __repr__(self):
        return f"Question ({self.id})"


def get_random_image():
    # TODO: Смотреть в директории стандартных картинок
    import random

    return str(random.randint(1, 5)) + ".jpg"


# TODO: Add images and description to categories
class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(20), nullable=False, default=get_random_image)

    tests = db.relationship("Test", backref="category", lazy=True)

    def get_image_path(self):
        return url_for("static", filename="images/categories/" + self.image)

    def __repr__(self):
        return f"Category ({self.name})"


class Test(db.Model):
    __tablename__ = "test"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    cat_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    draft = db.Column(db.Boolean, default=True, nullable=False)

    results = db.relationship("TestResult", backref="test", lazy=True)

    def __repr__(self):
        return f"Test ({self.id})"


class Answer(db.Model):
    __tablename__ = "answer"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    q_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    res_id = db.Column(db.Integer, db.ForeignKey("test_result.id"))
    text = db.Column(db.Text)
    grade = db.Column(db.Float)
    flagged = db.Column(db.Boolean, default=False)
    reviewed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Answer ({self.id})"


from enum import Enum


class Status(Enum):
    GRADED = 1
    AWAITS = 2
    REVIEW = 3


class TestResult(db.Model):
    __tablename__ = "test_result"
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey("test.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    answers = db.relationship("Answer", backref="result", lazy=True)

    def get_status(self):
        for a in self.answers:
            if a.grade == None:
                return 2
        for a in self.answers:
            if a.flagged:
                return 3
        return 1

    def get_score(self):
        return sum([a.grade if a.grade else 0 for a in self.answers])

    def __repr__(self):
        return f"Test Result ({self.id})"
