from flask import Blueprint, render_template, request, flash, redirect ,url_for
from flask_login import login_required, current_user
from . import create_app
from .models import PaymentMethod, Seasons, TravelPackage, Cart, Booking
from . import db
import datetime

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
    # Filter Travel Packages' by quering the database
    continents = db.session.query(TravelPackage.continent).distinct().all()
    countries = db.session.query(TravelPackage.country).distinct().all()
    cities = db.session.query(TravelPackage.city).distinct().all()
    hotels = db.session.query(TravelPackage.hotel_name).distinct().all()
    airlines = db.session.query(TravelPackage.airline_name).distinct().all()
    paxes = db.session.query(TravelPackage.pax).distinct().all()

    # Get The Users' Filter From The Filter Form From HTML
    continent = request.args.get('continent')
    country = request.args.get('country')
    city = request.args.get('city')
    price_min = request.args.get('price_min')
    price_max = request.args.get('price_max')
    hotel = request.args.get('hotel')
    airline = request.args.get('airline')
    pax = request.args.get('pax')
    date_start = request.args.get('date_start')
    date_end = request.args.get('date_end')

    # See if the conditions matches with the users' preferences
    query = db.session.query(TravelPackage)
    if continent:
        query = query.filter_by(continent=continent)
    if country:
        query = query.filter_by(country=country)
    if city:
        query = query.filter_by(city=city)
    if price_min:
        query = query.filter(TravelPackage.price >= price_min)
    if price_max:
        query = query.filter(TravelPackage.price <= price_max)
    if hotel:
        query = query.filter_by(hotel_name=hotel)
    if airline:
        query = query.filter_by(airline_name=airline)
    if pax:
        query = query.filter_by(pax=pax)
    if date_start:
        query = query.filter(TravelPackage.date >= datetime.datetime.strptime(date_start, '%Y-%m-%d').date())
    if date_end:
        query = query.filter(TravelPackage.date <= datetime.datetime.strptime(date_end, '%Y-%m-%d').date())

    travel_packages = query.all()
    # Display Message If No Packages Meets User's Criteria
    if not travel_packages:
        message = "No travel packages match your criteria or no packages is availables"
        return render_template('package.html', message=message, user=current_user,
                               continents=continents, countries=countries, cities=cities,
                               hotels=hotels, airlines=airlines, paxes=paxes)

    return render_template('package.html', travel_packages=travel_packages, user=current_user,
                           continents=continents, countries=countries, cities=cities,
                           hotels=hotels, airlines=airlines, paxes=paxes)
    
    

@views.route("/Booking", methods=['GET', 'POST'])
@login_required
def booking():
    return render_template('Booking.html', user=current_user)

@views.route('/cart', methods=['GET','POST'])
@login_required
def cart():
    # Get The Data From User's Cart
    cart_items = current_user.carts
    # Calculate Cart's Total Price
    cart_total = sum(cart_item.travel_package.price * cart_item.quantity if cart_item.travel_package.price is not None else 0 for cart_item in cart_items)
    return render_template('cart.html',user=current_user, cart_items=cart_items, cart_total=cart_total)


@views.route('/add_to_cart/<int:package_id>', methods=['POST'])
@login_required
def add_to_cart(package_id):
    travel_package = TravelPackage.query.get(package_id)
    # See if Quantity is In Range
    if travel_package:
        quantity = int(request.form.get('quantity', 1))
        if quantity > 0 and quantity <= travel_package.availability:
            cart_item = Cart.query.filter_by(user=current_user, travel_package=travel_package).first()
            # Check if the item is already in cart
            if cart_item:
                cart_item.quantity += quantity
            else:
                # Add to Cart's database
                cart_item = Cart(user=current_user, travel_package=travel_package, quantity=quantity)
                db.session.add(cart_item)

            db.session.commit()

            flash('Travel package(s) added to cart successfully!', 'success')
        else:
            flash('Invalid quantity or insufficient availability!', 'alert')
    else:
        flash('Travel package not found!', 'alert')

    return redirect(url_for('views.cart'))

@views.route('/cart/remove/<int:cart_item_id>', methods=['GET'])
@login_required
def remove_from_cart(cart_item_id):
    # Get User's Selected Cart Items based on Cart's ID
    cart_item = Cart.query.get(cart_item_id)

    if cart_item:
        # Delete Selected Cart
        db.session.delete(cart_item)
        db.session.commit()
        flash('Item removed from cart successfully!', 'success')
    else:
        flash('Cart item not found!', 'alert')

    return redirect(url_for('views.cart'))

