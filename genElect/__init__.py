from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, current_user
import datetime #for registration time set

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
from genElect.models import Completions
from genElect.models import Prerequisites
from genElect.models import Cores
from genElect.models import CoreRegistrations

from genElect.forms import *

global registration_start_time
global egistration_end_time

registration_start_time = "00:00:00"
registration_end_time = "23:59:59"

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
        #now try email if the username didn't work
        if not user:
            user = Users.query.filter_by(email=form.username.data).first()

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


#ADMIN STAT PAGE
@app.route("/stats")
def stats():
    if current_user.is_authenticated and current_user.role == "admin":
        empty = []
        full = []

        for offering in Offerings.query.all():
            if offering.capacity == 0:
                continue
            elif offering.current_count / offering.capacity <= 0.25:
                empty.append(offering)
            elif offering.current_count / offering.capacity >= 0.75:
                full.append(offering)
        return render_template('stats.html', empty=empty, full=full)
    else:
        return render_template('denied.html')


#ADMIN VIEW STUDENTS THAT ARE NOT REGISTERED FOR ALL PERIODS
@app.route("/notregistered")
def notregistered():
    if current_user.is_authenticated and current_user.role == "admin":
        students_not_registered = []
        for user in Users.query.filter_by(role='student'):
            if len(user.registrations) < 3:
                students_not_registered.append(user)
        return render_template('notregistered.html', users=students_not_registered)
    else:
        return render_template('denied.html')


#ADMIN COMPLETE A SINGLE OFFERING
@app.route("/complete/<offering_id>")
def complete(offering_id):
    if current_user.is_authenticated and current_user.role == "admin":
        offering = Offerings.query.filter_by(id=offering_id).first()
        if not offering:
            flash('Offering not found to complete', 'danger')
            return redirect(url_for('allofferings'))
        else:
            #RESET THE STUDENT COUNT BEFORE COMPLETING THE OFFERING
            offering.current_count = 0
            for registration in offering.registrations:
                #LOOP THROUGH REGISTRATIONS FOR THIS OFFERING AND MAKE A COMPLETION AND DUMP THE REGISTRATION
                new_completion = Completions(elective_id=offering.elective_id, user_id=registration.user_id)
                db.session.add(new_completion)
                db.session.delete(registration)
            db.session.commit()
            flash('Offering completed', 'success')
            return redirect(url_for('allofferings'))
    else:
        return render_template('denied.html')


#ADMIN SET ALL REGESTRATIONS TO COMPLETIONS
@app.route("/completeall")
def completeall():
    if current_user.is_authenticated and current_user.role == "admin":
        registrations = Registrations.query.all()
        offerings = Offerings.query.all()
        for registration in registrations: #complete each registration
            completion = Completions(user_id=registration.user_id,elective_id=registration.offering.elective.id)
            db.session.delete(registration) #if we want to dump all registrations while completing them
            db.session.add(completion)

        for offering in offerings: #reset offering student count
            offering.current_count = 0 

        db.session.commit()
        flash(f"Registrations removed and Completions set", 'success')
        return redirect(url_for('admin'))
    else:
        return render_template('denied.html')

#ADMIN RESET REGISTRATIONS (complete should do this also)
# @app.route("/reset")
# def reset():
#     if current_user.is_authenticated and current_user.role == "admin":
#         #reset registrations
#         registrations = Registrations.query.all()
#         for registration in registrations:
#             db.session.delete(registration)

#         #set student count to 0 for all offerings
#         offerings = Offerings.query.all()
#         for offering in offerings:
#             offering.current_count = 0

#         db.session.commit()
#         flash(f"Registrations reset", 'success')
#         return redirect(url_for('admin'))
#     else:
#         return render_template('denied.html')


#ADMIN SET REGISTRATION TIME
@app.route("/settime", methods=['GET', 'POST'])
def settime():
    if current_user.is_authenticated and current_user.role == "admin":
        form = TimeSetForm()
        global registration_start_time
        global registration_end_time
        if form.validate_on_submit():
            registration_start_time = form.start_time.data
            registration_end_time = form.end_time.data
            flash("Registration time set", 'success')
            return redirect(f'settime')
        elif request.method == 'GET':
            form.start_time.data = registration_start_time
            form.end_time.data = registration_end_time
        return render_template('settime.html', title='Set Registration Time', form=form)
    else:
        return render_template('denied.html')


