from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, SelectMultipleField, DateField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, Required, ValidationError
from wtforms import widgets
from wtforms.fields.html5 import DateTimeField
import datetime

#Form for User information (for Administrators)
class UserForm(FlaskForm):
	full_name = StringField('Full Name', validators=[DataRequired()], render_kw={"autofocus": True, "autocomplete": "off"})
	email = StringField('Email', validators=[DataRequired()])
	username = StringField('Username', validators=[DataRequired()])
	choices = [('student','Student'), ('instructor','Instructor'), ('admin','Admin')]
	role = SelectField('User Role', choices=choices, validators=[Required()])
	password = PasswordField('Set New Password', render_kw={"autocomplete": "off"})
	core1 = SelectField('Period 1 Core', choices=[('0','none')])
	core2 = SelectField('Period 2 Core', choices=[('0','none')])
	core3 = SelectField('Period 3 Core', choices=[('0','none')])
	submit = SubmitField('Save User')


#Form for Logging In
class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()], render_kw={"autocomplete": "off", "autofocus": True})
	password = PasswordField('Password', validators=[DataRequired()], render_kw={"autocomplete": "off"})
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


#Form for creating and updating electives
class ElectiveForm(FlaskForm):
	name = StringField('Elective Name', validators=[DataRequired()], render_kw={"autofocus": True})
	description = StringField('Description', validators=[DataRequired()])
	learning_objective = StringField('Learning Objective', validators=[DataRequired()])
	prerequisites = SelectMultipleField('Prerequisites', choices = []) #fill dynamically
	diff_choices = [('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')]
	difficulty = SelectField('Elective Difficulty', choices=diff_choices, validators=[Required()])
	can_retake = BooleanField('Allow users to take several times')
	submit = SubmitField('Save Elective')


#Form for creating and updating electives
class CoreForm(FlaskForm):
	name = StringField('Core Name', validators=[DataRequired()], render_kw={"autofocus": True})
	description = StringField('Description', validators=[DataRequired()])
	instructor = StringField('Instructor', validators=[DataRequired()])
	building = StringField('Building', validators=[DataRequired()])
	room = StringField('Room', validators=[DataRequired()])
	core_period = IntegerField('Core Period', validators=[DataRequired()])
	diff_choices = [('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')]
	difficulty = SelectField('Elective Difficulty', choices=diff_choices, validators=[Required()])
	submit = SubmitField('Save Core')


#Form for creating and updating offerings
class OfferingForm(FlaskForm):
	building = StringField('Building', validators=[DataRequired()], render_kw={"autofocus": True})
	room = StringField('Room', validators=[DataRequired()])
	instructor = StringField('Instructor', validators=[DataRequired()])
	choices = [] #to be filled dynamically
	elective = SelectField('Elective', choices=choices, validators=[Required()])
	capacity = IntegerField('Capacity', validators=[DataRequired()])
	num_choices = [('1','1'), ('2','2'), ('3','3')]
	period_start = SelectField('Offering Period', choices=num_choices, validators=[Required()])
	period_length = SelectField('Offering Length', choices=num_choices, validators=[Required()])
	submit = SubmitField('Save Offering')


#Form for creating and updating notifications
class NotificationForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()], render_kw={"autofocus": True})
	notification = StringField('Notification', validators=[DataRequired()])
	submit = SubmitField('Save Notification')


#Form for setting the registration time period
class TimeSetForm(FlaskForm):
	start_time = DateTimeField('Start Time', validators=[DataRequired()], format="%Y-%m-%d %H:%M:%S", render_kw={"autofocus": True})
	end_time = DateTimeField('End Time', validators=[DataRequired()], format="%Y-%m-%d %H:%M:%S")
	submit = SubmitField('Set Time')

	def validate_start_time(form ,field):
		if field.data < datetime.datetime.now():
			raise ValidationError("Start date must be in the future")

	def validate_end_time(form, field):
		if field.data < form.start_time.data:
			raise ValidationError("End time must fall after start time")

class BuildingForm(FlaskForm):
	name = StringField('Building Name', validators=[DataRequired(), Length(3,100)], render_kw={"autofocus": True})
	submit = SubmitField('Save Building')

class RoomForm(FlaskForm):
	building = SelectField('Building', validators=[Required()], coerce=int, render_kw={"autofocus": True})
	name = StringField('Room Name', validators=[DataRequired(), Length(3,100)])
	submit = SubmitField('Save Room')
