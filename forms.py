from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, TextAreaField, FileField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class SignupForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class RequestForm(FlaskForm):
    location_type = RadioField('Location Type', 
                             choices=[('office', 'Office'), ('lab', 'Lab'), ('hall', 'Hall')],
                             validators=[DataRequired()])
    location_number = StringField('Location Number', validators=[DataRequired()])
    problem_type = SelectField('Problem Type',
                             choices=[('computer', 'Computer'), ('projector', 'Projector'), ('printer', 'Printer')],
                             validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    image = FileField('Image (Optional)')