#### USERS ####

#ADMIN CREATE USER PAGE
@app.route("/createuser", methods=['GET', 'POST'])
def createuser():
    #ONLY ALLOW ACCESS IF ADMIN ACCOUNT
    if current_user.is_authenticated and current_user.role == "admin":
        form = UserForm()
        choices1 = [('-1', 'None')] #choices for period 1 cores
        choices2 = [('-1', 'None')] #choices for period 2 cores
        choices3 = [('-1', 'None')] #choices for period 3 cores

        cores = Cores.query.all()
        #correctly append cores to choices for the core dropdowns
        for core in cores:
            if core.core_period == 1:
                choices1.append((str(core.id),core.name))
            elif core.core_period == 2:
                choices2.append((str(core.id),core.name))
            else:
                choices3.append((str(core.id),core.name))

        #setting up choices and default data
        form.core1.choices = choices1 #set the choices
        form.core2.choices = choices2 #set the choices
        form.core3.choices = choices3 #set the choices

        if form.validate_on_submit():
            new_user = Users(username=form.username.data, full_name=form.full_name.data, role=form.role.data, email=form.email.data, password=form.password.data)

            #add user to database and commit changes
            db.session.add(new_user)
            try:
                db.session.commit()
                flash(f"User {form.username.data} created", 'success')
            except:
                flash("User creation failed, possibly from repeated user data", 'danger')
                return redirect(url_for('createuser'))

            #if the new user was a student we need to add the core registrations
            if new_user.role == "student":
                if form.core1.data != '-1':
                    new_reg1 = CoreRegistrations(user_id=new_user.id,core_id=int(form.core1.data))
                    db.session.add(new_reg1)
                if form.core2.data != '-1':
                    new_reg2 = CoreRegistrations(user_id=new_user.id,core_id=int(form.core2.data))
                    db.session.add(new_reg2)
                if form.core3.data != '-1':
                    new_reg3 = CoreRegistrations(user_id=new_user.id,core_id=int(form.core3.data))
                    db.session.add(new_reg3)

                try:
                    db.session.commit()
                    flash(f"User core registrations added", 'success')
                except:
                    flash("Failure occurred, could possibly come from repeated user data", 'danger')

            return redirect(url_for('createuser'))
        return render_template('createuser.html', title='Create User', form=form)
    
    else:
        return render_template('denied.html')


