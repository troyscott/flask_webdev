from flask import render_template, session, redirect, url_for
from . import main
from .forms import NameForm
# Reference to SQLAlchemy
from .. import db
from ..models import User


# Routes

# use main.route instead opp.route for our Blueprint

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/simplesignup', methods=['GET', 'POST'])
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


@main.route('/verifysignup')
def verify_signup():
    flash('Processing request ...')
    name = session.get('name')
    is_known = session.get('known')

    return render_template('verifysignup.html',
        name=name, is_known=is_known)


@main.route('/current')
def current():
    return render_template('current.html',
        current_time=datetime.utcnow())

@main.route('/user/<name>')
def user(name):
    return render_template('user.html',
        name=name)
