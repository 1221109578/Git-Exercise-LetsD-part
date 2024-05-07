from flask import Blueprint, render_template, request, flash, redirect ,url_for
from flask_login import login_required, current_user
from . import db

views = Blueprint('views', __name__)

@views.route("/", methods=['GET', 'POST'])
def home():
    return render_template('Home.html', user=current_user)

@views.route('/myaccount', methods=['GET','POST'])
@login_required
def myaccount():
    #Retrive User's informations
    username = current_user.username
    email   = current_user.email
    full_name = current_user.full_name
    return render_template('myaccount.html', user=current_user, username=username, email=email,
                             full_name=full_name)

@views.route("/package")
def package():
    return render_template('package.html', user=current_user)

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
@login_required
def Iceland():
    return render_template('Iceland.html')

@views.route("/United-Kingdom")
@login_required
def United_Kingdom():
    return render_template('United Kingdom.html')

@views.route("/Switzerland")
@login_required
def Switzerland():
    return render_template('Switzerland.html')

@views.route("/Turkey")
@login_required
def Turkey():
    return render_template('Turkey.html')

@views.route("/Germany")
@login_required
def Germany():
    return render_template('Germany.html')