#ADMIN UPLOAD USER CSV FILE
@app.route('/uploadusers', methods=['GET', 'POST'])
def uploadusers():
    #ONLY ALLOW ACCESS IF ADMIN ACCOUNT
    if current_user.is_authenticated and current_user.role == "admin":
        if request.method == 'POST': #posting user file information
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file data found', 'danger')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file', 'danger')
                return redirect(request.url)
            if file: #if file data is found
                filename = file.filename
                users = file.readlines()
                for user in users:
                    user = user.decode().strip().split(',')
                    if len(user) != 8 and len(user) != 5:
                        flash("Bad user input", 'danger')
                    else:
                        new_user = Users(username=user[0],full_name=user[1],email=user[2],role=user[3],password=user[4])
                        db.session.add(new_user)

                        #just trying (to get the id for the user)
                        db.session.commit()

                        #now add core registrations based on the last id
                        if user[3] == "student":
                            for i in range(5,8):
                                new_core_registration = CoreRegistrations(user_id=new_user.id, core_id=int(user[i]))
                                db.session.add(new_core_registration)

                #try to commit the new users
                try:
                    db.session.commit()
                    flash("Users uploaded!", 'success')
                except:
                    flash("Something went wrong, unique value repeat?", 'danger')

                return redirect('/allusers')
        else:
            return render_template('uploadusers.html')
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
            form = UserForm()

            if user.role == "student":
                #setup for core registrations (note these are only really used for students)
                choices1 = [('-1',"None")] #choices for period 1 cores
                choices2 = [('-1',"None")] #choices for period 2 cores
                choices3 = [('-1',"None")] #choices for period 3 cores

                #loop through and get current registered cores

                #set defaults in case
                cur1 = -1
                cur2 = -1
                cur3 = -1

                for reg in user.core_registrations:
                    if reg.core.core_period == 1:
                        cur1 = reg.core.id
                    elif reg.core.core_period == 2:
                        cur2 = reg.core.id
                    else:
                        cur3 = reg.core.id
                
                cores = Cores.query.all()

                #correctly append cores to choices for the core dropdowns
                for core in cores:
                    if core.core_period == 1:
                        choices1.append((str(core.id),core.name))
                    elif core.core_period == 2:
                        choices2.append((str(core.id),core.name))
                    else:
                        choices3.append((str(core.id),core.name))

                #setting up choices and default data
                form.core1.choices = choices1 #set the choices
                form.core2.choices = choices2 #set the choices
                form.core3.choices = choices3 #set the choices

            else:
                form.core1.data = form.core2.data = form.core3.data = "0" 
            
            if form.validate_on_submit():
                if user.username != "admin":
                    if form.username.data == "admin":
                        flash("Username cannot be made admin", 'danger')
                    else:
                        user.username = form.username.data
                else:
                    if form.username.data != user.username:
                        flash("Admin username must not be changed", 'danger')

                user.full_name = form.full_name.data
                user.email = form.email.data

                #check role is changed to or from a student
                if form.role.data != user.role:
                    #changing from a student we must dump all core registrations and elective registrations
                    
                    if user.role == "student":
                        #remove all core registrations
                        for core in user.core_registrations:
                            db.session.delete(core)

                        #remove all elective registrations
                        for elective in user.registrations:
                            db.session.delete(elective)
                        
                        db.session.commit()

                    #make change insuring that admin account is not adjusted
                    if user.username != "admin":
                        user.role = form.role.data
                    else:
                        flash("Admin account does not allow role change", 'danger')

                #only make these student updates if there wasn't a role change also
                elif user.role == "student":
                    #check if core period 1 was changed or removed
                    if cur1 != int(form.core1.data):
                        #if the current registration wasn't empty we have to remove it
                        if cur1 != -1:
                            #find registration with core_id and user_id
                            corereg = CoreRegistrations.query.filter_by(user_id=user.id,core_id=cur1).first()
                            #check before deletion
                            if corereg:
                                db.session.delete(corereg)

                        #now add new registration if there should be one
                        if int(form.core1.data) != -1:
                            #otherwise create the new core registration
                            new_core_reg = CoreRegistrations(user_id=user.id,core_id=int(form.core1.data))
                            db.session.add(new_core_reg)


                    #check if core period 2 was changed or removed
                    if cur2 != int(form.core2.data):
                        #if the current registration wasn't empty we have to remove it
                        if cur2 != -1:
                            corereg = CoreRegistrations.query.filter_by(user_id=user.id,core_id=cur2).first()
                            #check before deletion
                            if corereg:
                                db.session.delete(corereg)

                        #now add new registration is there should be one
                        if int(form.core2.data) != -1:
                            #otherwise create the new core registration
                            new_core_reg = CoreRegistrations(user_id=user.id,core_id=int(form.core2.data))
                            db.session.add(new_core_reg)


                    #check if core period 3 was changed or removed
                    if cur3 != int(form.core3.data):
                        #if the current registration wasn't empty we have to remove it
                        if cur3 != -1:
                            corereg = CoreRegistrations.query.filter_by(user_id=user.id,core_id=cur3).first()
                            if corereg:
                                db.session.delete(corereg)

                        #now add new registration is there should be one
                        if int(form.core3.data) != -1:
                            #otherwise create the new core registration
                            new_core_reg = CoreRegistrations(user_id=user.id,core_id=int(form.core3.data))
                            db.session.add(new_core_reg)

                #check if the password was changed
                if form.password.data:
                    user.password = form.password.data
                    flash("New password set", 'success')
                #attempt to commit the changes
                try:
                    db.session.commit()
                except:
                    #catch if something went wrong on the commit
                    flash("Something went wrong, try again but confirm data input", 'danger')

                flash("Account Info Updated", 'success')
                return redirect(f'/user/{user_id}')

            elif request.method == 'GET':
                if user.role == "student":
                    form.core1.data = str(cur1) #set the current registered
                    form.core2.data = str(cur2) #set the current registered
                    form.core3.data = str(cur3) #set the current registered
                form.full_name.data = user.full_name
                form.email.data = user.email
                form.username.data = user.username
                form.role.data = user.role

            return render_template('edituser.html', user=user, form=form, title="User Edit")
        else:
            return render_template('notfound.html')
    else:
        return render_template('denied.html')


