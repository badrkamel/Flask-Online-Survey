from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField
from wtforms.validators import DataRequired

class EmailForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    choices = RadioField('Select One Choise',
     					  choices = [('yes','Yes'),('no','No')], 
     					  validators=[DataRequired()])

    submit = SubmitField('Send')
