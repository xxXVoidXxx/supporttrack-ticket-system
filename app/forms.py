from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length

# Login form: used for existing users
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')  # Optional "stay logged in"
    submit = SubmitField('Login')

# Registration form: for new users
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=6)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password')
    ])
    submit = SubmitField('Register')

# New form for submitting support tickets
class TicketForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=120)])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit Ticket')

