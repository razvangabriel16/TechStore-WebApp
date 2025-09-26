from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp

class LoginForm(FlaskForm):
    username = username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=3, max=20),
            Regexp('^[A-Za-z][A-Za-z0-9_]*$', message="Username must contain only letters, numbers, or underscores!")
        ]
    )
    password = PasswordField('Password',
                            validators=[
                            DataRequired(),
                            Length(min=6, message="Password must have at least 6 characters!")
                            ])
    email = EmailField('Email',
                        validators=[
                        DataRequired(), 
                        Email(message="Please enter a valid email address!")])
    submit = SubmitField('Login')
    
class SignUpForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=3, max=20),
            Regexp('^[A-Za-z][A-Za-z0-9_]*$', message="Username must contain only letters, numbers, or underscores!")
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6, message="Password must have at least 6 characters!")
        ]
    )
    email = EmailField(
        'Email',
        validators=[
            DataRequired(),
            Email(message="Please enter a valid email address!")
        ]
    )
    submit = SubmitField('Sign Up')

    