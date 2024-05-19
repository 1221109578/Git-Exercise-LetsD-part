from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db

event = Blueprint('event', __name__)

@event.route("/winter")
def winter():
    return render_template('winter.html')