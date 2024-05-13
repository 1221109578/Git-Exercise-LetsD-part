from flask import Blueprint, render_template, request, flash, redirect ,url_for
from flask_login import login_required, current_user
from .__init__ import create_app
from .models import PaymentMethod

views = Blueprint('views', __name__)

months = [
    {'value': '01', 'label': '01 - January'},
    {'value': '02', 'label': '02 - February'},
    {'value': '03', 'label': '03 - March'},
    {'value': '04', 'label': '04 - April'},
    {'value': '05', 'label': '05 - May'},
    {'value': '06', 'label': '06 - June'},
    {'value': '07', 'label': '07 - July'},
    {'value': '08', 'label': '08 - August'},
    {'value': '09', 'label': '09 - September'},
    {'value': '10', 'label': '10 - October'},
    {'value': '11', 'label': '11 - November'},
    {'value': '12', 'label': '12 - December'},

]

years = [
    {'value': '2023', 'label': '2023'},
    {'value': '2024', 'label': '2024'},
    {'value': '2025', 'label': '2025'},
    {'value': '2026', 'label': '2026'},
    {'value': '2027', 'label': '2027'},
    {'value': '2028', 'label': '2028'},
    {'value': '2029', 'label': '2029'},
    {'value': '2030', 'label': '2030'},
    {'value': '2031', 'label': '2031'},
    {'value': '2032', 'label': '2032'},
]


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
    phone_number = current_user.phone_number
    payment_methods = PaymentMethod.query.filter_by(user_id=current_user.id).all()
    return render_template('myaccount.html',
                            user=current_user, 
                            username=username, 
                            email=email,
                            full_name=full_name, 
                            phone_number=phone_number, 
                            months=months, 
                            years=years,
                            payment_methods=payment_methods
                            )

@views.route("/package")
def package():
    return render_template('package.html', user=current_user)

@views.route("/Booking")
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

@views.route("/United Kingdom")
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