#ADMIN DELETE USER BY USER ID
@app.route("/deleteuser/<user_id>")
@app.route("/user/<user_id>/delete")
def deleteuser(user_id):
    if current_user.is_authenticated and current_user.role == "admin":
        user = Users.query.filter_by(id=user_id).first()
        if user: #make sure user is found
            if user.username == 'admin':
                #DON'T DELETE THE ADMIN USER
                flash("Cannot delete the admin user", 'danger')
                return redirect('/allusers')
            #WE HAVE TO DELETE THE REGISTRATIONS AND COMPLETIONS
            for registration in user.registrations:
                registration.offering.current_count -= 1
                db.session.delete(registration)
            for completion in user.completed_electives:
                db.session.delete(completion)

            #WE ALSO HAVE TO REMOVE ALL CORE REGISTRATIONS
            for core_registration in user.core_registrations:
                db.session.delete(core_registration)

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
    if current_user.is_authenticated and (current_user.role == "admin" or current_user.role == "instructor"):
        form = ElectiveForm()

        #CREATE THE PREREQ LIST CHOICES
        prereq_choices = [('-1','None')]
        electives = Electives.query.all()
        for elective in electives:
            prereq_choices.append((str(elective.id), elective.name))
        #SET THE PREREQ LIST
        form.prerequisites.choices = prereq_choices

        #IF FORM IS SUBMITTED AND VALID
        if form.validate_on_submit():
            new_elective = Electives(name=form.name.data, description=form.description.data, can_retake=form.can_retake.data)
            db.session.add(new_elective)
            #commit our new elective (have to do this to get new_elective's id)
            db.session.commit()
            #NOW ADD ALL PREREQUISITES THAT WERE SELECTED
            for pre in form.prerequisites.data:
                pre = int(pre)
                if pre > 0:
                    new_prerequisite = Prerequisites(elective_id=new_elective.id, prerequisite_elective_id=pre)
                    db.session.add(new_prerequisite)

            #commit our prereqs
            db.session.commit()
            flash(f"Elective {form.name.data} created!", 'success')
            return redirect(url_for('createelective'))
        return render_template('createelective.html', title='Create', form=form)

    else:
        return render_template('denied.html')

#ADMIN ALL ELECTIVES PAGE
@app.route("/allelectives")
def allelectives():
    if current_user.is_authenticated and (current_user.role == "admin" or current_user.role == "instructor"):
        electives = Electives.query.all()
        return render_template('allelectives.html', electives=electives, title="Electives")
    else:
        return render_template('denied.html')


#ADMIN EDIT ELECTIVE BY ELECTIVE_ID
@app.route("/elective/<elective_id>", methods=['GET', 'POST'])
@app.route("/editelective/<elective_id>", methods=['GET', 'POST'])
def editelective(elective_id):
    if current_user.is_authenticated and (current_user.role == "admin" or current_user.role == "instructor"):
        elective = Electives.query.filter_by(id=int(elective_id)).first()
        if elective:
            form = ElectiveForm()

            #CREATE THE PREREQ LIST CHOICES
            prereq_choices = [('-1','None')]
            electives = Electives.query.all()
            for e in electives:
                if elective != e:
                    prereq_choices.append((str(e.id), e.name))
            #SET THE PREREQ LIST
            form.prerequisites.choices = prereq_choices

            if form.validate_on_submit():
                elective.name = form.name.data
                elective.description = form.description.data
                elective.can_retake = form.can_retake.data

                #NOW UPDATE ALL PREREQUISITES THAT WERE SELECTED
                for prerequisite in elective.prerequisites:
                    db.session.delete(prerequisite)
                for pre in form.prerequisites.data:
                    pre = int(pre)
                    if pre > 0:
                        new_prerequisite = Prerequisites(elective_id=elective.id, prerequisite_elective_id=pre)
                        db.session.add(new_prerequisite)

                db.session.commit()
                flash("Elective Info Updated", 'success')
                return redirect(f'/elective/{elective_id}')
            
            elif request.method == 'GET':
                form.name.data = elective.name
                form.description.data = elective.description
                form.can_retake.data = elective.can_retake
                #CREATE THE DATA LIST OF CHOICES
                picked = []
                for p in elective.prerequisites:
                    picked.append(str(p.prerequisite_elective_id))
                #SET THE DATA LIST OF PICKED PREREQS
                if picked:
                    form.prerequisites.data = picked
                else: #if there are no selected prerequisites show 'None' selected
                    form.prerequisites.data = ['-1']

            return render_template('editelective.html', elective=elective, form=form, title="Elective Edit")
        else:
            return render_template('notfound.html')
    else:
        return render_template('denied.html')

