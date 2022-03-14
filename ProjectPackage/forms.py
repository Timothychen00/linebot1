from flask_wtf import FlaskForm
from wtforms.fields import SelectField,TextField,SubmitField,DecimalField
from wtforms.validators import InputRequired
from ProjectPackage import parameter

class FinishForm(FlaskForm):
    name=SelectField('客戶名稱',choices=['Timothychen',"B"],validators=[InputRequired()])
    component=SelectField("部件名稱",choices=[],validators=[InputRequired()])
    submit=SubmitField('送出')
class DelayForm(FlaskForm):
    name=SelectField("客戶名稱",choices=['Timothychen',"B"],validators=[InputRequired()])
    component=SelectField("部件名稱",choices=[],validators=[InputRequired()])
    days=TextField("延遲天數",validators=[InputRequired()])
    submit=SubmitField('送出')
class AddUserForm(FlaskForm):
    
    submit=SubmitField("送出")
    
# ,NumberInput(min=1,max=999)    
class SettingsForm(FlaskForm):
    component1=DecimalField('部件1',validators=[InputRequired()])
    component2=DecimalField('部件2',validators=[InputRequired()])
    component3=DecimalField('部件3',validators=[InputRequired()])
    component4=DecimalField('部件4',validators=[InputRequired()])
    component5=DecimalField('部件5',validators=[InputRequired()])
    component6=DecimalField('部件6',validators=[InputRequired()])
    submit=SubmitField('Submit')