@views.route('/cart/update/<int:cart_item_id>', methods=['GET', 'POST'])
@login_required
def update_cart_item(cart_item_id):  
    # Get User's Selected Cart Items based on Cart's ID
    cart_item = Cart.query.get(cart_item_id)

    if cart_item:
        # Get The New Quantity 
        new_quantity = request.form.get('quantity')
        if new_quantity is not None: # Check If new_quantity is null or not
            if new_quantity != cart_item.quantity: # Update the user's cart quantity
                cart_item.quantity = new_quantity
                db.session.commit()
                flash('Cart item updated successfully!', 'success')
            else:
                flash('No changes made to the quantity!', 'alert')
        else:
            flash('Item is unavailable', 'alert')
    else:
        flash('Cart item not found!', 'alert')
    return redirect(url_for('views.cart'))

@views.route('/summary', methods=['GET', 'POST']) 
@login_required
def summary():
    # Get the require informations to render the template
    travel_package = TravelPackage.query.all()
    cart_items = current_user.carts
    cart_total = sum(cart_item.travel_package.price * cart_item.quantity if cart_item.travel_package.price is not None else 0 for cart_item in cart_items)
    full_name = current_user.full_name
    return render_template('summary.html', user=current_user, cart_items=cart_items, cart_total=cart_total, travel_package=travel_package, full_name=full_name)

@views.route('/cust-info', methods=['GET', 'POST'])
@login_required
def cust_info():
    cart_items = current_user.carts
    # To store the informations
    form_data = {}

    for cart_item in cart_items:
        package_id = cart_item.travel_package.id
        quantity = cart_item.quantity

        package_data = []
        for i in range(quantity):
            form_counter = i + 1
            pax_data = []
            # Get the infromations based on its packages numbers and its form numbers 
            for j in range(cart_item.travel_package.pax):
                pax_info = {
                    'airline_name': request.form.get(f'airline_name{package_id}_{form_counter}_{j+1}'),
                    'airline_ic': request.form.get(f'airline_ic{package_id}_{form_counter}_{j+1}')
                }
                pax_data.append(pax_info)
            # Get Head/Name for hotel's Informations
            form_info = {
                'name': request.form.get(f'name{package_id}_{form_counter}'),
                'ic': request.form.get(f'ic{package_id}_{form_counter}'),
                'airline_details': pax_data
            }
            package_data.append(form_info)

        form_data[package_id] = package_data

    return render_template('cust_info.html', user=current_user, form_data=form_data, cart_items=cart_items)

@views.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    # Get User's Cart Data 
    cart_items = current_user.carts
    payment_methods = PaymentMethod.query.filter_by(user_id=current_user.id).all()
    # Calculate Cart's Total
    cart_total = sum(cart_item.travel_package.price * cart_item.quantity if cart_item.travel_package.price is not None else 0 for cart_item in cart_items)

    if not payment_methods: # Will automatically redirect to the MyAccount page to add payment method.
        flash('Please add a payment method first', 'alert')
        return redirect(url_for('views.myaccount'))
    return render_template('checkout.html', user=current_user, cart_items=cart_items, payment_methods=payment_methods, cart_total=cart_total)

@views.route('/payed', methods=['POST', 'GET'])
@login_required
def paid():
    # Get the cart items for the current user
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    cart_total = sum(cart_item.travel_package.price * cart_item.quantity if cart_item.travel_package.price is not None else 0 for cart_item in cart_items)

    if cart_items:
        for cart_item in cart_items:
            # Get the package based on the package ID
            package = TravelPackage.query.get(cart_item.travel_package_id)

            if package and package.availability >= cart_item.quantity:
                # Update the quantity of the package
                package.availability -= cart_item.quantity
                db.session.commit()

                # Create a new booking record
                booking = Booking(
                    user_id=current_user.id,
                    package_id=package.id,
                    buyers_username=current_user.username,
                    package_place=f"{package.city}, {package.country}",
                    total_price = cart_total,
                    quantity=cart_item.quantity
                )
                db.session.add(booking)
                db.session.commit()

                # Remove the cart item
                db.session.delete(cart_item)
                db.session.commit()
            else:
                flash(f'Not enough quantity available for package ID {cart_item.travel_package_id}', category='alert')
                return redirect(url_for('client.cart'))

        flash('Booking successful', category='success')
    else:
        flash('No items in the cart', category='alert')

    return redirect(url_for('views.booking_history'))

@views.route('/history')
@login_required
def booking_history():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template('history.html', user=current_user, bookings=bookings)