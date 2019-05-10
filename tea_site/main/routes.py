from flask import Blueprint
from tea_site import db

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    return "Hello world!"

@main.route("/about")
def about():
    return "About page"