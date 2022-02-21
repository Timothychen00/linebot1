from flask_wtf import FlaskForm
from wtforms.fields import SelectField,TextField,SubmitField,DecimalField
from wtforms.validators import InputRequired

class FinishForm(FlaskForm):
    submit=SubmitField('Submit')
class DelayForm(FlaskForm):
    submit=SubmitField('Submit')
class UserForm(FlaskForm):
    submit=SubmitField("Submit")
    
# ,NumberInput(min=1,max=999)    
class SettingsForm(FlaskForm):
    component1=DecimalField('部件1',validators=[InputRequired()])
    component2=DecimalField('部件2',validators=[InputRequired()])
    component3=DecimalField('部件3',validators=[InputRequired()])
    component4=DecimalField('部件4',validators=[InputRequired()])
    component5=DecimalField('部件5',validators=[InputRequired()])
    component6=DecimalField('部件6',validators=[InputRequired()])
    submit=SubmitField('Submit')