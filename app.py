from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from genElect.forms import *
from genElect.models import *
from genElect.utils.crypto import hash_password

#set app to flask instance
app = Flask(__name__, template_folder='genElect/templates')

#CONFIGURATIONS
#set secret key
app.config['SECRET_KEY'] = 'ec19370b6275506ac26a40c4e6c2e597'
#sqlite uri
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///genelect.db'


#setup database
db = SQLAlchemy(app)
migrate = Migrate(app, db)


#EXAMPLE POSTS (to be notifications)
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
    #ONLY ALLOW ACCESS IF ADMIN ACCOUNT
    form = CreateUserForm()
    if form.validate_on_submit():
        ##TO FIX
        #hash password for storage 
        # hashed_pw = hash_password(form.password.data)
        # new_user = Users(username=form.username.data, full_name=form.full_name.data, email=form.email.data, password=hashed_pw)
        # #add user to database and commit changes
        # db.session.add(new_user)
        # db.session.commit()
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

#Elective Creator Page (TESTING ROUTE)
@app.route("/elective", methods=['GET', 'POST'])
def createelective():
    form = CreateElectiveForm()
    if form.validate_on_submit():
        flash(f"Elective {form.name.data} created!", 'success')
        return redirect(url_for('index'))
    
    return render_template('createelective.html', title='Create', form=form)


#CONTACT PAGE
@app.route("/contactus")
@app.route("/contact")
def contact():
    return render_template('contact.html')



if __name__ == '__main__':
    app.run(debug=True) #start app in debug mode