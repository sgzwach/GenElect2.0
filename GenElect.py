from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import CreateUserForm, LoginForm

#set app to flask instance
app = Flask(__name__)

#CONFIGURATIONS
#set secret key
app.config['SECRET_KEY'] = 'ec19370b6275506ac26a40c4e6c2e597'
#sqlite uri
app.config['SQLALCHEMY_DATABSE_URI'] = 'sqlite:///genelect.db'


#setup database
db = SQLAlchemy(app)

#MODELS
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)


#EXAMPLE POSTS
posts = [
    {
        'author': 'admin',
        'title': 'New Elective',
        'content': 'Check out the new elective!',
        'date_posted': 'March 12, 2019'
    },
    {
        'author': 'admin',
        'title': 'Welcome!',
        'content': 'We are happy to announce a new site!',
        'date_posted': 'March 11, 2019'
    }
]


#INDEX PAGE
@app.route("/")
@app.route("/home")
@app.route("/index")
def index():
    return render_template('index.html', posts=posts)


#ABOUT PAGE
@app.route("/about")
def about():
    return render_template('about.html', title='About')


#CREATE USER PAGE
@app.route("/createuser", methods=['GET', 'POST'])
def createuser():
    form = CreateUserForm()
    if form.validate_on_submit():
        flash(f"User {form.username.data} created", 'success')
        return redirect(url_for('createuser'))
    return render_template('createuser.html', title='Create User', form=form)


#LOGIN PAGE
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'admin' and form.password.data == 'Password1!':
            flash(f"User {form.username.data} login successful!", 'success')
            return redirect(url_for('index'))
        else:
            flash("Login failed, try again", 'danger')
    return render_template('login.html', title='Login', form=form)


#CONTACT PAGE
@app.route("/contactus")
@app.route("/contact")
def contact():
    return render_template('contact.html')



if __name__ == '__main__':
    app.run(debug=True) #start app in debug mode