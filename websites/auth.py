from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import re


auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Username or Password may be incorrect, Please try again.', category='error')
        else:
            flash('Username or Password may be incorrect, Please try again.', category='error')

    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    #Get the User info
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        full_name = request.form.get('full_name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        phone_number= request.form.get('phone_number')

        #Check if username or email has been taken
        email_check = User.query.filter_by(email=email).first()
        user_check = User.query.filter_by(username=username).first()
        if user_check:
            flash('Username already exists.', category='error')
        elif email_check:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 character', category='error')
        elif len(full_name) < 2:
            flash('Full name must be greater than 2 character', category='error')
        elif password != confirm_password:
            flash('Password don\'t match', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 character', category='error')
        elif not validate_phone_number(phone_number):
            flash('Invalid phone number format. Please enter a valid phone number.', category='error')
        else:
            new_user = User(email=email,username=username, full_name=full_name, password=generate_password_hash(
                confirm_password, method='pbkdf2:sha1'), phone_number=phone_number)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))

    return render_template('signup.html', user=current_user)

# Validate Phone Number
def validate_phone_number(number):
    pattern = r'^\+?\d{1,3}[-.\s]?\(?\d{1,3}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}$'
    return re.match(pattern, number) is not None

@auth.route('/phone', methods=['POST'])
@login_required
def update_phone_number():
    new_full_name = request.form.get('full_name')
    new_phone_number = request.form.get('phone')

    current_user.full_name = new_full_name
    current_user.phone_number = new_phone_number
    db.session.commit()

    flash('Phone number updated successfully.', category='success')
    return redirect(url_for('views.myaccount'))

@auth.route('/pass', methods=['POST'])
@login_required

def change_password():
    current_password = request.form.get('current-password')
    new_password = request.form.get('new-password')
    confirm_password = request.form.get('confirm-password')
    
    user = User.query.get(current_user.id)

    if not check_password_hash(user.password, current_password):
        flash('Current password is incorrect.', category='alert')
    elif new_password != confirm_password:
        flash('New password and confirmation do not match.', category='alert')
    elif check_password_hash(user.password, new_password):
        flash('New password must be different from the current password.', category='alert')
    elif len(new_password) < 7:
        flash('Password must be at least 7 character', category='alert')

    else:
        user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
        db.session.commit()
        flash('Password changed successfully.', category='success')

    return redirect(url_for('views.myaccount'))