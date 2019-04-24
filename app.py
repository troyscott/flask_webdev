from flask import Flask, render_template
from flask import session, redirect,url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment

# Flask Forms
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from datetime import datetime

 
'''
 __name__ is used to determine the path of 
 the application.

 This creates an application instance of Flask
'''
app = Flask(__name__)
app.config['SECRET_KEY'] = 'somestring123'
bootstrap = Bootstrap(app)
moment = Moment(app)

# Forms
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

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
        print('submit NameForm')
        session['name'] = form.name.data
       
        # url_for references the verify_sign_up method
        return redirect(url_for('verify_signup'))
    return render_template('simplesignup.html',
        form=form,
        name=name)


@app.route('/verifysignup')
def verify_signup():
    flash('Processing request ...')
    name = session.get('name')

    return render_template('verifysignup.html',
        name=name)


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
