#import some basics
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError



#Create some fields
# Datarequired means field cant be empty
class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Sign Up')   
#   def check(username):
#     user = User.query.filter_by(username = username).first()
#     if not user:
#       raise ValidationError(user)
      
#   def check(password):
#     password = User.query.filter_by(password = password).first()
#     if not password:
#       raise ValidationError(password)
      
  
      