#ADMIN DELETE ELECTIVE BY ELECTIVE ID
@app.route("/deleteelective/<elective_id>")
@app.route("/elective/<elective_id>/delete")
def deleteelective(elective_id):
    if current_user.is_authenticated and (current_user.role == "admin" or current_user.role == "instructor"):
        elective = Electives.query.filter_by(id=elective_id).first()
        if elective:
            #DELETE PREREQ INSTANCES FOR ELECTIVE
            for pre in elective.prerequisites:
                db.session.delete(pre)

            #DELETE PREREQS WHERE ELECTIVE IS THE PREREQ
            prerequisites_to_delete = Prerequisites.query.filter_by(prerequisite_elective_id=elective.id)
            for pre in prerequisites_to_delete:
                db.session.delete(pre)

            #DELETE COMPLETIONS FOR AN ELECTIVE
            for completion in elective.completed_users:
                db.session.delete(completion)

            #DELETE ELECTIVE OFFERINGS
            for offering in elective.offerings:
                for registration in offering.registrations:
                    db.session.delete(registration)
                db.session.delete(offering)
            
            #SAVE DELETIONS
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
    offerings = Offerings.query.order_by(Offerings.elective_id).all()
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
            #elective = Electives.query.filter_by(id=int(form.elective.data)).first()
            new_offering = Offerings(building=form.building.data, room=form.room.data, instructor=form.instructor.data, capacity=form.capacity.data, current_count=0, elective_id=int(form.elective.data), period_start=int(form.period_start.data), period_length=int(form.period_length.data))
            db.session.add(new_offering)
            db.session.commit()
            flash(f"Offering created!", 'success')
            return redirect(url_for('allofferings'))

        elif request.method == 'GET':
            #IF TEMPLATED FILL THE FIELDS WITH THE TEMPLATE
            template_id = request.args.get('offering_template_id')
            if template_id:
                template_offering = Offerings.query.filter_by(id=template_id).first()
                if not template_offering: #if the offering template is not found
                    flash("Offering template not found", 'danger')
                    return redirect(url_for('allofferings'))
                else: #fill the new elective with the template information 
                    form.building.data = template_offering.building
                    form.room.data = template_offering.room
                    form.instructor.data = template_offering.instructor
                    form.capacity.data = template_offering.capacity
                    form.elective.data = str(template_offering.elective_id)
                    form.period_start.data = str(template_offering.period_start)
                    form.period_length.data = str(template_offering.period_length)

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
            registrations_to_delete = Registrations.query.filter_by(offering_id=offering.id) #dump registrations that involve the offering that is deleted
            for registration in registrations_to_delete:
                db.session.delete(registration)
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


#CAMP SCHEDULE PAGE
@app.route("/campschedule")
def campschedule():
    return render_template('campschedule.html')


#### STUDENT PAGES ####

