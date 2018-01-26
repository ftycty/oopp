from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, StringField, PasswordField, validators, RadioField, SelectField, ValidationError, FileField, \
    SubmitField, TextAreaField, DateField
import firebase_admin
from firebase_admin import credentials, db
import registration as regist
from wtforms.fields.html5 import DateField
from PastIllness import PastIllness
from CurrentIllness import CurrentIllness
from Common import Common
import Forum as f
import Nutrition as n
import Fitness as fit
import csv
import json
import g_products as g_pdt
import w_products as w_pdt
import BMI as b

cred = credentials.Certificate('cred/oopp-53405-firebase-adminsdk-82c85-5582818dd3.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://oopp-53405.firebaseio.com',
    'storageBucket': 'gs://oopp-53405.appspot.com'
})

root = db.reference()

user_ref = db.reference('userbase')
forum_ref = db.reference('postbase')

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


class bmi(Form):
    weight = StringField('Weight:', [validators.data_required()])
    height = StringField('Height:', [validators.data_required()])


@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    key = session['key']
    user = user_ref.child(key)
    form = bmi(request.form)
    if request.method == 'POST' and form.validate():
        weight = float(form.weight.data)
        height = float(form.height.data)
        BMI = b.BMI(weight, height)
        bmi_db = user.child('BodyMassIndex')
        bmi_db.update({
            "BMI": str(BMI.get_bmi())
        })
        flash('You have successfully post', 'success')
        return redirect(url_for('calculator'))
    return render_template('calculator.html', form=form)


@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')


@app.route('/gym_fitness')
def gym_fitness():
    return render_template('gym_fitness.html')


@app.route('/medshop')
def medshop_main():
    website = 'main'
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    with open('scrape_files/g_cough_pg1.csv', newline='') as csv_file:
        reader = csv.reader(csv_file)
        next(reader, None)
        for data in reader:
            products = g_pdt.Products(data[0], data[1], data[2], data[3], data[4], data[5])
            list1.append(products)
            if len(list1) == 6:
                break
    with open('scrape_files/g_pain_pg1.csv', newline='', encoding='cp932', errors='ignore') as csv_file:
        reader = csv.reader(csv_file)
        next(reader, None)
        for data in reader:
            products = g_pdt.Products(data[0], data[1], data[2], data[3], data[4], data[5])
            list2.append(products)
            if len(list2) == 6:
                break
    with open('scrape_files/w_cold_pg1.csv', newline='') as csv_file:
        reader = csv.reader(csv_file)
        next(reader, None)
        for data in reader:
            products = w_pdt.Products(data[0], data[1], data[2], data[3], data[4])
            list3.append(products)
            if len(list3) == 6:
                break
    with open('scrape_files/w_fever_pg1.csv', newline='') as csv_file:
        reader = csv.reader(csv_file)
        next(reader, None)
        for data in reader:
            products = w_pdt.Products(data[0], data[1], data[2], data[3], data[4])
            list4.append(products)
            if len(list4) == 6:
                break
    return render_template('medshop.html', website=website, list1=list1, list2=list2, list3=list3, list4=list4)


@app.route('/medshop/guardian/<type>')
@app.route('/medshop/guardian/<type>/<page>')
def medshop_guardian(type, page='1'):
    if type == 'cough_cold_allergy' and page == '1':
        list = []
        with open('scrape_files/g_cough_pg1.csv', newline='') as csv_file:
            reader = csv.reader(csv_file)
            next(reader, None)
            for data in reader:
                products = g_pdt.Products(data[0], data[1], data[2], data[3], data[4], data[5])
                list.append(products)
    elif type == 'cough_cold_allergy' and page == '2':
        list = []
        with open('scrape_files/g_cough_pg2.csv', newline='', encoding='cp932', errors='ignore') as csv_file:
            reader = csv.reader(csv_file)
            next(reader, None)
            for data in reader:
                products = g_pdt.Products(data[0], data[1], data[2], data[3], data[4], data[5])
                list.append(products)
    elif type == 'pain_fever' and page == '1':
        list = []
        with open('scrape_files/g_pain_pg1.csv', newline='', encoding='cp932', errors='ignore') as csv_file:
            reader = csv.reader(csv_file)
            next(reader, None)
            for data in reader:
                products = g_pdt.Products(data[0], data[1], data[2], data[3], data[4], data[5])
                list.append(products)
    website = 'Guardian'
    return render_template('medshop.html', pdt=list, website=website, type=type, page=page)


