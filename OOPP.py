from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, StringField, PasswordField, validators, RadioField, SelectField, ValidationError, FileField, SubmitField, TextAreaField, DateField
import firebase_admin
from firebase_admin import credentials, db, storage
import registration as regist
from PastIllness import PastIllness
from CurrentIllness import CurrentIllness
import Forum as f
import csv
import products as pdt

cred = credentials.Certificate('cred/oopp-53405-firebase-adminsdk-82c85-5582818dd3.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://oopp-53405.firebaseio.com',
    'storageBucket':'gs://oopp-53405.appspot.com'
})

root = db.reference()

user_ref = db.reference('userbase')
forum_ref = db.reference('postbase')
# bucket = storage.bucket()

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


@app.route('/medshop/guardian')
def medshop_guardian():
    list = []
    with open('cough_pg1.csv',newline ='') as csv_file:
        reader = csv.reader(csv_file)
        next(reader, None)
        for data in reader:
            products = pdt.Products(data[0],data[1],data[2],data[3],data[4])
            list.append(products)
    return render_template('medshop.html',pdt=list)

@app.route('/medshop/watsons')
def medshop_watsons():
    list = []
    with open('cough_pg1.csv',newline ='') as csv_file:
        reader = csv.reader(csv_file)
        next(reader, None)
        for data in reader:
            products = pdt.Products(data[0],data[1],data[2],data[3],data[4])
            list.append(products)
    return render_template('medshop.html',pdt=list)


@app.route('/faq')
def faq():
    return render_template('faq.html')

class AddFriend(Form):
    friend_name = SubmitField('Add Friend')

@app.route('/profile/<username>', methods=['GET','POST'])
def user_profile(username):
    form = AddFriend(request.form)
    userbase = user_ref.get()
    if request.method == 'POST':
        add_user = request.form['form-add']
        key = session['key']
        user_update = user_ref.child(key).child('friends')
        user_update.update({
            add_user : 'from'
        })
        for user in userbase.items():
            if user[1]['username'] == add_user:
                friend_key = user[0]
                friend_update = user_ref.child(friend_key).child('friends')
                friend_update.update({
                    session['user_data']['username'] : 'to'
                })
        return redirect(url_for('user_profile',username=add_user))
    else:
        for user in userbase.items():
            if username == user[1]['username']:
                fname = user[1]['fname']
                lname = user[1]['lname']
                birthday = user[1]['birthday']
                gender = user[1]['gender']
                about = user[1]['about']
                friends = user[1]['friends']
                return render_template('profile.html', form=form, username=username,fname=fname,lname=lname,birthday=birthday,gender=gender,about=about,friends=friends)

class RespondFriend(Form):
    accept = SubmitField()
    reject = SubmitField()

@app.route('/my_friends', methods=['GET','POST'])
def my_friends():
    form = RespondFriend()
    key = session['key']
    friends = user_ref.child(key).child('friends').get()

    # if request.method == 'POST' and form.validate():
    #     form_name = request.form['form-name']
    #     if form_name == 'form':
    #         if form.accept.data:
    #             pass
    # else:
    pending_list = []
    for pending in friends.items():
        if pending[1] == 'from':
            pending_list.append(pending[0])
    return render_template('friends.html', pending_list=pending_list,form=form)

class ProfileForm(Form):
    gender = SelectField('My Gender',choices=[('Male','Male'),('Female','Female'),('Others','Others')])
    birthday = DateField('My Birthday')
    homephone = StringField('Home Phone Number')
    mobilephone = StringField('Mobile Phone Number')
    address = StringField('Address')
    postalcode = StringField('Postal Code')
    about = TextAreaField('About Me')

class AccountForm(Form):
    email = StringField('New Email', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password (Optional)', [
        validators.Length(min=6, max=50),
        validators.EqualTo('confirmpass', message='Passwords must match')
    ])
    confirmpass = PasswordField('Confirm New Password (Optional)')

class PictureForm(Form):
    picture = FileField('Upload Profile Picture')

