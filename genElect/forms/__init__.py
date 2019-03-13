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


#Form for Logging In
class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


#Form for creating electives
class CreateElectiveForm(FlaskForm):
	name = StringField('Elective Name', validators=[DataRequired()])
	instructor = StringField('Instructor', validators=[DataRequired()])
	description = StringField('Description', validators=[DataRequired()])
	prerequisites = StringField('Prerequisites', validators=[DataRequired()])
	capacity = IntegerField('capacity', validators=[Required()])
	submit = SubmitField('Save Elective')