@app.route('/medshop/watsons/<type>')
@app.route('/medshop/watsons/<type>/<page>')
def medshop_watsons(type, page='1'):
    if type == 'colds_flu_nasal' and page == '1':
        list = []
        with open('scrape_files/w_cold_pg1.csv', newline='') as csv_file:
            reader = csv.reader(csv_file)
            next(reader, None)
            for data in reader:
                products = w_pdt.Products(data[0], data[1], data[2], data[3], data[4])
                list.append(products)
    elif type == 'fever_analgesics' and page == '1':
        list = []
        with open('scrape_files/w_fever_pg1.csv', newline='') as csv_file:
            reader = csv.reader(csv_file)
            next(reader, None)
            for data in reader:
                products = w_pdt.Products(data[0], data[1], data[2], data[3], data[4])
                list.append(products)
    website = 'Watsons'
    return render_template('medshop.html', pdt=list, website=website, type=type, page=page)


@app.route('/faq')
def faq():
    return render_template('faq.html')


class AddFriend(Form):
    friend_name = SubmitField('Add Friend')


@app.route('/profile/<username>', methods=['GET', 'POST'])
def user_profile(username):
    form = AddFriend(request.form)
    userbase = user_ref.get()
    current_list = []
    past_list = []
    sports_list = []
    if request.method == 'POST':
        add_user = request.form['form-add']
        key = session['key']
        user_update = user_ref.child(key).child('friends')
        user_update.update({
            add_user: 'from'
        })
        for user in userbase.items():
            if user[1]['username'] == add_user:
                friend_key = user[0]
                friend_update = user_ref.child(friend_key).child('friends')
                friend_update.update({
                    session['user_data']['username']: 'to'
                })
        return redirect(url_for('user_profile', username=add_user))
    else:
        key = session['key']
        friends = user_ref.child(key).child('friends').get()
        friends_list = []
        pending_list = []
        for current in friends.items():
            if current[1] == 'friends':
                friends_list.append(current[0])
            elif current[1] == 'from':
                pending_list.append(current[0])
        for user in userbase.items():
            if username == user[1]['username']:
                fname = user[1]['fname']
                lname = user[1]['lname']
                birthday = user[1]['birthday']
                gender = user[1]['gender']
                about = user[1]['about']
                friends = user[1]['friends']
                try:
                    sports = user[1]['sports']
                    try:
                        for sport in sports.items():
                            s = sport[0]
                            sports_list.append(s)
                    except AttributeError:
                        pass
                except AttributeError and KeyError:
                    pass
                try:
                    current = user[1]['currentillness']
                    try:
                        for illness in current.items():
                            c = illness[0]
                            cdate = illness[1]['startdate']
                            current = CurrentIllness(c, cdate)
                            current_list.append(current)
                    except AttributeError:
                        pass
                except AttributeError and KeyError:
                    pass

                try:
                    past = user[1]['pastillness']
                    try:
                        for illness in past.items():
                            p = illness[0]
                            pdate = illness[1]['startdate']
                            pedate = illness[1]['enddate']
                            past = PastIllness(p, pdate, pedate)
                            past_list.append(past)
                    except AttributeError:
                        pass
                except AttributeError and KeyError:
                    pass

                if 'None' in sports_list:
                    sports_list.remove('None')

                return render_template('profile.html', form=form, friends_list=friends_list, username=username,
                                       pending_list=pending_list, fname=fname, lname=lname, birthday=birthday,
                                       gender=gender, about=about, friends=friends, sports=sports_list,
                                       current=current_list, past=past_list)


