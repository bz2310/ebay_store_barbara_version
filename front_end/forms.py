from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,EmailField,SelectField,DecimalField,IntegerField
from wtforms.validators import DataRequired,Length,InputRequired,ValidationError,NumberRange

class SignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(),Length(min=6, max=35)])
    submit = SubmitField('Signup')

class AdminForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired(),Length(min=1)])
    last_name = StringField('Last Name', validators=[InputRequired(),Length(min=1)])
    email = EmailField('Email', validators=[DataRequired(),Length(min=6, max=35)])
    action = SelectField('Action', choices = ['Sign up', 'Delete', 'Search'], validators = [InputRequired()])
    submit = SubmitField('Submit')

class BetterDecimalField(DecimalField):
    """
    Very similar to WTForms DecimalField, except with the option of rounding
    the data always.
    """
    def __init__(self, label=None, validators=None, places=2, rounding=None,
                 round_always=False, **kwargs):
        super(BetterDecimalField, self).__init__(
            label=label, validators=validators, places=places, rounding=
            rounding, **kwargs)
        self.round_always = round_always

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = decimal.Decimal(valuelist[0])
                if self.round_always and hasattr(self.data, 'quantize'):
                    exp = decimal.Decimal('.1') ** self.places
                    if self.rounding is None:
                        quantized = self.data.quantize(exp)
                    else:
                        quantized = self.data.quantize(
                            exp, rounding=self.rounding)
                    self.data = quantized
            except (decimal.InvalidOperation, ValueError):
                self.data = None
                raise ValueError(self.gettext('Not a valid decimal value'))

class ProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[InputRequired(),Length(min=1)])
    price = BetterDecimalField('Price', round_always=True, validators=[DataRequired(), NumberRange(min=0, max=10000)])
    inventory = IntegerField('Number in inventory', validators=[DataRequired(), Length(min=1)])
    image = StringField('Image URL', validators=[DataRequired()])
    action = SelectField('Action', choices = ['Create', 'Delete', 'Search'], validators = [InputRequired()])
    submit = SubmitField('Submit')