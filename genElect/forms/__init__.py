from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, SelectMultipleField, DateField, FileField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Length, EqualTo, Required, ValidationError, Optional
from wtforms import widgets
from wtforms.fields.html5 import DateTimeField
import datetime
from sqlalchemy import and_, or_

from genElect.models import Offerings, Event

def room_is_available(rid, st, et, oid=None):
	if not oid:
		o = Offerings.query.filter(
			and_(Offerings.room_id == rid,
				 or_(and_(et > Offerings.start_time,
						  et <= Offerings.end_time),
					 and_(st >= Offerings.start_time,
						  st < Offerings.end_time)))).first()
	else:
		o = Offerings.query.filter(
			and_(Offerings.room_id == rid,
			     Offerings.id != oid,
				 or_(and_(et > Offerings.start_time,
						  et <= Offerings.end_time),
					 and_(st >= Offerings.start_time,
						  st < Offerings.end_time)))).first()
	e = Event.query.filter(
		and_(Event.room_id == rid,
		 or_(and_(et > Event.start_time,
				  et <= Event.end_time),
			 and_(st >= Event.start_time,
				  st < Event.end_time)))).first()
	if o or e:
		return False
	else:
		return True

def core_period_to_datetimes(d, ps, pe):
	return (datetime.datetime(d.year, d.month, d.day, 8, 30) + datetime.timedelta(minutes=60 * (ps - 1)), datetime.datetime(d.year, d.month, d.day, 9, 30)+ datetime.timedelta(minutes=60 * (pe - 1)))

def offering_period_to_datetimes(d, ps, pe):
	return (datetime.datetime(d.year, d.month, d.day, 12, 30) + datetime.timedelta(minutes=90 * (ps - 1)), datetime.datetime(d.year, d.month, d.day, 2)+ datetime.timedelta(minutes=90 * (pe - 1)))

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
	description = StringField('Description', validators=[DataRequired(), Length(0,500)])
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
	instructor = SelectField('Instructor', validators=[DataRequired()], choices=[], coerce=int)
	room = SelectField('Room', validators=[Required()], choices=[], coerce=int)
	core_period = IntegerField('Core Period', validators=[DataRequired()])
	diff_choices = [('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')]
	difficulty = SelectField('Core Difficulty', choices=diff_choices, validators=[Required()])
	submit = SubmitField('Save Core')


#Form for creating and updating offerings
class OfferingForm(FlaskForm):
	room = SelectField('Room', validators=[Required()], choices=[], coerce=int)
	instructor = SelectField('Instructor', validators=[DataRequired()], choices=[], coerce=int)
	choices = [] #to be filled dynamically
	elective = SelectField('Elective', choices=choices, validators=[Required()], render_kw={"autofocus": True})
	capacity = IntegerField('Capacity', validators=[DataRequired()])
	num_choices = [(1,'1'), (2,'2'), (3,'3')]
	period_start = SelectField('Offering Period', choices=num_choices, validators=[Required()], coerce=int)
	period_length = SelectField('Offering Length', choices=num_choices, validators=[Required()], coerce=int)
	date = DateField('Offering Date', format="%Y-%m-%d", default=datetime.datetime.now().date())
	recur = BooleanField('Recurring Event')
	recur_end_date = DateField('Recur End Date', format="%Y-%m-%d", validators=[Optional()])
	offering_id = HiddenField('Offering ID', validators=[Optional()])
	submit = SubmitField('Save Offering')

	def validate_date(form, field):
		d = field.data
		(st, et) = offering_period_to_datetimes(d, form.period_start.data, form.period_length.data)
		if field.data and st.time() >= datetime.datetime(2021, 6, 14, 8, 30).time() and st.time() <= datetime.datetime(2021, 6, 14, 11, 30).time():
			raise ValidationError("You cannot schedule an offering during core periods")
		if not room_is_available(form.room.data, st, et, form.offering_id.data):
			raise ValidationError("Selected room is occupied")

	def validate_recur(form, field):
		if field.data and not form.recur_end_date.data:
			raise ValidationError("You must enter an end date for recurrence")

	def validate_recur_end_date(form, field):
		d = field.data
		r = form.recur.data
		if r and d and d < form.date.data:
			raise ValidationError("Recurrence must end in the future")
		od = form.date.data
		if r and d and od:
			while od <= d:
				(st, et) = offering_period_to_datetimes(od, form.period_start.data, form.period_length.data)
				if not room_is_available(form.room.data, st, et):
					raise ValidationError(f"Room is unavailable on {st}")
				od += datetime.timedelta(days=1)


#Form for creating and updating notifications
class NotificationForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()], render_kw={"autofocus": True})
	notification = StringField('Notification', validators=[DataRequired()])
	submit = SubmitField('Save Notification')


#Form for setting the registration time period
class TimeSetForm(FlaskForm):
	start_time = DateTimeField('Start Time', validators=[DataRequired()], format="%Y-%m-%d %H:%M", render_kw={"autofocus": True})
	end_time = DateTimeField('End Time', validators=[DataRequired()], format="%Y-%m-%d %H:%M")
	offering_date = DateField('Offering Date', validators=[DataRequired()], format="%Y-%m-%d")
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

class EventForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired(), Length(3,100)], render_kw={"autofocus": True})
	description = StringField('Description', validators=[DataRequired(), Length(0, 250)])
	room = SelectField('Room', validators=[Required()], coerce=int)
	start_time = DateTimeField('Start Time', validators=[DataRequired()], format="%Y-%m-%d %H:%M")
	end_time = DateTimeField('End Time', validators=[DataRequired()], format="%Y-%m-%d %H:%M")
	recur = BooleanField('Recurring Event')
	recur_end_date = DateField('Recur End Date', format="%Y-%m-%d", validators=[Optional()])
	submit = SubmitField('Save Event')

	def validate_end_time(form, field):
		if field.data < form.start_time.data:
			raise ValidationError("End time must fall after start time")

	def validate_recur(form, field):
		if field.data and not form.recur_end_date.data:
			raise ValidationError("You must enter an end date for recurrence")

	def validate_recur_end_date(form, field):
		d = field.data
		r = form.recur.data
		if r and d and datetime.datetime(d.year, d.month, d.day) < form.start_time.data:
			raise ValidationError("Recurrence must end in the future")
