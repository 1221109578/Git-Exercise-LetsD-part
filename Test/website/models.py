from . import db
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150))
    username = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    phone_number = db.Column(db.String(10))
    is_admin = db.Column(db.Boolean, default=False)
    carts = db.relationship('Cart', backref='user', lazy=True)
    payment_methods = db.relationship('PaymentMethod', backref='user', lazy=True)

class PaymentMethod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    card_number_hash = db.Column(db.String(128), nullable=False)
    card_number_last_digits = db.Column(db.String(4), nullable=False)
    cardholder_name = db.Column(db.String(200), nullable=False)
    expiry_month = db.Column(db.Integer, nullable=False)
    expiry_year = db.Column(db.Integer, nullable=False)
    cvv_hash = db.Column(db.String(128), nullable=False)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    travel_package_id = db.Column(db.Integer, db.ForeignKey('travel_package.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class TravelPackage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    continent = db.Column(db.String(100))  
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    description = db.Column(db.String(500))
    price = db.Column(db.Float)
    days = db.Column(db.Integer)
    nights = db.Column(db.Integer)
    date = db.Column(db.Date)
    date_end = db.Column(db.Date)
    airline_name = db.Column(db.String(100))
    hotel_name = db.Column(db.String(100))
    pax = db.Column(db.Integer)
    availability = db.Column(db.Integer)
    image_url = db.Column(db.String(200))
    carts = db.relationship('Cart', backref='travel_package', lazy=True)


    @hybrid_property
    def days(self):
        if self.date and self.date_end:
            return (self.date_end - self.date).days
        return None

    @hybrid_property
    def nights(self):
        if self.days is not None:
            return self.days - 1
        return None
    
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('travel_package.id'), nullable=False)  
    buyers_username = db.Column(db.String(150), nullable=False)
    package_place = db.Column(db.String(150), nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.relationship('User', backref='bookings')
    travel_package = db.relationship('TravelPackage', backref='bookings')