class RespondFriend(Form):
    accept = SubmitField()
    reject = SubmitField()


class SearchFriend(Form):
    search = StringField('Find Friend', [validators.DataRequired])


class DeleteFriend(Form):
    del_friend = StringField('Remove Friend')


@app.route('/my_friends', methods=['GET', 'POST'])
def my_friends():
    userbase = user_ref.get()
    keys = []
    my_list = []
    common = []
    user_dict = {}
    form = RespondFriend(request.form)
    form2 = SearchFriend(request.form)
    form3 = DeleteFriend(request.form)
    key = session['key']
    friends = user_ref.child(key).child('friends').get()

    for user in userbase.items():
        if user[1]['username'] == session['id']:
            my_sport = user[1]['sports']
            for sport in my_sport:
                my_list.append(sport)

        if user[1]['username'] != session['id']:
            keys.append(user[0])
            sport_list = []
            user_sport = user[1]['sports']
            for sport in user_sport:
                sport_list.append(sport)
                user_dict[user[0]] = sport_list

    for u in keys:
        this = user_dict[u]
        for each in this:
            if each in my_list:
                name = userbase[u]['username']
                c = Common(name)
                common.append(c)
                break

    if request.method == 'POST' and form.validate():
        form_name = request.form['form-name']
        if form_name == 'form':
            if form.accept.data:
                add_user = request.form['form-username']
                key = session['key']
                user_update = user_ref.child(key).child('friends')
                user_update.update({
                    add_user: 'friends'
                })
                for user in userbase.items():
                    if user[1]['username'] == add_user:
                        friend_key = user[0]
                        friend_update = user_ref.child(friend_key).child('friends')
                        friend_update.update({
                            session['user_data']['username']: 'friends'
                        })
                flash('You have accepted ' + add_user + "'s friend request!", 'success')
            elif form.reject.data:
                add_user = request.form['form-username']
                key = session['key']
                user_ref.child(key).child('friends').child(add_user).delete()
                for user in userbase.items():
                    if user[1]['username'] == add_user:
                        friend_key = user[0]
                        user_ref.child(friend_key).child('friends').child(session['user_data']['username']).delete()
                flash('You have rejected ' + add_user + "'s friend request.", 'danger')
            return redirect(url_for('my_friends'))
        elif form_name == 'form2':
            search_user = form2.search.data.strip()
            for user in userbase.items():
                if user[1]['username'] == search_user:
                    return redirect(url_for('user_profile', username=search_user))
            flash('User not found', 'danger')
            return redirect(url_for('my_friends'))
        elif form_name == 'form3':
            delete_user = form3.del_friend.data.strip()
            key = session['key']
            check = user_ref.child(key).child('friends').get()
            for check in check:
                if check == delete_user:
                    user_ref.child(key).child('friends').child(delete_user).delete()
                    flash('You have successfully removed ' + delete_user + ' as a friend.', 'success')
                    return redirect(url_for('my_friends'))
            flash('You do not have ' + delete_user + ' as a friend!', 'danger')
            return redirect(url_for('my_friends'))

    else:
        pending_list = []
        friends_list = []
        for pending in friends.items():
            if pending[1] == 'to':
                pending_list.append(pending[0])
        for current in friends.items():
            if current[1] == 'friends':
                friends_list.append(current[0])

        return render_template('friends.html', pending_list=pending_list, friends_list=friends_list, form=form,
                               form2=form2, form3=form3, common_list=common)


class ProfileForm(Form):
    gender = SelectField('My Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')])
    birthday = DateField('My Birthday')
    homephone = StringField('Home Phone Number', [validators.Length(min=8, max=8)])
    mobilephone = StringField('Mobile Phone Number', [validators.Length(min=8, max=8)])
    address = StringField('Address')
    postalcode = StringField('Postal Code', [validators.Length(min=6, max=6)])
    about = TextAreaField('About Me')
    sports = SelectField('Your Interests',
                         choices=[('running', 'Running'), ('swimming', 'Swimming'), ('badminton', 'Badminton'),
                                  ('volleyball', 'Volleyball'), ('soccer', 'Soccer')])


