from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, current_user
from genElect.forms import *
from genElect.models import *
from genElect.utils.crypto import hash_password, verify_password

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
db.create_all()

#LOGIN MANAGER
login_manager = LoginManager(app)

#DECORATOR FOR LoginManager user_loader
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


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
        #hash password for storage 
        hashed_pw = hash_password(form.password.data)
        new_user = Users(username=form.username.data, full_name=form.full_name.data, email=form.email.data, password=form.password.data)
        
        #add user to database and commit changes
        db.session.add(new_user)
        db.session.commit()
        flash(f"User {form.username.data} created", 'success')
        return redirect(url_for('createuser'))
    
    return render_template('createuser.html', title='Create User', form=form)


#LOGIN PAGE
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first() #login with username for now
        if user and form.password.data == user.password:
            login_user(user, remember=form.remember.data)
            flash(f"User {form.username.data} login successful!", 'success')
            return redirect(url_for('index'))
        else:
            flash("Login failed, try again", 'danger')
    
    return render_template('login.html', title='Login', form=form)

#Elective Creator Page (TESTING ROUTE)
@app.route("/createelective", methods=['GET', 'POST'])
def createelective():
    if current_user.is_authenticated and current_user.username == "admin":
        form = CreateElectiveForm()
        if form.validate_on_submit():
            flash(f"Elective {form.name.data} created!", 'success')
            return redirect(url_for('index'))
        return render_template('createelective.html', title='Create', form=form)

    else:
        return render_template('denied.html')


#ACCOUNT PAGE
@app.route("/account")
def account():
    if current_user.is_authenticated and current_user.username == "admin":
        return render_template('account.html')
    else:
        return render_template('denied.html')


#ADMIN PAGE
@app.route("/admin")
def admin():
    if current_user.is_authenticated and current_user.username == "admin":
        return render_template('admin.html')
    else:
        return render_template('denied.html')


#CONTACT PAGE
@app.route("/contactus")
@app.route("/contact")
def contact():
    return render_template('contact.html')


#LOGOUT ROUTE
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True) #start app in debug mode