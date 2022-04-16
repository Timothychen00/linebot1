from flask import Flask
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,TextField,SubmitField,SelectMultipleField,SelectField,PasswordField,BooleanField
from wtforms.fields.html5 import DateField
from wtforms.widgets.html5 import MonthInput
from wtforms.validators import InputRequired,AnyOf,Regexp

class FinishForm(FlaskForm):#used to finish the
    key=SelectField("搜索類型",choices=[("name",'姓名'),('phone','電話'),('_id',"_id"),('address','地址')])
    value=TextField("搜索內容")
    state=TextField("搜索結果",validators=[InputRequired(),AnyOf(['found'],message='請先選擇正確的用戶')])
    component=SelectMultipleField("部件",choices=[("A",'第一道'),("B",'第二道'),("C",'第三道'),("D",'第四道'),("E",'第五道'),("F",'第六道')])
    finish_time=DateField('完成日期',validators=[InputRequired("請輸入完成日期")])
    next_time=TextField('下次保養月份',validators=[InputRequired(),Regexp("\d\d\d\d-\d\d",message="請輸入 YYYY-mm 格式的月份")])
    person=TextField('人員',validators=[InputRequired()])
    note=TextAreaField("備註")
    fee=TextField("費用")
    submit=SubmitField('完成')

class DelayForm(FlaskForm):#used to delay the mission
    key=SelectField("搜索類型",choices=[("name",'姓名'),('phone','電話'),('_id',"_id"),('address','地址')])
    value=TextField("搜索內容")
    state=TextField("搜索結果",validators=[InputRequired('請先選擇用戶')])
    next_time=TextField('下次保養日期',validators=[InputRequired(),Regexp("\d\d\d\d-\d\d",message="請輸入 YYYY-mm 格式的月份")])
    person=TextField('人員',validators=[InputRequired()])
    note=TextAreaField('備註')
    submit=SubmitField('完成')

class CustomerForm(FlaskForm):#used to create a new customer
    id=TextField('id',validators=[InputRequired()])
    name=TextField("客戶名稱",validators=[InputRequired()])
    address=TextField("地址",validators=[InputRequired()])
    phone=TextField('電話',validators=[InputRequired()])
    machine=TextField("機器型號",validators=[InputRequired()])
    note=TextAreaField('備註')
    last_time=TextField('上次保養日期',validators=[InputRequired(),Regexp("\d\d\d\d-\d\d",message="請輸入 YYYY-mm 格式的月份")])
    submit=SubmitField("儲存")
    next_time=TextField('下次保養日期',validators=[InputRequired(),Regexp("\d\d\d\d-\d\d",message="請輸入 YYYY-mm 格式的月份")])
    submit=SubmitField("儲存")

class LoginForm(FlaskForm):
    username=TextField("用戶名",validators=[InputRequired()])
    password=PasswordField('密碼',validators=[InputRequired()])
    rememberme=BooleanField('記住我')
    submit=SubmitField("登入")