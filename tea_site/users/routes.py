from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user, logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash

from tea_site import db
from tea_site.models import User
from tea_site.users.forms import RegistrationForm, LoginForm

users = Blueprint('users', __name__)


@login_required
@users.route("/account")
def account():
    return render_template("account.html")


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash(f"Аккаунт был успешно создан", 'success')
        return redirect(url_for('users.login'))
    return render_template("register.html", title='Регистрация', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(f"Вход не удался, пожалуйста, проверьте email и пароль", 'danger')
    return render_template("login.html", title='Вход', form=form)


@login_required
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))