from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, current_user

#set app to flask instance
app = Flask(__name__, template_folder='templates')

#CONFIGURATIONS
#set secret key
app.config['SECRET_KEY'] = 'ec19370b6275506ac26a40c4e6c2e597'
#sqlite uri
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../genelect.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BASEDIR'] = '.'
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

from genElect.models import Notifications
from genElect.models import Users
from genElect.models import Electives
from genElect.models import Offerings
from genElect.models import Registrations

from genElect.forms import *

#INDEX PAGE
@app.route("/")
@app.route("/home")
@app.route("/index")
def index():
    notifications = Notifications.query.all()
    notifications.reverse()
    return render_template('index.html', notifications=notifications)


#ABOUT PAGE
@app.route("/about")
def about():
    return render_template('about.html', title='About')


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


#ACCOUNT PAGE
@app.route("/account", methods=['GET', 'POST'])
def account():
    if current_user.is_authenticated:
        return render_template('account.html', title='Account')
    else:
        flash("Please login first", 'info')
        return redirect(url_for('login'))


#ADMIN PAGE
@app.route("/admin")
def admin():
    if current_user.is_authenticated and current_user.role == "admin":
        return render_template('admin.html')
    else:
        return render_template('denied.html')


#### USERS ####

#ADMIN CREATE USER PAGE
@app.route("/createuser", methods=['GET', 'POST'])
def createuser():
    #ONLY ALLOW ACCESS IF ADMIN ACCOUNT
    if current_user.is_authenticated and current_user.role == "admin":
        form = CreateUserForm()
        if form.validate_on_submit():
            new_user = Users(username=form.username.data, full_name=form.full_name.data, role=form.role.data, email=form.email.data, password=form.password.data)
            
            #add user to database and commit changes
            db.session.add(new_user)
            db.session.commit()
            flash(f"User {form.username.data} created", 'success')
            return redirect(url_for('createuser'))
        return render_template('createuser.html', title='Create User', form=form)
    
    else:
        return render_template('denied.html')


#ADMIN ALL USERS PAGE
@app.route("/allusers")
def allusers():
    if current_user.is_authenticated and current_user.role == "admin":
        users = Users.query.all()
        return render_template('allusers.html', users=users)
    else:
        return render_template('denied.html')

#ADMIN EDIT USER BY USER_ID
@app.route("/user/<user_id>", methods=['GET', 'POST'])
@app.route("/edituser/<user_id>", methods=['GET', 'POST'])
def edituser(user_id):
    if current_user.is_authenticated and current_user.role == "admin":
        user = Users.query.filter_by(id=int(user_id)).first()
        if user:
            form = UpdateUserForm()
            if form.validate_on_submit():
                user.username = form.username.data
                user.full_name = form.full_name.data
                user.email = form.email.data
                user.role = form.role.data
                db.session.commit()
                flash("Account Info Updated", 'success')
                return redirect(f'/user/{user_id}')
            elif request.method == 'GET':
                form.full_name.data = user.full_name
                form.email.data = user.email
                form.username.data = user.username
                form.role.data = user.role
            return render_template('edituser.html', user=user, form=form, title="User Edit")
        else:
            return redirect(url_for('index'))
    else:
        return render_template('denied.html')


#ADMIN DELETE USER BY USER ID
@app.route("/deleteuser/<user_id>")
@app.route("/user/<user_id>/delete")
def deleteuser(user_id):
    if current_user.is_authenticated and current_user.role == "admin":
        user = Users.query.filter_by(id=user_id).first()
        if user and user.username != "admin": #make sure not to delete admin
            db.session.delete(user)
            db.session.commit()
            flash("User Deleted", 'info')
            return redirect('/allusers')
        else:
            return render_template('notfound.html')
    else:
        return render_template('denied.html')

#### END OF USERS ####



#### ELECTIVES ####

#Elective Creator Page (TESTING ROUTE)
@app.route("/createelective", methods=['GET', 'POST'])
def createelective():
    if current_user.is_authenticated and current_user.role == "admin":
        form = ElectiveForm()
        if form.validate_on_submit():
            new_elective = Electives(name=form.name.data, description=form.description.data, prerequisites=form.prerequisites.data)
            db.session.add(new_elective)
            db.session.commit()
            flash(f"Elective {form.name.data} created!", 'success')
            return redirect(url_for('createelective'))
        return render_template('createelective.html', title='Create', form=form)

    else:
        return render_template('denied.html')

#ADMIN ALL ELECTIVES PAGE
@app.route("/allelectives")
def allelectives():
    if current_user.is_authenticated and current_user.role == "admin":
        electives = Electives.query.all()
        return render_template('allelectives.html', electives=electives, title="Electives")
    else:
        return render_template('denied.html')


