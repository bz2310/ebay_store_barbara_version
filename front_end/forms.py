from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,EmailField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('Search')