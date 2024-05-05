from flask import Blueprint,render_template

views = Blueprint(__name__, "views")

@views.route("/")
def home():
    return render_template("Home.html")

@views.route("/package")
def package():
    return render_template("package.html")

@views.route("/login")
def login():
    return render_template("login.html")
