from flask import Flask, render_template
from flask import session, redirect,url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment

# Flask Forms
'''
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
'''

# Sql Alchemy
from flask_sqlalchemy import SQLAlchemy

import os
from datetime import datetime

# Import forms
from forms import NameForm

 
'''
 __name__ is used to determine the path of 
 the application.

 This creates an application instance of Flask
'''
# Bad design current scope
app = Flask(__name__)
app.config['SECRET_KEY'] = 'somestring123'
basedir = os.path.abspath(os.path.dirname(__file__))
os_path = os.path.join(basedir, 'data.sqlite')
db_uri = 'sqlite:///{}'.format(os_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

# Models

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name    


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr_(self):
        return '<User %r>' % self.name


# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simplesignup', methods=['GET', 'POST'])
def simple_signup():
    name = None
    form = NameForm()
    print('Get NameForm')
    if form.validate_on_submit():
        # Checks to see if the user exists
        print("name:", form.name.data)
        user = User.query.filter_by(username=form.name.data).first()
        # if the user does not exist then add the user
        if user is None:
            # Create a new user
            user = User(username=form.name.data, role_id=3)
            # add to database
            db.session.add(user)
            # commit changes
            db.session.commit()
            session["known"] = False
        # if the user exists ...
        else:
            session["known"] = True
        session["name"] = form.name.data
        # url_for references the verify_sign_up method
        return redirect(url_for('verify_signup'))
    return render_template('simplesignup.html',
        form=form,
        name=name)


@app.route('/verifysignup')
def verify_signup():
    flash('Processing request ...')
    name = session.get('name')
    is_known = session.get('known')

    return render_template('verifysignup.html',
        name=name, is_known=is_known)


@app.route('/current')
def current():
    return render_template('current.html',
        current_time=datetime.utcnow())

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',
        name=name)

@app.errorhandler(404)
def page_not_found(e):
        return render_template('404.html'), 404
