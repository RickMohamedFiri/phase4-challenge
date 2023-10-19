from wtforms import Form, StringField, FloatField, IntegerField
from wtforms.validators import Length, DataRequired, NumberRange

class RestaurantForm(Form):
    name = StringField('Name', validators=[DataRequired(), Length(max=50)])
    address = StringField('Address', validators=[DataRequired(), Length(max=255)])

class RestaurantPizzaForm(Form):
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=1, max=30)])
    pizza_id = IntegerField('Pizza ID', validators=[DataRequired()])
    restaurant_id = IntegerField('Restaurant ID', validators=[DataRequired()])
