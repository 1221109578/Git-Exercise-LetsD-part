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
    payment_methods = db.relationship('PaymentMethod', backref='user', lazy=True)

class PaymentMethod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cardholder_name = db.Column(db.String(200), nullable=False)
    expiry_month = db.Column(db.Integer, nullable=False)
    expiry_year = db.Column(db.Integer, nullable=False)
    card_number_hash = db.Column(db.String(200), nullable=False)
    card_number_last_digits = db.Column(db.String(200), nullable=False)
    cvv_hash = db.Column(db.String(200), nullable=False)


