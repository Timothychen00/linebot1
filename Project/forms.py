from flask import Flask
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,TextField,SubmitField,SelectMultipleField,SelectField,PasswordField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired

class FinishForm(FlaskForm):#used to finish the mission
    pass

class DelayForm(FlaskForm):#used to delay the mission
    pass

class CustomerForm(FlaskForm):#used to create a new customer
    pass

class LoginForm(FlaskForm):
    username=TextField("用戶名",validators=[InputRequired()])
    password=PasswordField('密碼',validators=[InputRequired()])
    submit=SubmitField("登入")