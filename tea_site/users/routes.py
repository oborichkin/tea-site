from flask import Blueprint, render_template
from flask_login import login_required, current_user

users = Blueprint('users', __name__)


@login_required
@users.route("/account")
def account():
    return render_template("account.html")


@users.route("/register")
def register():
    return render_template("register.html")


@users.route("/login")
def login():
    return render_template("login.html")


@login_required
@users.route("/logout")
def logout():
    pass