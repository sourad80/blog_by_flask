from flask_wtf import Form
from flask_wtf.file import FileField,file_allowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class Registration(Form):
    username = StringField('Username', validators = [ DataRequired() , Length(min = 2, max = 20) ])
    email = StringField('Email',validators= [ DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmpassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username = username.data).first()

        if user:
            raise ValidationError('Username already exist!!')
    
    def validate_email(self,email):
        user = User.query.filter_by(email = email.data).first()

        if user:
            raise ValidationError('Emali already exist!!')

class Login(Form):
    email = StringField('Email',validators= [ DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class Update(Form):
    username = StringField('Username', validators = [ DataRequired() , Length(min = 2, max = 20) ])
    email = StringField('Email',validators= [ DataRequired(), Email()])
    image = FileField('Update Profile Picture', validators=[file_allowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()

            if user:
                raise ValidationError('Username already exist!!')
        
    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()

            if user:
                raise ValidationError('Emali already exist!!')

class request_reset_password(Form):
    email = StringField('Email',validators= [ DataRequired(), Email()])
    submit = SubmitField('Request Password Change')

    def validate_email(self,email):
        user = User.query.filter_by(email = email.data).first()

        if not user:
            raise ValidationError("Emali doesn't exist!!")

class reset_password(Form):
    password = PasswordField('Password', validators=[DataRequired()])
    confirmpassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Change Password')