from flask import Flask, render_template, request, flash, redirect, url_for
from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField, RadioField,SelectField
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


class RequiredIf(object):

    def __init__(self, *args, **kwargs):
        self.conditions = kwargs

    def __call__(self, form, field):
        for name, data in self.conditions.items():
            if name not in form._fields:
                validators.Optional()(field)
            else:
                condition_field = form._fields.get(name)
                if condition_field.data == data:
                    validators.DataRequired().__call__(form, field)
                else:
                    validators.Optional().__call__(form, field)


class IllnessForm(Form):
    medtype = RadioField('Which to edit ', choices=[('scurrent', 'Current'), ('spast', 'Past')], default='spast')
    cmedical = SelectField('Current Illness', [validators.DataRequired(), RequiredIf(medtype='scurrent')], choices=[('','Select'), ('HIGH BLOOD PRESSURE','High Blood Pressure'), ('DIABETES','Diabetes')], default='')
    pmedical = SelectField('Past Illness', [validators.DataRequired(), RequiredIf(medtype='pcurrent')], choices=[('', 'Select'), ('HIGH BLOOD PRESSURE', 'High Blood Pressure'),('DIABETES', 'Diabetes')], default='')



@app.route('/illnessinput', methods=['GET','POST'])
def illnessinput():
    form = IllnessForm(request.form)
    if request == 'POST' and form.validate():
        if form.medtype.data == 'scurrent':
            current = form.cmedical.data

            current_db = root.child('publications')
            current_db.push({
                    'current': current,
            })

            flash('Currant Medical History Inserted Sucessfully.', 'success')

        elif form.medtype.data == 'spast':
            past = form.pmedical.data

            past_db = root.child('publications')
            past_db.push({
                'title': form.pmedical.data,
            })

            flash('Past Medical History Inserted Sucessfully.', 'success')
        return render_template('IllnessInput.html', form=form)
    return render_template('IllnessInput.html', form=form)


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run()