#ADMIN EDIT ELECTIVE BY ELECTIVE_ID
@app.route("/elective/<elective_id>", methods=['GET', 'POST'])
@app.route("/editelective/<elective_id>", methods=['GET', 'POST'])
def editelective(elective_id):
    if current_user.is_authenticated and current_user.role == "admin":
        elective = Electives.query.filter_by(id=int(elective_id)).first()
        if elective:
            form = ElectiveForm()
            if form.validate_on_submit():
                elective.name = form.name.data
                elective.description = form.description.data
                elective.prerequisites = form.prerequisites.data
                db.session.commit()
                flash("Elective Info Updated", 'success')
                return redirect(f'/elective/{elective_id}')
            elif request.method == 'GET':
                form.name.data = elective.name
                form.description.data = elective.description
                form.prerequisites.data = elective.prerequisites
            return render_template('editelective.html', elective=elective, form=form, title="Elective Edit")
        else:
            return render_template('notfound.html')
    else:
        return render_template('denied.html')

#ADMIN DELETE ELECTIVE BY ELECTIVE ID
@app.route("/deleteelective/<elective_id>")
@app.route("/elective/<elective_id>/delete")
def deleteelective(elective_id):
    if current_user.is_authenticated and current_user.role == "admin":
        elective = Electives.query.filter_by(id=elective_id).first()
        if elective:
            db.session.delete(elective)
            db.session.commit()
            flash("Elective Deleted", 'info')
            return redirect('/allelectives')
        else:
            return render_template('notfound.html')
    else:
        return render_template('denied.html')

#### END OF ELECTIVES ####




#### OFFERINGS ####

#ALL OFFERINGS PAGE
@app.route("/allofferings")
def allofferings():
    offerings = Offerings.query.all()
    return render_template('allofferings.html', offerings=offerings, title="Offerings")

#ADMIN CREATE NEW OFFERING
#Elective Creator Page (TESTING ROUTE)
@app.route("/createoffering", methods=['GET', 'POST'])
def createoffering():
    if current_user.is_authenticated and (current_user.role == "admin" or current_user.role == "instructor"):
        form = OfferingForm()
        choices = []
        electives = Electives.query.all()
        for elective in electives:
            choices.append((str(elective.id), elective.name))
        form.elective.choices = choices
        if form.validate_on_submit():
            elective = Electives.query.filter_by(id=int(form.elective.data)).first()
            new_offering = Offerings(building=form.building.data, room=form.room.data, instructor=form.instructor.data, capacity=form.capacity.data, elective=elective, period_start=int(form.period_start.data), period_length=int(form.period_length.data))
            db.session.add(new_offering)
            db.session.commit()
            flash(f"Offering created!", 'success')
            return redirect(url_for('createoffering'))
        return render_template('createoffering.html', title='Create Offering', form=form)

    else:
        return render_template('denied.html')


#ADMIN EDIT OFFERING BY OFFERING
@app.route("/offering/<offering_id>", methods=['GET', 'POST'])
@app.route("/editoffering/<offering_id>", methods=['GET', 'POST'])
def editoffering(offering_id):
    if current_user.is_authenticated and current_user.role == "admin":
        offering = Offerings.query.filter_by(id=int(offering_id)).first()
        if offering:
            form = OfferingForm()
            choices = []
            electives = Electives.query.all()
            for elective in electives:
                choices.append((str(elective.id), elective.name))
            form.elective.choices = choices
            if form.validate_on_submit():
                elective = Electives.query.filter_by(id=int(form.elective.data)).first()
                offering.elective = elective
                offering.building = form.building.data
                offering.room = form.room.data
                offering.instructor = form.instructor.data
                offering.capacity = form.capacity.data
                offering.period_start = int(form.period_start.data)
                offering.period_length = int(form.period_length.data)
                db.session.commit()
                flash("Offering Info Updated", 'success')
                return redirect(f'/offering/{offering_id}')
            elif request.method == 'GET':
                form.elective.data = str(offering.elective.id)
                form.building.data = offering.building
                form.room.data = offering.room
                form.instructor.data = offering.instructor
                form.capacity.data = offering.capacity
                form.period_start.data = str(offering.period_start)
                form.period_length.data = str(offering.period_length)
            return render_template('editoffering.html', offering=offering, form=form, title="Offering Edit")
        else:
            return render_template('notfound.html')
    else:
        return render_template('denied.html')


