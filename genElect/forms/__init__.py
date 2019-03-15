from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Required


#Form for Creating New Users (for Administrators)
class CreateUserForm(FlaskForm):
	full_name = StringField('Full Name', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired()])
	username = StringField('Username', validators=[DataRequired()])
	choices = [('student','Student'), ('instructor','Instructor'), ('admin','Admin')]
	role = SelectField('User Role', choices=choices, validators=[Required()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Create User')

#Form for Updating user information (for Administrators)
class UpdateUserForm(FlaskForm):
	full_name = StringField('Full Name', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired()])
	username = StringField('Username', validators=[DataRequired()])
	choices = [('student','Student'), ('instructor','Instructor'), ('admin','Admin')]
	role = SelectField('User Role', choices=choices, validators=[Required()])
	submit = SubmitField('Update User')


#Form for Logging In
class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


#Form for creating and updating electives
class ElectiveForm(FlaskForm):
	name = StringField('Elective Name', validators=[DataRequired()])
	description = StringField('Description', validators=[DataRequired()])
	prerequisites = StringField('Prerequisites', validators=[DataRequired()])
	submit = SubmitField('Save Elective')


#Form for creating and updating offerings
class OfferingForm(FlaskForm):
	building = StringField('Building', validators=[DataRequired()])
	room = StringField('Room', validators=[DataRequired()])
	instructor = StringField('Instructor', validators=[DataRequired()])
	#choices = get_elective_choices()
	#elective = SelectField('Elective', choices=choices, validators=[Required()])
	capacity = IntegerField('capacity', validators=[DataRequired()])
	submit = SubmitField('Save Offering')


#Form for creating and updating notifications
class NotificationForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	notification = StringField('Notification', validators=[DataRequired()])
	submit = SubmitField('Save Notification')