#STUDENTS VIEWING ELECTIVES
@app.route("/electives") #FOR STUDENT USE
@app.route("/offerings") #FOR STUDENT USE
def electives():
    try:
        period = int(request.args.get('period'))
    except:
        period = 0
    
    search = request.args.get('search')

    if search is None:
        search = ""

    #QUERY FOR WHAT OFFERINGS TO SHOW
    all_offerings = Offerings.query.order_by(Offerings.elective_id).all()
    offerings = []
    for offering in all_offerings:
        if (period == 0 or offering.period_start == period) and (search == "" or search.lower() in offering.elective.name.lower()):
            offerings.append(offering)

    registered = [] #build out list of registered offerings based on user registrations
    if current_user.is_authenticated:
        registrations = current_user.registrations
        for registration in registrations:
            registered.append(registration.offering)
    return render_template('studentelectives.html', offerings=offerings, registered=registered, Electives=Electives, period=period)



#STUDENTS VIEWING THEIR SCHEDULE
@app.route("/schedule") #FOR STUDENT OR ADMIN USE
def schedule():
    if current_user.is_authenticated:
        if current_user.role == 'admin' or current_user.role == 'instructor':
            user_id = request.args.get('user_id')
            user = Users.query.filter_by(id=user_id).first()
            if not user:
                flash("User schedule not found", 'danger')
                return redirect(url_for('allusers'))   
        else:
            user = current_user
            user_id = user.id

        registrations = user.registrations #grab all user registrations
        registered = [] #to build out registered offerings

        #WEIRD WAY TO SORT REGISTERED OFFERINGS SINCE sorted() DOESN'T WORK ON TYPE OFFERINGS
        #TODO: BETTER SORTING MECHANISM
        for registration in registrations:
            if registration.offering.period_start == 1:
                registered.append(registration.offering)
        for registration in registrations:
            if registration.offering.period_start == 2:
                registered.append(registration.offering)
        for registration in registrations:
            if registration.offering.period_start == 3:
                registered.append(registration.offering)

        #SAME WEIRD WAY TO SORT CORE REGISTRATIONS
        #TODO: REALLY FIX THIS
        core_registrations = []
        for core_reg in user.core_registrations:
            if core_reg.core.core_period == 1:
                core_registrations.append(core_reg)
        for core_reg in user.core_registrations:
            if core_reg.core.core_period == 2:
                core_registrations.append(core_reg)
        for core_reg in user.core_registrations:
            if core_reg.core.core_period == 3:
                core_registrations.append(core_reg)

        return render_template('schedule.html', registered=registered, core_registrations=core_registrations, user=user)

    else:
        flash("Please login first", 'info')
        return redirect(url_for('login'))


#STUDENTS VIEWING THEIR COMPLETIONS
@app.route("/completions") #FOR STUDENT OR ADMIN USE
def completions():
    if current_user.is_authenticated:
        user = current_user
        completions = user.completed_electives #grab all user completions

        return render_template('completions.html', completions=completions)

    else:
        flash("Please login first", 'info')
        return redirect(url_for('login'))


