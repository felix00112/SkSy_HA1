from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
from website.models import User
from flask_login import current_user, login_user, logout_user, login_required

# all routes needed for authentication

auth = Blueprint('auth', __name__)

# route for signup page
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    # getting data from form
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # checks if registration is valid
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already registered',category='error')
        elif len(email) < 3:
            flash('Email must be at least 3 characters', category='error')
        elif len(first_name) < 3:
            flash('First name must be at least 3 characters', category='error')
        elif len(password1) < 3:
            flash('Password must be at least 3 characters', category='error')
        elif password1 != password2:
            flash('Passwords must match', category='error')
        else:
            # add user to database
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('You have successfully registered', category='success')
            return redirect(url_for('views.home'))  # Ensure to return the result of redirect

    return render_template('sign_up.html', user=current_user)

# route for login page
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # getting data from form
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        # check if user exists in database
        if user:
            if check_password_hash(user.password, password):
                flash('You have successfully logged in', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect email or password', category='error')
        else:
            flash('Incorrect email or password', category='error')

    return render_template('login.html', user=current_user)

# route for logout
@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))