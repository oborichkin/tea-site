from flask_wtf import FlaskForm
from wtforms import FormField, TextField, StringField, SelectField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user

from tea_site.models import Test


class CreateCategoryForm(FlaskForm):
    name = StringField('Название категории', validators=[DataRequired()])
    submit = SubmitField('Создать')
    # TODO: Name is unique, add validator


class CreateTestForm(FlaskForm):
    name = StringField('Название теста', validators=[DataRequired()])
    cat_id = SelectField('Категория', coerce=int)
    submit = SubmitField('Создать')


class CreateQuestion(FlaskForm):
    question_text = TextField('Вопрос', validators=[DataRequired()])
    answer_text = TextField('Правильный ответ', validators=[DataRequired()])
    submit = SubmitField('Добавить вопрос')


class SubmitTestForm(FlaskForm):
    submit = SubmitField('Создать тест')


class QuestionForm(FlaskForm):
    answer_text = TextField('Ваш ответ', validators=[DataRequired()])


class TestForm(FlaskForm):
    submit = SubmitField('Отправить ответ')