from flask import Blueprint, render_template, request
from flask_login import current_user, login_user, logout_user, login_required

views = Blueprint('views', __name__)

@views.route('/')
def home():


    return render_template('home.html', user=current_user)