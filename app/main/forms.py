from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired, Length
from app.models import Announcments

class Announcment(Form):
    title = StringField('Announcment',validators=[DataRequired(),Length(min = 2,max = 100)])
    submit = SubmitField('Announce')