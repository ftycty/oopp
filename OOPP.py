from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/index')
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

@app.route('/workouts')
def workouts():
    return render_template('workouts.html')


if __name__ == '__main__':
    app.run()