class AccountForm(Form):
    email = StringField('New Email', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password (Optional)', [
        validators.Length(min=6, max=50),
        validators.EqualTo('confirmpass', message='Passwords must match')
    ])
    confirmpass = PasswordField('Confirm New Password (Optional)')


class PictureForm(Form):
    picture = FileField('Upload Profile Picture')


@app.route('/edit_profile', methods=['GET', 'POST'])
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
    disp_sports = user_data['sports']

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
            sports = form.sports.data

            sports_db = user_update.child('sports')
            sports_db.update({
                sports: sports,
            })
            user_update.update({
                'gender': gender,
                'birthday': birthday,
                'about': about,
                'homephone': homephone,
                'mobilephone': mobilephone,
                'address': address,
                'postalcode': postalcode
            })

            flash('You have updated your profile settings', 'success')

        elif form_name == 'form2':
            wrong_info = False
            email = form2.email.data
            user_update.update({
                'email': email
            })
            if form2.password.data != '' and form2.validate():
                password = form2.password.data
                user_update.update({
                    'password': password
                })
            elif form2.password.data != '' and form2.validate() == False:
                wrong_info = True
                flash('Inncorrect password details', 'danger')
            if wrong_info == False:
                flash('You have updated your account settings', 'success')
        elif form_name == 'form3':
            pass
        return redirect(url_for('edit_profile'))
    return render_template('edit_profile.html', form=form, form2=form2, form3=form3, disp_gender=disp_gender,
                           disp_birthday=disp_birthday, disp_about=disp_about, disp_email=disp_email,
                           disp_homephone=disp_homephone,
                           disp_mobilephone=disp_mobilephone, disp_address=disp_address,
                           disp_postalcode=disp_postalcode, disp_sports=disp_sports)


class formpost(Form):
    title = StringField('Title:', [validators.length(min=3), validators.DataRequired()])
    content = TextAreaField('Content:', [validators.DataRequired()])
    type = RadioField('Type:', [validators.DataRequired()],
                      choices=[('F', 'Fitness'), ('N', 'Nutrition'), ('O', 'Other')])
    posttime = DateField('Date and Time:', format='%Y-%m-%d %H:%M:%S')
    # nutrition
    ingredient = TextAreaField('Ingredients:')
    method = TextAreaField('Methods:')
    # exercise
    exercise = TextAreaField('Exercise:')
    time = StringField('Duration:')


