import pytest
from flask import url_for
from flask_login import current_user

from website import create_app, db
from website.models import User
from werkzeug.security import check_password_hash, generate_password_hash


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def user():
    user = User(email='test@example.com', first_name='Test', password='password')
    db.session.add(user)
    db.session.commit()
    return user

def test_login_get(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

# def test_login_post_success(client, user):
#     response = client.post('/login', data=dict(
#         email='test@example.com',
#         password='password'
#     ), follow_redirects=True)
#
#     assert response.status_code == 200
#     assert b'You have successfully logged in' in response.data
#     assert current_user.is_authenticated
#     assert response.request.path == url_for('views.home')

def test_login_post_incorrect_password(client, user):
    response = client.post('/login', data=dict(
        email='test@example.com',
        password='wrongpassword'
    ), follow_redirects=True)

def test_login_post_nonexistent_user(client):
    response = client.post('/login', data=dict(
        email='nonexistent@example.com',
        password='password'
    ), follow_redirects=True)

    assert response.status_code == 200
    assert b'Incorrect email or password' in response.data
    #assert not current_user.is_authenticated

def test_signup(client):
    response = client.post('/signup', data={
        'email': 'test@example.com',
        'firstName': 'Test',
        'password1': 'password',
        'password2': 'password'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'You have successfully registered' in response.data

    user = User.query.filter_by(email='test@example.com').first()
    assert user is not None
    assert user.first_name == 'Test'
    assert check_password_hash(user.password, 'password')

def test_signup_email_already_registered(client):
    user = User(email='existing@example.com', first_name='Existing', password='password')
    db.session.add(user)
    db.session.commit()

    response = client.post('/signup', data={
        'email': 'existing@example.com',
        'firstName': 'Test',
        'password1': 'password',
        'password2': 'password'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Email already registered' in response.data

def test_signup_passwords_do_not_match(client):
    response = client.post('/signup', data={
        'email': 'test2@example.com',
        'firstName': 'Test',
        'password1': 'password1',
        'password2': 'password2'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Passwords must match' in response.data

def test_signup_short_password(client):
    response = client.post('/signup', data={
        'email': 'test3@example.com',
        'firstName': 'Test',
        'password1': 'pw',
        'password2': 'pw'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Password must be at least 3 characters' in response.data

def test_signup_short_email(client):
    response = client.post('/signup', data={
        'email': 't@e',
        'firstName': 'Test',
        'password1': 'password',
        'password2': 'password'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Email must be at least 6 characters' in response.data

def test_signup_short_first_name(client):
    response = client.post('/signup', data={
        'email': 'test4@example.com',
        'firstName': 'Te',
        'password1': 'password',
        'password2': 'password'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'First name must be at least 3 characters' in response.data