#STUDENTS REGISTER FOR AN OFFERING
@app.route("/register/<offering_id>")
def register(offering_id):
    currTime = datetime.datetime.now().strftime("%H:%M:%S")
    if currTime < registration_start_time or currTime > registration_end_time:
        flash(f"It is {currTime} and Registration time is from {registration_start_time} to {registration_end_time}", 'danger')
        return redirect(url_for('electives'))

    if current_user.is_authenticated:
        #make sure user isn't admin or instructor since they shouldn't be registering
        if current_user.role == "admin" or current_user.role == "instructor":
            flash("Only students can register for electives", 'danger')
            return redirect(url_for('allelectives'))

        #check if already registered for (won't happen unless going by url)
        reg_check = Registrations.query.filter_by(user_id=current_user.id, offering_id=offering_id).first()
        if reg_check:
            flash("Elective already registered for", 'danger')
            return redirect(url_for('electives'))

        offering = Offerings.query.filter_by(id=offering_id).first()
        if not offering:
            flash("Elective not found for registration", 'danger')
            return redirect(url_for('electives'))

        #check if already completed elective type
        completion = Completions.query.filter_by(user_id=current_user.id, elective_id=offering.elective.id).first()
        if completion and offering.elective.can_retake == False: #if they can't retake the elective
            flash("Elective type already completed", 'danger')
            return redirect(url_for('electives'))

        #check if registered for same time period or elective
        for registration in current_user.registrations:
            if registration.offering.period_start == offering.period_start:
                flash("Elective time conflict", 'danger')
                return redirect(url_for('electives'))
            if registration.offering.elective == offering.elective and offering.elective.can_retake == False:
                flash("Already registered for that elective type", 'danger')
                return redirect(url_for('electives'))
                
        #check if completed prerequisites (using both completed and other registrations that are before selected elective)
        for p in offering.elective.prerequisites:
            #CHECK ELECTIVES THAT HAVE BEEN COMPLETED
            #QUERY FOR COMPLETION WITH USER_ID AND THE PREREQUISITE_ELECTIVE_ID
            p_check = Completions.query.filter_by(user_id=current_user.id, elective_id=p.prerequisite_elective_id).first()
            #CHECK ELECTIVES REGISTERED NOW THAT WILL TAKE PLACE BEFORE THIS ELECTIVE 
            r_check = False
            for registration in current_user.registrations:
                if registration.offering.elective_id == p.prerequisite_elective_id and registration.offering.period_start < offering.period_start:
                    r_check = True
            if not p_check and not r_check:
                flash("Elective prerequisites not completed", 'danger')
                return redirect(url_for('electives'))

        if offering:
            if offering.current_count >= offering.capacity: #check if offering is full
                flash("Elective full", 'danger')
                return redirect(url_for('electives'))
            #if everything passed, register
            new_registration = Registrations(user_id=current_user.id, offering_id=offering_id)
            offering.current_count += 1
            db.session.add(new_registration)
            db.session.commit()
            flash("Elective Registration Successful", 'success')
            return redirect(url_for('electives'))

    else:
        flash("Please login first", 'info')
        return redirect(url_for('login'))


#STUDENTS DROP AN ELECTIVE THEY HAVE REGISTERED FOR
@app.route("/drop/<offering_id>")
def drop(offering_id):
    #TO GRAB WHERE TO RETURN TO
    back = request.args.get('back')
    if current_user.is_authenticated:
        #make sure user isn't admin or instructor since they shouldn't be dropping
        if current_user.role == "admin" or current_user.role == "instructor":
            user_id = request.args.get('user_id')
            registration = Registrations.query.filter_by(user_id=user_id,offering_id=offering_id).first()
            if not registration:
                flash("Registration not found", 'danger')
                return redirect(url_for('attendance',offering_id=offering_id))
            else:
                student_name = registration.user.full_name
                registration.offering.current_count -= 1
                db.session.delete(registration)
                db.session.commit()
                flash(f"{student_name} dropped", 'success')
                #IF WE CAME FROM SCHEDULE RETURN THERE
                if back == 'schedule':
                    return redirect(f'/schedule?user_id={user_id}')
                #OTHERWISE RETURN BACK TO THE ATTENDANCE PAGE
                else:
                    return redirect(url_for('attendance',offering_id=offering_id))

        registration = Registrations.query.filter_by(offering_id=offering_id, user_id=current_user.id).first()
        if registration:
            if current_user.id == registration.user_id or current_user.role == "admin":
                #DELETE OTHER REGISTRATIONS THAT RELIED ON THIS AS A PREREQ
                for other_registration in current_user.registrations:
                    if other_registration == registration:
                        continue
                    for pre_req in other_registration.offering.elective.prerequisites:
                        if registration.offering.elective_id == pre_req.prerequisite_elective_id: #if we are deleting a prereq that was required
                            other_registration.offering.current_count -= 1
                            db.session.delete(other_registration)
                            break

                registration.offering.current_count -= 1
                db.session.delete(registration)
                db.session.commit()
                flash("Elective and other reliant electives succesfully dropped", 'info')
                #RETURN TO SCHEDULE IF WE CAME FROM THERE
                if back == 'schedule':
                    return redirect(url_for('schedule'))
                #OTHERWISE RETURN BACK TO ELECTIVES
                else:
                    return redirect(url_for('electives'))

            else:
                return render_template('denied.html')
        else:
            flash("Elective not found for drop", 'danger')
            return redirect(url_for('electives'))
    else:
        flash("Please login first", 'info')
        return redirect(url_for('login'))

#### END OF STUDENTS PAGES ####



#### INSTRUCTOR PAGES ####

