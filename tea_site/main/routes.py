from flask import Blueprint, render_template

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    return render_template("index.html")


@main.route("/about")
def about():
    return "About page"
