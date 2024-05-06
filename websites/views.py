from flask import Blueprint, render_template, request, flash, redirect ,url_for
from flask_login import login_required, current_user
from . import db

views = Blueprint('views', __name__)

@views.route("/", methods=['GET', 'POST'])
def home():
    return render_template('Home.html')

@views.route('/myaccount', methods=['GET','POST'])
@login_required
def myaccount():
    return render_template('myaccount.html')
from flask import Blueprint,render_template
