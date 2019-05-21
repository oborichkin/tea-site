from flask import Blueprint, render_template, url_for
from flask_login import login_required, current_user

from tea_site.models import Answer, TestResult

stats = Blueprint("stats", __name__)


@stats.route("/account")
@login_required
def account():
    need_review = current_user.get_need_review(5)
    last_results = current_user.results.order_by(TestResult.date).limit(5).all()
    img_file = url_for("static", filename="images/profile_pics/" + current_user.image)
    return render_template(
        "account.html",
        img_file=img_file,
        need_review=need_review,
        last_results=last_results,
    )


@stats.route("/results")
@login_required
def get_all_results():
    # TODO: Добавить пагинацию
    results = TestResult.query.filter_by(author=current_user).all()
    return render_template("results.html", results=results, title="Результаты")


@stats.route("/review")
@login_required
def review():
    # TODO: Добавить пагинацию
    results = current_user.get_need_review()
    return render_template("results.html", results=results, title="Ревью")
