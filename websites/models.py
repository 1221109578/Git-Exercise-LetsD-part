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
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    payment_methods = db.relationship('PaymentMethod', backref='user', lazy=True)

class PaymentMethod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cardholder_name = db.Column(db.String(200), nullable=False)
    expiry_month = db.Column(db.Integer, nullable=False)
    expiry_year = db.Column(db.Integer, nullable=False)
    card_number_hash = db.Column(db.String(200), nullable=False)
    card_number_last_digits = db.Column(db.String(200), nullable=False)
    cvv_hash = db.Column(db.String(200),nullable=False)

class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    

class Packages(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100))
    city = db.Column(db.String(100))
    description = db.Column(db.String(100))
    price = db.Column(db.Float)
    days = db.Column(db.Integer)
    nights = db.Column(db.Integer)
    departure_date = db.Column(db.Date)
    return_date = db.Column(db.Date)
    airline_company = db.Column(db.String(100))
    hotel_name = db.Column(db.String(100))
    pax = db.Column(db.Integer)
    availability = db.Column(db.Integer)
    image_url = db.Column(db.String(200))
