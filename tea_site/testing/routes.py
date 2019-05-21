from flask import Blueprint, render_template, abort, flash, redirect, url_for, request
from flask_login import login_required, current_user

from tea_site import db
from tea_site.tasks import eval_answer
from tea_site.models import Category, Test, Question, Answer, TestResult
from tea_site.testing.forms import (
    CreateQuestion,
    CreateTestForm,
    CreateCategoryForm,
    TestForm,
    SubmitTestForm,
    GradeAnswerForm,
    FlagAnswerForm,
)

testing = Blueprint("testing", __name__)

# TODO: Категории создают и удаляют только админы


@testing.route("/categories")
def categories():
    categories = Category.query.all()
    return render_template("categories.html", categories=categories)


@testing.route("/category/new", methods=["POST", "GET"])
@login_required
def new_category():
    form = CreateCategoryForm()
    if form.validate_on_submit():
        cat = Category(name=form.name.data)
        db.session.add(cat)
        db.session.commit()
        flash(f"Категория успешно создана", "success")
        return redirect(url_for("testing.categories"))
    return render_template("create_category.html", form=form)


@testing.route("/category/<int:cat_id>/delete", methods=["POST"])
@login_required
def delete_category(cat_id):
    Category.query.get_or_404(id=cat_id).delete()
    db.session.commit()
    flash("Category successfully deleted", "alert alert-success")
    return redirect(url_for("categories"))


@testing.route("/tests")
@login_required
def all_tests():
    tests = Test.query.filter_by(draft=False).all()
    return render_template("tests.html", tests=tests)


@testing.route("/tests/<int:category_id>")
@login_required
def category_tests(category_id):
    tests = Test.query.filter_by(cat_id=category_id, draft=False).all()
    if not tests:
        # TODO: Add to template message that there is no tests yet
        # TODO: Add link to template like 'You can be the first to add'
        abort(404)
    return render_template("tests.html", tests=tests)


# TODO: Тесты создают учителя и админы


@testing.route("/test/new", methods=["GET", "POST"])
@login_required
def create_test():
    form = CreateTestForm()
    form.cat_id.choices = [(c.id, c.name) for c in Category.query.all()]
    if form.validate_on_submit():
        test = Test(
            name=form.name.data,
            author=current_user,
            cat_id=form.cat_id.data,
            draft=True,
        )
        db.session.add(test)
        db.session.commit()
        return redirect(url_for("testing.all_tests"))
    return render_template("create_test.html", form=form)


@testing.route("/test/<int:test_id>/update", methods=["GET", "POST"])
@login_required
def update_test(test_id):
    form = SubmitTestForm()
    test = Test.query.get_or_404(test_id)
    if test.author != current_user or not test.draft:
        abort(403)
    # TODO: Вынести валидацию в форму
    if form.validate_on_submit():
        if len(test.questions) == 0:
            flash("Добавьте как минимум один вопрос", "alert alert-danger")
            return redirect(url_for("testing.update_test", test_id=test_id))
        test.draft = False
        db.session.commit()
        return redirect(url_for("testing.all_tests"))
    return render_template("update_test.html", test=test, form=form)


@testing.route("/test/<int:test_id>/add", methods=["GET", "POST"])
@login_required
def test_add_question(test_id):
    form = CreateQuestion()
    test = Test.query.get_or_404(test_id)
    if test.author != current_user:
        abort(403)
    if form.validate_on_submit():
        question = Question(author=current_user, text=form.question_text.data)
        answer = Answer(
            author=current_user,
            question=question,
            text=form.answer_text.data,
            grade=1,
            reviewed=True,
        )
        db.session.add(question)
        db.session.add(answer)
        test.questions.append(question)
        db.session.commit()
        return redirect(url_for("testing.update_test", test_id=test_id))
    return render_template("add_question.html", test=test, form=form)


@testing.route("/test/<int:test_id>/delete")
@login_required
def delete_test(test_id):
    test = Test.query.get_or_404(id=test_id)
    if test.author != current_user:
        abort(403)
    test.delete()
    db.session.commit()
    flash("Test successfully deleted", "alert alert-success")
    # TODO: Redirect somewhere else
    return redirect(url_for("main.home"))


@testing.route("/test/<int:test_id>", methods=["GET", "POST"])
@login_required
def take_test(test_id):
    test = Test.query.get_or_404(test_id)
    form = TestForm()
    if form.validate_on_submit():
        result = TestResult(test_id=test_id, author=current_user)
        db.session.add(result)
        for q in test.questions:
            text = request.values.get(str(q.id))
            answer = Answer(author=current_user, text=text, question=q, result=result)
            db.session.add(answer)
        db.session.commit()
        for a in result.answers:
            eval_answer.delay(a.id)
        return redirect(url_for("testing.overview_result", result_id=result.id))
    return render_template("test.html", test=test, form=form)


@testing.route("/result/<int:result_id>/overview")
@login_required
def overview_result(result_id):
    from collections import defaultdict

    result = TestResult.query.get_or_404(result_id)
    grade_forms = defaultdict()
    appeal_forms = defaultdict()
    for a in result.answers:
        grade_forms[a.id] = GradeAnswerForm()
        appeal_forms[a.id] = FlagAnswerForm()
    if (result.author != current_user) and (result.test.author != current_user):
        abort(403)
    return render_template(
        "result.html", result=result, grade_forms=grade_forms, appeal_forms=appeal_forms
    )


@testing.route("/answer/<int:answer_id>/grade", methods=["POST"])
@login_required
def grade_answer(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if answer.result.test.author != current_user:
        abort(403)
    grade = float(request.values.get("grade"))
    if not 0 <= grade <= 1:
        flash(
            "Оценка должна быть в пределах от 0.0 до 1.0 " + str(grade),
            "alert alert-danger",
        )
        return redirect(url_for("testing.overview_result", result_id=answer.result.id))
    answer.grade = grade
    answer.flagged = False
    answer.reviewed = True
    db.session.commit()
    return redirect(url_for("testing.overview_result", result_id=answer.result.id))


@testing.route("/answer/<int:answer_id>/flag", methods=["POST"])
@login_required
def flag_answer(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if answer.author != current_user:
        abort(403)
    answer.flagged = True
    db.session.commit()
    return redirect(url_for("testing.overview_result", result_id=answer.result.id))
