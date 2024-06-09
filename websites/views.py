from flask import Blueprint, render_template, request, flash, redirect ,url_for
from flask_login import login_required, current_user
from . import create_app
from .models import PaymentMethod, Seasons, Package
from . import db

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

#-----

@views.route('/winter', methods=['GET'])
def winter():
    # Retrieve all events from the Seasons table
    main_events = Seasons.query.all()
    return render_template('winter.html', 
                           user=current_user, 
                           events=main_events,
                           event_id = 1)

@views.route('/summer', methods=['GET'])
def summer():
    # Retrieve all events from the Seasons table
    main_events = Seasons.query.all()
    return render_template('summer.html', 
                           user=current_user, 
                           events=main_events,
                           event_id = 2
                           )

@views.route('/spring', methods=['GET'])
def spring():
    # Retrieve all events from the Seasons table
    main_events = Seasons.query.all()
    return render_template('spring.html', 
                           user=current_user, 
                           events=main_events,
                           event_id=3,
                           )

@views.route('/autumn', methods=['GET'])
def autumn():
    # Retrieve all events from the Seasons table
    main_events = Seasons.query.all()
    return render_template('autumn.html', 
                           user=current_user, 
                           events=main_events,
                           event_id=4)

@views.route("/package")
def package():
    return render_template('package.html', user=current_user)

@views.route("/Booking", methods=['GET','POST'])
@login_required
def Booking():
    if request.method =='POST':
        package_id = request.form [package_id]
        package = Package.query.get(package_id)
        booking = booking()
        booking.user_id = current_user.id 
        booking.package_id = package_id
        booking.package_name = package.name
        booking.price = package.price
        db.session.add(booking)
        db.session.commit()
        
        flash('Booking Successful' , 'success')
        #return redirect(url_for('views.booking_confirmation'))

        booking_items = Package.query.all()     
        return render_template('Booking.html', user=current_user, booking_items=booking_items)
    else:
        booking_items = Package.query.all()
        return render_template('Booking.html', user=current_user, booking_items=booking_items)

@views.route("/chat")
@login_required
def chat():
    return render_template("chat.html", user=current_user)

@views.route("/Iceland", methods=["GET"])
@login_required
def Iceland():
    if request.method == "POST":
        selected_activities = request.form.getlist('activities')
        Num_of_pax = int(request.form['No. of Pax'])
        price_flight = db.session.query(Package.price_flight).first()[0]
        price_lodge = db.session.query(Package.price_lodge).first()[0]
        price_activity_1 = db.session.query(Package.price_activity_1).first()[0]
        price_activity_2 = db.session.query(Package.price_activity_2).first()[0]
        price_activity_3 = db.session.query(Package.price_activity_3).first()[0]
        price_activity_4 = db.session.query(Package.price_activity_4).first()[0]
        price_activity_5 = db.session.query(Package.price_activity_5).first()[0]

        #Calculate total activity cost
        total_activity_cost = 0
        if 'activity_1' in selected_activities:
            total_activity_cost += price_activity_1
        if 'activity_2' in selected_activities:
            total_activity_cost += price_activity_2
        if 'activity_3' in selected_activities:
            total_activity_cost += price_activity_3
        if 'activity_4' in selected_activities:
            total_activity_cost += price_activity_4
        if 'activity_5' in selected_activities:
            total_activity_cost += price_activity_5

            #total activity costs (without person)
            total_cost = total_activity_cost + price_flight + price_lodge

            total_cost_with_pax = total_cost * Num_of_pax

            return render_template('Booking.html', total_cost_with_persons=total_cost_with_pax)
        
    
    price_flight = db.session.query(Package.price_flight).first()
    price_lodge = db.session.query(Package.price_lodge).first()
    date_start = db.session.query(Package.date_start).first()
    date_end = db.session.query(Package.date_end).first()
    price_activity_1 = db.session.query(Package.price_activity_1).first()
    price_activity_2 = db.session.query(Package.price_activity_2).first()
    price_activity_3 = db.session.query(Package.price_activity_3).first()
    price_activity_4 = db.session.query(Package.price_activity_4).first()
    price_activity_5 = db.session.query(Package.price_activity_5).first()
    activity_1 = db.session.query(Package.activity_1).first()
    activity_2 = db.session.query(Package.activity_2).first()
    activity_3 = db.session.query(Package.activity_3).first()
    activity_4 = db.session.query(Package.activity_4).first()
    activity_5 = db.session.query(Package.activity_5).first()
    return render_template('Iceland.html',
                            user=current_user,
                            price_flight = price_flight,
                            price_lodge = price_lodge,
                            date_start = date_start,
                            date_end = date_end,
                            price_activity_1 = price_activity_1,
                            price_activity_2 = price_activity_2,
                            price_activity_3 = price_activity_3,
                            price_activity_4 = price_activity_4,
                            price_activity_5 = price_activity_5,
                            activity_1 = activity_1,
                            activity_2 = activity_2,
                            activity_3 = activity_3,
                            activity_4 = activity_4,
                            activity_5 = activity_5,
                            id=1)

