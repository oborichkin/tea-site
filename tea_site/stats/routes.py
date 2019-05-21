from flask import Blueprint, render_template, url_for
from flask_login import login_required, current_user

from tea_site.models import Answer

stats = Blueprint("stats", __name__)


@stats.route("/account")
@login_required
def account():
    need_review = current_user.get_need_review()
    img_file = url_for("static", filename="images/profile_pics/" + current_user.image)
    return render_template("account.html", img_file=img_file, need_review=need_review)
