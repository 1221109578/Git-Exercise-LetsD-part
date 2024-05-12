from flask import Blueprint, render_template, request, flash, redirect ,url_for
from flask_login import login_required, current_user
from .__init__ import create_app

views = Blueprint('views', __name__)

@views.route("/", methods=['GET', 'POST'])
def home():
    return render_template('Home.html')

@views.route('/myaccount', methods=['GET','POST'])
@login_required
def myaccount():
    return render_template('myaccount.html')

@views.route("/package")
def package():
    return render_template('package.html')

@views.route("/history")
def Booking():
    return render_template('Booking.html')

@views.route("/cart")
def cart():
    return render_template("cart.html")

@views.route("/chat")
def chat():
    return render_template("chat.html")

@views.route("/Iceland")
def Iceland():
    return render_template('Iceland.html')

@views.route("/United Kingdom")
def United_Kingdom():
    return render_template('United Kingdom.html')

@views.route("/Switzerland")
def Switzerland():
    return render_template('Switzerland.html')

@views.route("/Turkey")
def Turkey():
    return render_template('Turkey.html')

@views.route("/Germany")
def Germany():
    return render_template('Germany.html')

@views.route("/winter")
def Winter():
    return render_template('winter.html')

@views.route("/summer")
def Summer():
    return render_template('summer.html')

@views.route("/spring")
def Spring():
    return render_template('spring.html')

@views.route("/autumn")
def Autumn():
    return render_template('autumn.html')