@views.route("/United Kingdom")
@login_required
def United_Kingdom():
    price_flight = db.session.query(Package.price_flight).filter_by(id=2).first()
    price_lodge = db.session.query(Package.price_lodge).filter_by(id=2).first()
    date_start = db.session.query(Package.date_start).filter_by(id=2).first()
    date_end = db.session.query(Package.date_end).filter_by(id=2).first()
    price_activity_1 = db.session.query(Package.price_activity_1).filter_by(id=2).first()
    price_activity_2 = db.session.query(Package.price_activity_2).filter_by(id=2).first()
    price_activity_3 = db.session.query(Package.price_activity_3).filter_by(id=2).first()
    price_activity_4 = db.session.query(Package.price_activity_4).filter_by(id=2).first()
    price_activity_5 = db.session.query(Package.price_activity_5).filter_by(id=2).first()
    activity_1 = db.session.query(Package.activity_1).filter_by(id=2).first()
    activity_2 = db.session.query(Package.activity_2).filter_by(id=2).first()
    activity_3 = db.session.query(Package.activity_3).filter_by(id=2).first()
    activity_4 = db.session.query(Package.activity_4).filter_by(id=2).first()
    activity_5 = db.session.query(Package.activity_5).filter_by(id=2).first()
    return render_template('United Kingdom.html',
                            user=current_user,
                            price_flight = price_flight,
                            price_lodge = price_lodge,
                            date_start = date_start,
                            date_end = date_end,
                            price_activity_1 = price_activity_1,
                            price_activity_2 = price_activity_2,
                            price_activity_3 = price_activity_3,
                            price_activity_4 = price_activity_4,
                            price_activity_5 = price_activity_5,
                            activity_1 = activity_1,
                            activity_2 = activity_2,
                            activity_3 = activity_3,
                            activity_4 = activity_4,
                            activity_5 = activity_5,
                            id=2)

@views.route("/Switzerland")
@login_required
def Switzerland():
    price_flight = db.session.query(Package.price_flight).filter_by(id=3).first()
    price_lodge = db.session.query(Package.price_lodge).filter_by(id=3).first()
    date_start = db.session.query(Package.date_start).filter_by(id=3).first()
    date_end = db.session.query(Package.date_end).filter_by(id=3).first()
    price_activity_1 = db.session.query(Package.price_activity_1).filter_by(id=3).first()
    price_activity_2 = db.session.query(Package.price_activity_2).filter_by(id=3).first()
    price_activity_3 = db.session.query(Package.price_activity_3).filter_by(id=3).first()
    price_activity_4 = db.session.query(Package.price_activity_4).filter_by(id=3).first()
    price_activity_5 = db.session.query(Package.price_activity_5).filter_by(id=3).first()
    activity_1 = db.session.query(Package.activity_1).filter_by(id=3).first()
    activity_2 = db.session.query(Package.activity_2).filter_by(id=3).first()
    activity_3 = db.session.query(Package.activity_3).filter_by(id=3).first()
    activity_4 = db.session.query(Package.activity_4).filter_by(id=3).first()
    activity_5 = db.session.query(Package.activity_5).filter_by(id=3).first()
    return render_template('Switzerland.html',
                            user=current_user,
                            price_flight = price_flight,
                            price_lodge = price_lodge,
                            date_start = date_start,
                            date_end = date_end,
                            price_activity_1 = price_activity_1,
                            price_activity_2 = price_activity_2,
                            price_activity_3 = price_activity_3,
                            price_activity_4 = price_activity_4,
                            price_activity_5 = price_activity_5,
                            activity_1 = activity_1,
                            activity_2 = activity_2,
                            activity_3 = activity_3,
                            activity_4 = activity_4,
                            activity_5 = activity_5,
                            id=3)