#INSTRUCTORS VIEW OFFERING REGISTERED STUDENTS (ATTENDANCE/ROLLCALL)
@app.route("/attendance/<offering_id>")
@app.route("/roll/<offering_id>")
def attendance(offering_id):
    if current_user.is_authenticated and (current_user.role == "admin" or current_user.role == "instructor"):
        offering = Offerings.query.filter_by(id=offering_id).first()
        if offering:
            registrations = Registrations.query.filter_by(offering_id=offering.id)
            return render_template('roll.html', registrations=registrations, title='Roll')
        else:
            return render_template('notfound.html')
    else:
        return render_template('denied.html')



#### END OF INSTRUCTOR PAGES ####


#### CORE CREATION EDITING AND DELETION ####

#ADMIN ALL CORES PAGE
@app.route("/allcores")
def allcores():
    if current_user.is_authenticated and (current_user.role == "admin" or current_user.role == "instructor"):
        cores = Cores.query.all()
        return render_template('allcores.html', cores=cores, title="Cores")
    else:
        return render_template('denied.html')

#CORE Creator Page
@app.route("/createcore", methods=['GET', 'POST'])
def createcore():
    if current_user.is_authenticated and current_user.role == "admin":
        form = CoreForm()

        #IF FORM IS SUBMITTED AND VALID
        if form.validate_on_submit():
            #create the new core
            new_core = Cores(name=form.name.data, description=form.description.data, instructor=form.instructor.data, core_period=int(form.core_period.data), building=form.building.data, room=form.room.data)
            db.session.add(new_core)
            #commit our new core
            db.session.commit()

            flash(f"Core {new_core.name} created!", 'success')
            return redirect(url_for('allcores'))
        return render_template('createcore.html', title='Create', form=form)

    else:
        return render_template('denied.html')



#ADMIN EDIT CORE BY CORE_ID
@app.route("/core/<core_id>", methods=['GET', 'POST'])
@app.route("/editcore/<core_id>", methods=['GET', 'POST'])
def editcore(core_id):
    if current_user.is_authenticated and (current_user.role == "admin" or current_user.role == "instructor"):
        core = Cores.query.filter_by(id=int(core_id)).first()
        if core:
            #create the core form
            form = CoreForm()

            if form.validate_on_submit():
                #update the core information
                core.name = form.name.data
                core.description = form.description.data
                core.instructor = form.instructor.data
                core.building = form.building.data
                core.room = form.room.data
                core.core_period = form.core_period.data

                #commit the changes
                db.session.commit()
                flash("Core Info Updated", 'success')
                return redirect(f'/core/{core_id}')
            
            elif request.method == 'GET':
                form.name.data = core.name
                form.description.data = core.description
                form.instructor.data = core.instructor
                form.building.data = core.building
                form.room.data = core.room
                form.core_period.data = core.core_period

            return render_template('editcore.html', core=core, form=form, title="Core Edit")
        else:
            return render_template('notfound.html')
    else:
        return render_template('denied.html')


#ADMIN DELETE CORE BY CORE_ID
@app.route("/deletecore/<core_id>")
@app.route("/core/<core_id>/delete")
def deletecore(core_id):
    if current_user.is_authenticated and current_user.role == "admin":
        core = Cores.query.filter_by(id=core_id).first()
        if core:
            #WE NEED TO REMOVE ALL REGISTRATIONS FOR THE CORE COURSE THAT WE ARE ABOUT TO DELETE
            for core_registration in core.registrations:
                db.session.delete(core_registration)

            db.session.delete(core)
            db.session.commit()
            flash("Core Deleted", 'info')
            return redirect('/allcores')
        else:
            return render_template('notfound.html')
    else:
        return render_template('denied.html')




#GET ROLL BY CORE ID
@app.route("/coreroll/<core_id>")
def coreroll(core_id):
    if current_user.is_authenticated and (current_user.role == "admin" or current_user.role == "instructor"):
        core = Cores.query.filter_by(id=core_id).first()
        if core:
            registrations = core.registrations
            return render_template('coreroll.html', registrations=registrations, title='Core Roll')
        else:
            return render_template('notfound.html')
    else:
        return render_template('denied.html')



#### END OF THE CORE CODE ####

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

