from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField, RadioField,SelectField, ValidationError
import firebase_admin
from firebase_admin import credentials, db
import registration as regist

cred = credentials.Certificate('cred/oopp-53405-firebase-adminsdk-82c85-5582818dd3.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://oopp-53405.firebaseio.com'
})

root = db.reference()

userref = db.reference('userbase')

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

@app.route('/gym_fitness')
def gym_fitness():
    return render_template('gym_fitness.html')


@app.route('/medshop')
def medshop():
    return render_template('medshop.html')

@app.route('/profile/<username>')
def user_profile(username):
    userbase = userref.get()
    for user in userbase.items():
        if username == user[1]['username']:
                fname = user[1]['fname']
                lname = user[1]['lname']
                return render_template('profile.html', username=username,fname=fname,lname=lname)

@app.route('/edit_profile')
def edit_profile():
    return render_template('edit_profile.html')

@app.route('/forumInput')
def foruminput():
    return render_template('forumInput.html')

@app.route('/forum')
def forum():
    return render_template('forum.html')

def validate_registration(form, field):
    userbase = userref.get()
    for user in userbase.items():
        if user[1]['username'] == field.data:
            raise ValidationError('Username is already taken')
        elif user[1]['email'] == field.data:
            raise ValidationError('Email has already been used')
        elif user[1]['nric'] == field.data:
            raise ValidationError('You have already registered with this NRIC')

class RegistrationForm(Form):
    fname = StringField('*First Name', [validators.Length(min=1), validators.DataRequired()])
    lname  = StringField('*Last Name', [validators.Length(min=1), validators.DataRequired()])
    username = StringField('*Username', [validators.Length(min=6,max=20), validators.DataRequired(), validate_registration])
    nric = StringField('*NRIC',[validators.DataRequired(), validate_registration])
    email = StringField('*Email Address', [validators.Length(min=6, max=50),
                                          validators.DataRequired(),
                                          validators.EqualTo('confirmemail',message='Email must match'), validate_registration])
    confirmemail = StringField('*Confirm Email Address:',[validators.DataRequired()])
    password = PasswordField('*Password', [
        validators.DataRequired(),
        validators.EqualTo('confirmpass', message='Passwords must match')
    ])
    confirmpass = PasswordField('*Confirm Password',[validators.DataRequired()])
    homephone = StringField('Home Phone Number')
    mobilephone = StringField('Mobile Phone Number')
    address = StringField('*Address', [validators.DataRequired()])
    postalcode = StringField('*Postal Code', [validators.Length(min=6,max=6)])
    newsletter = RadioField('Would you like to receive monthly newsletters from us through email?',choices=[('Y','Yes'),('N','No')])

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        fname = form.fname.data.title()
        lname = form.lname.data.title()
        username = form.username.data
        nric = form.nric.data.upper()
        email = form.email.data
        password = form.password.data
        homephone = form.homephone.data
        mobilephone = form.mobilephone.data
        address = form.address.data
        postalcode = form.postalcode.data
        newsletter = form.newsletter.data
        user = regist.User(fname,lname,username,nric,email,password,homephone,mobilephone,address,postalcode,newsletter)
        user_db = root.child('userbase')
        user_db.push({
            'fname': user.get_fname(),
            'lname': user.get_lname(),
            'username': user.get_username(),
            'nric': user.get_nric(),
            'email': user.get_email(),
            'password': user.get_password(),
            'homephone': user.get_homephone(),
            'mobilephone': user.get_mobilephone(),
            'address': user.get_address(),
            'postalcode': user.get_postalcode(),
            'newsletter': user.get_newsletter()
        })
        flash('You have successfully created an account','success')
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

class LoginForm(Form):
    id = StringField('Username:',[validators.DataRequired()])
    password = PasswordField('Password:',[validators.DataRequired()])

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method =='POST' and form.validate():
        id = form.id.data
        password = form.password.data
        userbase = userref.get()
        for user in userbase.items():
            if user[1]['username'] == id and user[1]['password'] == password:
                session['user_data'] = user[1]
                session['logged_in'] = True
                session['id'] = id
                session['key'] = user
                return redirect(url_for('home'))
            else:
                flash('Invalid Login', 'danger')
                return render_template('login.html', form=form)
    elif request.method=='POST' and form.validate()==False:
        flash('Please enter your details', 'danger')
        return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('login'))

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


# userbase = userref.get()
# for user in userbase.items():
#     print(user[1]['password'])
#     print(user[1]['nric'])
#     print(user[1])
# username = 'fattycuty'
# userbase = userref.get()
# for user in userbase.items():
#     if username == user[1]['username']:
#             fname = user['fname']
#             lname = user['lname']
#             print(fname)
if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run()