@app.route('/forumpost', methods=['GET', 'POST'])
def foruminput():
    form = formpost(request.form)
    if request.method == 'POST' and form.validate():
        if form.type.data == 'O':
            title = form.title.data
            content = form.content.data
            type = form.type.data
            other = f.Forum(title, content, type)
            forum_db = root.child('postbase')
            forum_db.push({
                'title': other.get_title(),
                'content': other.get_content(),
                'type': other.get_type()
            })
            flash('You have successfully post', 'success')
        elif form.type.data == 'N':
            title = form.title.data
            content = form.content.data
            type = form.type.data
            method = form.method.data
            ingredient = form.ingredient.data
            nutrition = n.Nutrition(title, content, type, ingredient, method)
            forum_db = root.child('postbase')
            forum_db.push({
                'title': nutrition.get_title(),
                'content': nutrition.get_content(),
                'type': nutrition.get_type(),
                'ingredient': nutrition.get_ingredient(),
                'method': nutrition.get_method()

            })
            flash('You have successfully post', 'success')
        elif form.type.data == 'F':
            title = form.title.data
            content = form.content.data
            type = form.type.data
            exercise = form.exercise.data
            time = form.time.data
            fitness = fit.Fitness(title, content, type, exercise, time)
            forum_db = root.child('postbase')
            forum_db.push({
                'title': fitness.get_title(),
                'content': fitness.get_content(),
                'type': fitness.get_type(),
                'exercise': fitness.get_exercise(),
                'time': fitness.get_time()
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
        if eachpost['type'] == 'O':
            other = f.Forum(eachpost['title'], eachpost['content'], eachpost['type'])
            list.append(other)
        elif eachpost['type'] == 'F':
            fitness = fit.Fitness(eachpost['title'], eachpost['content'], eachpost['type'], eachpost['exercise'],
                                  eachpost['time'])
            list.append(fitness)
        elif eachpost['type'] == 'N':
            nutrition = n.Nutrition(eachpost['title'], eachpost['content'], eachpost['type'], eachpost['ingredient'],
                            eachpost['method'])
            list.append(nutrition)
    return render_template('forumDisplay.html', forum=list)


def validate_registration(form, field):
    userbase = user_ref.get()
    for user in userbase.items():
        if user[1]['username'] == field.data:
            raise ValidationError('Username is already taken')
        if user[1]['email'] == field.data:
            raise ValidationError('Email has already been used')
        if user[1]['nric'] == field.data:
            raise ValidationError('You have already registered with this NRIC')


def phone_length(form, field):
    if field.data == '':
        pass
    elif field.data.isalpha():
        raise ValidationError('Your phone number should only contain numbers')
    elif len(field.data) != 8:
        raise ValidationError('Your phone number should contain 8 numbers')


class RegistrationForm(Form):
    fname = StringField('*First Name', [validators.Length(min=1), validators.DataRequired()])
    lname = StringField('*Last Name', [validators.Length(min=1), validators.DataRequired()])
    username = StringField('*Username',
                           [validators.Length(min=6, max=12), validators.DataRequired(), validate_registration])
    nric = StringField('*NRIC', [validators.DataRequired(), validate_registration])
    email = StringField('*Email Address', [validators.Length(min=6, max=50),
                                           validators.DataRequired(),
                                           validators.EqualTo('confirmemail', message='Email must match'),
                                           validate_registration])
    confirmemail = StringField('*Confirm Email Address:', [validators.DataRequired()])
    password = PasswordField('*Password', [
        validators.Length(min=6, max=50),
        validators.DataRequired(),
        validators.EqualTo('confirmpass', message='Passwords must match')
    ])
    confirmpass = PasswordField('*Confirm Password', [validators.DataRequired()])
    homephone = StringField('Home Phone Number', [phone_length])
    mobilephone = StringField('Mobile Phone Number', [phone_length])
    address = StringField('*Address', [validators.DataRequired()])
    postalcode = StringField('*Postal Code', [validators.DataRequired(), validators.Length(min=6, max=6)])
    newsletter = RadioField('Would you like to receive monthly newsletters from us through email?',
                            choices=[('Y', 'Yes'), ('N', 'No')])


@app.route('/register', methods=['GET', 'POST'])
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
        user = regist.User(fname, lname, username, nric, email, password, homephone, mobilephone, address, postalcode,
                           newsletter)
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
            'friends': {'dummy': 'user'},
            'birthday': '',
            'favourites': '',
            'gender': '',
            'currentillness': '',
            'pastillness': '',
            'healthtips': 'yes',
            'sports': ''
        })
        flash('You have successfully created an account', 'success')
        return redirect(url_for('login'))
    used_username = []
    used_email = []
    userbase = user_ref.get()
    for user in userbase.items():
        used_username.append(user[1]['username'])
        used_email.append(user[1]['email'])
    return render_template('register.html', form=form, used_username=used_username, used_email=used_email)


class LoginForm(Form):
    id = StringField('Username:', [validators.DataRequired()])
    password = PasswordField('Password:', [validators.DataRequired()])


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
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
    elif request.method == 'POST' and form.validate() == False:
        flash('Please enter your details', 'danger')
        return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
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