@views.route("/Turkey")
@login_required
def Turkey():
    price_flight = db.session.query(Package.price_flight).filter_by(id=4).first()
    price_lodge = db.session.query(Package.price_lodge).filter_by(id=4).first()
    date_start = db.session.query(Package.date_start).filter_by(id=4).first()
    date_end = db.session.query(Package.date_end).filter_by(id=4).first()
    price_activity_1 = db.session.query(Package.price_activity_1).filter_by(id=4).first()
    price_activity_2 = db.session.query(Package.price_activity_2).filter_by(id=4).first()
    price_activity_3 = db.session.query(Package.price_activity_3).filter_by(id=4).first()
    price_activity_4 = db.session.query(Package.price_activity_4).filter_by(id=4).first()
    price_activity_5 = db.session.query(Package.price_activity_5).filter_by(id=4).first()
    activity_1 = db.session.query(Package.activity_1).filter_by(id=4).first()
    activity_2 = db.session.query(Package.activity_2).filter_by(id=4).first()
    activity_3 = db.session.query(Package.activity_3).filter_by(id=4).first()
    activity_4 = db.session.query(Package.activity_4).filter_by(id=4).first()
    activity_5 = db.session.query(Package.activity_5).filter_by(id=4).first()
    return render_template('Turkey.html',
                            user=current_user,
                            price_flight = price_flight,
                            price_lodge = price_lodge,
                            date_start = date_start,
                            date_end = date_end,
                            price_activity_1 = price_activity_1,
                            price_activity_2 = price_activity_2,
                            price_activity_3 = price_activity_3,
                            price_activity_4 = price_activity_4,
                            price_activity_5 = price_activity_5,
                            activity_1 = activity_1,
                            activity_2 = activity_2,
                            activity_3 = activity_3,
                            activity_4 = activity_4,
                            activity_5 = activity_5,
                            id=4)
@views.route("/Germany")
@login_required
def Germany():
    price_flight = db.session.query(Package.price_flight).filter_by(id=5).first()
    price_lodge = db.session.query(Package.price_lodge).filter_by(id=5).first()
    date_start = db.session.query(Package.date_start).filter_by(id=5).first()
    date_end = db.session.query(Package.date_end).filter_by(id=5).first()
    price_activity_1 = db.session.query(Package.price_activity_1).filter_by(id=5).first()
    price_activity_2 = db.session.query(Package.price_activity_2).filter_by(id=5).first()
    price_activity_3 = db.session.query(Package.price_activity_3).filter_by(id=5).first()
    price_activity_4 = db.session.query(Package.price_activity_4).filter_by(id=5).first()
    price_activity_5 = db.session.query(Package.price_activity_5).filter_by(id=5).first()
    activity_1 = db.session.query(Package.activity_1).filter_by(id=5).first()
    activity_2 = db.session.query(Package.activity_2).filter_by(id=5).first()
    activity_3 = db.session.query(Package.activity_3).filter_by(id=5).first()
    activity_4 = db.session.query(Package.activity_4).filter_by(id=5).first()
    activity_5 = db.session.query(Package.activity_5).filter_by(id=5).first()
    return render_template('Germany.html',
                            user=current_user,
                            price_flight = price_flight,
                            price_lodge = price_lodge,
                            date_start = date_start,
                            date_end = date_end,
                            price_activity_1 = price_activity_1,
                            price_activity_2 = price_activity_2,
                            price_activity_3 = price_activity_3,
                            price_activity_4 = price_activity_4,
                            price_activity_5 = price_activity_5,
                            activity_1 = activity_1,
                            activity_2 = activity_2,
                            activity_3 = activity_3,
                            activity_4 = activity_4,
                            activity_5 = activity_5,
                            id=5)