@app.route('/edit_profile', methods=['GET','POST'])
def edit_profile():
    key = session['key']
    user_update = user_ref.child(key)
    user_data = user_ref.child(key).get()

    disp_gender = user_data['gender']
    disp_birthday = user_data['birthday']
    disp_about = user_data['about']
    disp_homephone = user_data['homephone']
    disp_mobilephone = user_data['mobilephone']
    disp_email = user_data['email']
    disp_address = user_data['address']
    disp_postalcode = user_data['postalcode']

    form = ProfileForm(request.form)
    form2 = AccountForm(request.form)
    form3 = PictureForm(request.form)
    if request.method == 'POST':
        form_name = request.form['form-name']
        if form_name == 'form':
            gender = form.gender.data
            birthday = str(form.birthday.data)
            about = form.about.data
            homephone = form.homephone.data
            mobilephone = form.mobilephone.data
            address = form.address.data
            postalcode = form.postalcode.data

            user_update.update({
                'gender': gender,
                'birthday': birthday,
                'about':about,
                'homephone':homephone,
                'mobilephone':mobilephone,
                'address':address,
                'postalcode':postalcode
            })
            flash('You have updated your profile settings','success')
        elif form_name == 'form2':
            wrong_info = False
            email = form2.email.data
            user_update.update({
                'email':email
            })
            if form2.password.data != '' and form2.validate():
                password = form2.password.data
                user_update.update({
                    'password':password
                })
            elif form2.password.data !='' and form2.validate() == False:
                wrong_info = True
                flash('Inncorrect password details','danger')
            if wrong_info == False:
                flash('You have updated your account settings','success')
        elif form_name == 'form3':
            pass
        return redirect(url_for('edit_profile'))
    return render_template('edit_profile.html',form=form, form2=form2, form3=form3, disp_gender=disp_gender,disp_birthday=disp_birthday,disp_about=disp_about,disp_email=disp_email,disp_homephone=disp_homephone,disp_mobilephone=disp_mobilephone,disp_address=disp_address,disp_postalcode=disp_postalcode)


class formpost(Form):
    title = StringField('Title:', [validators.length(min=3, max=30), validators.DataRequired()])
    content = TextAreaField('Content:', [validators.DataRequired()])
    type = RadioField('Type:', [validators.DataRequired()], choices=[('F', 'Fitness'),('N', 'Nutrition'),('O', 'Other')])


@app.route('/forumpost', methods=['POST', 'GET'])
def foruminput():
    form = formpost(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        content = form.content.data
        type = form.type.data
        forum = f.Forum(title, content, type)
        forum_db = root.child('postbase')
        forum_db.push({
            'title': forum.get_title(),
            'content': forum.get_content(),
            'type': forum.get_type()
        })
        flash('You have successfully post', 'success')
        return redirect(url_for('forum'))
    return render_template('forumpost.html', form=form)


@app.route('/forumDisplay')
def forum():
    forumbase = forum_ref.get()
    list = []
    for post in forumbase:
        eachpost = forumbase[post]
        forum = f.Forum(eachpost['title'], eachpost['content'], eachpost['type'])
        list.append(forum)
    return render_template('forumDisplay.html', forum=list)


def validate_registration(form, field):
    userbase = user_ref.get()
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
        validators.Length(min=6, max=50),
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
            'newsletter': user.get_newsletter(),
            'about': '',
            'friends': '',
            'birthday': '',
            'favourites': '',
            'gender': ''
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
        userbase = user_ref.get()
        for user in userbase.items():
            if user[1]['username'] == id and user[1]['password'] == password:
                session['user_data'] = user[1]
                session['logged_in'] = True
                session['id'] = id
                session['key'] = user[0]
                return redirect(url_for('home'))
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
    medtype = RadioField('Which to edit', choices=[('scurrent', 'Current'), ('spast', 'Past')], default='scurrent')
    illness = SelectField('Type of Illness', [validators.DataRequired()], choices=[('','Select'), ('HIGH BLOOD PRESSURE','High Blood Pressure'), ('DIABETES','Diabetes')], default='')
    startdate = DateField('Start Date', [validators.DataRequired()], format='%Y-%m-%d')
    enddate = DateField('End Date', [RequiredIf(medtype='spast')], format='%Y-%m-%d')


@app.route('/illnessinput', methods=['GET', 'POST'])
def illnessinput():
    form = IllnessForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.medtype.data == 'scurrent':
            illness = form.illness.data
            start = str(form.startdate.data)

            current = CurrentIllness(illness, start)

            current_db = user_ref.child('currentillness')
            current_db.push({
                'illness': current.get_illness(),
                'startdate': current.get_startdate(),
            })

            flash('Current Medical History Inserted Sucessfully.', 'success')

        elif form.medtype.data == 'spast':
            illness = form.illness.data
            start = str(form.startdate.data)
            end = str(form.enddate.data)

            past = PastIllness(illness, start, end)

            past_db = user_ref.child('pastillness')
            past_db.push({
                'illness': past.get_illness(),
                'startdate': past.get_startdate(),
                'enddate': past.get_enddate(),
            })

            flash('Past Medical History Inserted Sucessfully.', 'success')
        return redirect(url_for('login')) #supposed to link back to profile
    return render_template('IllnessInput.html', form=form)


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run()
