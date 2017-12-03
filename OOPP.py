from flask import Flask, render_template, request, flash, redirect, url_for
from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField, RadioField
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate('cred/oopp-53405-firebase-adminsdk-82c85-5582818dd3.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://oopp-53405.firebaseio.com'
})

root = db.reference()

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/amenities')
def amenities():
    return render_template('amenities.html')

@app.route('/calculator')
def calculator():
    return render_template('calculator.html')

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

@app.route('/food_recipes')
def food_recipes():
    return render_template('food_recipes.html')

@app.route('/gym_fitness')
def gym_fitness():
    return render_template('gym_fitness.html')

@app.route('/medshop')
def medshop():
    return render_template('medshop.html')

@app.route('/my_profile')
def my_profile():
    return render_template('my_profile.html')

@app.route('/forumInput')
def foruminput():
    return render_template('forumInput.html')


@app.route('/forum')
def forum():
    return render_template('forum.html')

class RegistrationForm(Form):
    name = StringField('Your Full Name:', [validators.Length(min=1)])
    nric = StringField('Your NRIC:')
    email = StringField('Your Email Address:', [validators.Length(min=6, max=50),
                                          validators.DataRequired(),
                                          validators.EqualTo('confirmemail',message='Email must match')])
    confirmemail = StringField('Confirm Email Address:')
    password = PasswordField('Enter a Password:', [
        validators.DataRequired(),
        validators.EqualTo('confirmpass', message='Passwords must match')
    ])
    confirmpass = PasswordField('Confirm Password:')
    phone = IntegerField('Your Phone Number:')
    newsletter = RadioField('Would you like to receive monthly newsletters from us through email?',choices=[('Y','Yes'),('N','No')])

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm(request.form)
    if request == 'POST' and form.validate():
        return render_template('register.html',form=form)
    return render_template('register.html',form=form)


@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run()