#ADMIN DELETE ELECTIVE BY ELECTIVE ID
@app.route("/deleteoffering/<offering_id>")
@app.route("/offering/<offering_id>/delete")
def deleteoffering(offering_id):
    if current_user.is_authenticated and current_user.role == "admin":
        offering = Offerings.query.filter_by(id=offering_id).first()
        if offering:
            db.session.delete(offering)
            db.session.commit()
            flash("Offering Deleted", 'info')
            return redirect('/allofferings')
        else:
            return render_template('notfound.html')
    else:
        return render_template('denied.html')

#### END OF OFFERINGS ####



#### NOTIFICATIONS ####

#ADMIN Notification Creator (new posts on homepage)
@app.route("/createpost", methods=['GET', 'POST'])
@app.route("/createnotification", methods=['GET', 'POST'])
def createnotification():
    if current_user.is_authenticated and current_user.role == "admin":
        form = NotificationForm()
        if form.validate_on_submit():
            new_post = Notifications(title=form.title.data, notification=form.notification.data)
            db.session.add(new_post)
            db.session.commit()
            flash(f"Notification {form.title.data} created!", 'success')
            return redirect(url_for('admin'))
        return render_template('createnotification.html', title='New Notification', form=form)

    else:
        return render_template('denied.html')

#ADMIN ALL NOTIFICATIONS PAGE
@app.route("/allnotifications")
def allnotifications():
    if current_user.is_authenticated and current_user.role == "admin":
        notifications = Notifications.query.all()
        return render_template('allnotifications.html', notifications=notifications, title="Notifications")
    else:
        return render_template('denied.html')


#ADMIN EDIT NOTIFICATION BY NOTIFICATION_ID
@app.route("/notification/<notification_id>", methods=['GET', 'POST'])
@app.route("/editnotification/<notification_id>", methods=['GET', 'POST'])
def editnotification(notification_id):
    if current_user.is_authenticated and current_user.role == "admin":
        notification = Notifications.query.filter_by(id=int(notification_id)).first()
        if notification:
            form = NotificationForm()
            if form.validate_on_submit():
                notification.title = form.title.data
                notification.notification = form.notification.data
                db.session.commit()
                flash("Notification Updated", 'success')
                return redirect(f'/notification/{notification_id}')
            elif request.method == 'GET':
                form.title.data = notification.title
                form.notification.data = notification.notification
            return render_template('editnotification.html', notification=notification, form=form, title="Notification Edit")
        else:
            return render_template('notfound.html')
    else:
        return render_template('denied.html')


#ADMIN DELETE NOTIFICATION BY NOTIFICATION ID
@app.route("/deletenotification/<notification_id>")
@app.route("/notification/<notification_id>/delete")
def deletenotification(notification_id):
    if current_user.is_authenticated and current_user.role == "admin":
        notification = Notifications.query.filter_by(id=notification_id).first()
        if notification:
            db.session.delete(notification)
            db.session.commit()
            flash("Notification Deleted", 'info')
            return redirect('/index')
        else:
            return render_template('notfound.html')
    else:
        return render_template('denied.html')

#### END OF NOTIFICATIONS ####



#### STUDENT PAGES ####

#STUDENTS VIEWING ELECTIVES
@app.route("/electives") #FOR STUDENT USE
@app.route("/offerings") #FOR STUDENT USE
def electives():
    if current_user.is_authenticated:
        offerings = Offerings.query.all()
        return render_template('studentelectives.html', offerings=offerings)
    else:
        flash("Please login first", 'info')
        return redirect(url_for('login'))


#STUDENTS VIEWING THEIR SCHEDULE
@app.route("/schedule") #FOR STUDENT USE
def schedule():
    if current_user.is_authenticated:
        registrations = current_user.registrations #grab all user registrations
        return render_template('schedule.html', registrations=registrations)
    else:
        flash("Please login first", 'info')
        return redirect(url_for('login'))



#STUDENTS REGISTER FOR AN OFFERING
@app.route("/register/<offering_id>")
def register(offering_id):
    if current_user.is_authenticated:
        offering = Offerings.query.filter_by(id=offering_id).first()
        if offering:
            new_registration = Registrations(user_id=current_user.id, offering_id=offering_id)
            db.session.add(new_registration)
            db.session.commit()
            flash("Elective Registration Successful", 'success')
            return redirect(url_for('electives'))
        else:
            return render_template('notfound.html')
    else:
        flash("Please login first", 'info')
        return redirect(url_for('login'))

#### END OF STUDENTS PAGES ####


#CONTACT PAGE
@app.route("/contactus")
@app.route("/contact")
def contact():
    return render_template('contact.html')


#LOGOUT ROUTE
@app.route("/logout")
def logout():
    logout_user()
    flash("Logout successful", 'success')
    return redirect(url_for('index'))

