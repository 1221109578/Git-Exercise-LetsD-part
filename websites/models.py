from . import db 
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from sqlalchemy.sql import func

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

#------
class Seasons(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(150), nullable=False)
    country = db.Column(db.String(150), nullable=False)
    date = db.Column(db.String(150), nullable=False)
    event_id = db.Column(db.Integer, nullable=False)
#
#class Summer(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    event_name = db.Column(db.String(150), nullable=False)
#    country = db.Column(db.String(150), nullable=False)
#    date = db.Column(db.String(150), nullable=False)
#
#class Spring(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    event_name = db.Column(db.String(150), nullable=False)
#    country = db.Column(db.String(150), nullable=False)
#    date = db.Column(db.String(150), nullable=False)
#
#class Autumn(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    event_name = db.Column(db.String(150), nullable=False)
#    country = db.Column(db.String(150), nullable=False)
#    date = db.Column(db.String(150), nullable=False)
##------
