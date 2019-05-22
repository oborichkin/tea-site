from flask_wtf import FlaskForm
from wtforms import (
    FormField,
    TextField,
    StringField,
    SelectField,
    PasswordField,
    SubmitField,
    BooleanField,
    FloatField,
    HiddenField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
    NumberRange,
)
from flask_login import current_user

from tea_site.models import Test, Category


class CreateCategoryForm(FlaskForm):
    name = StringField("Название категории", validators=[DataRequired()])
    desc = TextField("Описание", validators=[DataRequired()])
    submit = SubmitField("Создать")

    def validate_name(self, name):
        cat = Category.query.filter_by(name=name.data).first()
        if cat:
            raise ValidationError("Категория с таким именем уже существует")


class GradeAnswerForm(FlaskForm):
    grade = FloatField(validators=[DataRequired(), NumberRange(min=0, max=1)])
    submit = SubmitField("Оценить")


class FlagAnswerForm(FlaskForm):
    submit = SubmitField("Подать аппеляцию")


class ApproveAnswer(FlaskForm):
    submit = SubmitField("Подтвердить оценку")


class CreateTestForm(FlaskForm):
    name = StringField("Название теста", validators=[DataRequired()])
    cat_id = SelectField("Категория", coerce=int)
    submit = SubmitField("Создать")


class CreateQuestion(FlaskForm):
    question_text = TextField("Вопрос", validators=[DataRequired()])
    answer_text = TextField("Правильный ответ", validators=[DataRequired()])
    submit = SubmitField("Добавить вопрос")


class SubmitTestForm(FlaskForm):
    submit = SubmitField("Создать тест")


class QuestionForm(FlaskForm):
    answer_text = TextField("Ваш ответ", validators=[DataRequired()])


class TestForm(FlaskForm):
    submit = SubmitField("Отправить ответ")