# def validate_current_illness(form, field):
#     key = session['key']
#     userbase = user_ref.child(key)
#     current_db = userbase.get('currentillness')
#     for illness in current_db.items():
#         if illness == field.data
#             raise ValidationError('This current illness has already been added')
#
#
# def validate_past_illness(form, field):
#     key = session['key']
#     userbase = user_ref.child(key)
#     past_db = userbase.get('pastillness')
#     for illness in past_db.items():
#         if illness == field.data:
#             raise ValidationError('This past illness has already been added')


class IllnessForm(Form):
    medtype = RadioField('Which to edit', choices=[('scurrent', 'Current'), ('spast', 'Past')], default='scurrent')
    illness = SelectField('Type of Illness', [validators.DataRequired()],
                          choices=[('', 'Select'), ('High Blood Pressure', 'High Blood Pressure'),
                                   ('Diabetes', 'Diabetes')], default='')
    startdate = DateField('Start Date', [validators.DataRequired()], format='%Y-%m-%d')
    enddate = DateField('End Date', [RequiredIf(medtype='spast')], format='%Y-%m-%d')


@app.route('/illnessinput', methods=['GET', 'POST'])
def illnessinput():
    key = session['key']
    user = user_ref.child(key)
    form = IllnessForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.medtype.data == 'scurrent':
            illness = form.illness.data
            start = str(form.startdate.data)

            current = CurrentIllness(illness, start)

            current_db = user.child('currentillness')
            current_date_db = current_db.child(form.illness.data)
            current_date_db.update({
                'startdate': current.get_startdate(),
            })

            flash('Current Medical History Inserted Sucessfully.', 'success')

        elif form.medtype.data == 'spast':
            illness = form.illness.data
            start = str(form.startdate.data)
            end = str(form.enddate.data)

            past = PastIllness(illness, start, end)

            past_db = user.child('pastillness')
            past_date_db = past_db.child(form.illness.data)
            past_date_db.update({
                'startdate': past.get_startdate(),
                'enddate': past.get_enddate(),
            })

            flash('Past Medical History Inserted Sucessfully.', 'success')
        return redirect(url_for('user_profile', username=session['id']))
    return render_template('IllnessInput.html', form=form)


@app.route('/deletecurrent/<string:illness>', methods=['POST'])
def delete_current(illness):
    username = session['id']
    key = session['key']
    userbase = user_ref.child(key)
    current_db = userbase.child('currentillness/' + illness)
    current_db.delete()
    flash('Current Illness deleted successfully', 'success')
    return redirect(url_for('user_profile', username=username))


@app.route('/deletepast/<string:illness>', methods=['POST'])
def delete_past(illness):
    username = session['id']
    key = session['key']
    userbase = user_ref.child(key)
    past_db = userbase.child('pastillness/' + illness)
    past_db.delete()
    flash('Past Illness deleted successfully', 'success')
    return redirect(url_for('user_profile', username=username))


# @app.route('/connect')
# def connect():
#     userbase = user_ref.get()
#     keys = []
#     my_list = []
#     common = []
#     user_dict = {}
#
#     for user in userbase.items():
#         if user[1]['username'] == session['id']:
#             my_sport = user[1]['sports']
#             for sport in my_sport:
#                 my_list.append(sport)
#
#         if user[1]['username'] != session['id']:
#             keys.append(user[0])
#             sport_list = []
#             user_sport = user[1]['sports']
#             for sport in user_sport:
#                 sport_list.append(sport)
#                 user_dict[user[0]] = sport_list
#
#     for u in keys:
#         this = user_dict[u]
#         for each in this:
#             if each in my_list:
#                 name = userbase[u]['username']
#                 c = Common(name)
#                 common.append(c)
#                 break
#
#     return redirect(url_for('my_friends'))


# @app.route('/deleteinterest/<string:sport>')
# def delete_interest(sport):
#     username = session['id']
#     key = session['key']
#     userbase = user_ref.child(key)
#     sports_db = userbase.child('sports/' + sport)
#     sports_db.delete()
#     flash('Interest deleted successfully', 'success')
#     return redirect(url_for('edit_profile'))

app.secret_key = 'secret123'

if __name__ == '__main__':
    app.run(port='80',debug=True)
