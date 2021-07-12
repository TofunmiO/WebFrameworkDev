from flask import Flask, render_template, url_for, flash, redirect
from falsk_wtf import FlaskForm
from wtforms import Stringfield, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from forms import RegistrationForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)                    # this gets the name of the file so Flask knows it's name
app.config['SECRET KEY'] ='669ff589765fb1019b125588d2d85a50'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlie:///site.db'

db = SQLAlchemy(app)

# creating schema
class User(db.Model):
  id = db.Column(db.Integer,primary_key= True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column( db.String(60), nullable=False)

def __repr__(self):
  return f"User('{self.username}', '{self.email}')"


@app.route("/") #slash is home page                   # this tells you the URL the method below is related to
def hello_world():
    return "<p>Hello, World!</p>"        # this prints HTML to the webpage


@app.route("/about") #slash is home page                          # this tells you the URL the method below is related to
def about():
    return render_template('about.html', subtitle='About Page') 
  
@app.route("/home") #slash is hompe page  
def home():
    return render_template('home.html', subtitle='Home Page') 
  
@app.route("/register", methods=['GET', 'POST']) #getting info from user and posting  
def register():
  form= RegistrationForm()
    return render_template('register_html', subtitle ='Register', form=form)


if __name__ == '__main__':               # this should always be at the end
    app.run(debug=True, host="0.0.0.0")