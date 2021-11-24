from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,EmailField,SelectField
from wtforms.validators import DataRequired,Length,InputRequired

class SearchForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(),Length(min=6, max=35)])
    submit = SubmitField('Search')

class SignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired(),Length(min=1)])
    last_name = StringField('Last Name', validators=[InputRequired(),Length(min=1)])
    email = EmailField('Email', validators=[DataRequired(),Length(min=6, max=35)])
    action = SelectField('Action', choices = ['Sign up', 'Delete'], validators = [InputRequired()])
    submit = SubmitField('Submit')