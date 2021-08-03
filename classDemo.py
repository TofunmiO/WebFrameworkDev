from flask import Flask, render_template, url_for, flash, redirect
from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField, BooleanField
# from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from forms import RegistrationForm
from loginForms import LoginForm
from flask_sqlalchemy import SQLAlchemy
from audio import printWAV
import time, random, threading
from turbo_flask import Turbo
from flask_bcrypt import Bcrypt
from flask_behind_proxy import FlaskBehindProxy


app = Flask(__name__)                    # this gets the name of the file so Flask knows it's name
proxied = FlaskBehindProxy(app)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = '21d5e83a343bebf7c4174dd694091ffd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #location in flask. when you run it create site.db file

db = SQLAlchemy(app)
interval = 12
FILE_NAME = "value.wav"
turbo = Turbo(app)

# creating schema
class User(db.Model):
  id = db.Column(db.Integer,primary_key= True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"


@app.route("/") #slash is home page                   # this tells you the URL the method below is related to
@app.route("/home") #slash is hompe page  
def home():
    return render_template('home.html', subtitle='Home Page')        # this prints HTML to the webpage

@app.route("/about") #slash is home page                          # this tells you the URL the method below is related to
def about():
    return render_template('about.html', subtitle='About Page') 
  
  
@app.route("/register", methods=['GET', 'POST']) #getting info from user and posting  
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        pw_hash = (bcrypt.generate_password_hash(password=form.password.data).decode('uft-8')
        bcrypt.check_password_hash(pw_hash, password=form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=pw_hash)
#         print(user)
        try:
            db.session.add(user)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            flash(f'Username or email account already exists!', 'success')
        else:
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('home')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])   
def login():
    form = LoginForm()
    if form.validate_on_submit(): 
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            flash(f'Incorrect username for {form.username.data}! Try again!', 'failed')
            return redirect(url_for('login'))
        password = User.query.filter_by(password=form.password.data).first()
        if not password:
          flash(f'Incorrect password for {form.username.data}! Try again!', 'failed')
          return redirect(url_for('login'))
        flash(f'Successful login for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('login.html', title='Login', form=form)
  
@app.route("/captions")
def captions():
    TITLE = "value"
    return render_template('captions.html', songName=TITLE, file=FILE_NAME)
  
@app.before_first_request
def before_first_request():
    #resetting time stamp file to 0
    file = open("pos.txt","w") 
    file.write(str(0))
    file.close()

    #starting thread that will time updates
    threading.Thread(target=update_captions, daemon=True).start()
    
# integration testing    
# def time_stamp():
#     pass
#     file = open("pos.txt","w")
#     pos = int(file.read())
#     file.write(str(pos+interval))
#     file.close()

@app.context_processor
def inject_load():
    # getting previous time stamp
#     try:
    file = open("pos.txt","r")
#     except:  
    pos = int(file.read())
    file.close()
    
#     time_stamp()
#     writing next time stamp
    file = open("pos.txt","w")
    file.write(str(pos+interval))
    file.close()

    #returning captions
    return {'caption':printWAV(FILE_NAME, pos=pos, clip=interval)}

def update_captions():
    with app.app_context():
        while True:
            # timing thread waiting for the interval
            time.sleep(interval)

            # forcefully updating captionsPane with caption
            turbo.push(turbo.replace(render_template('captionsPane.html'), 'load'))
            

if __name__ == '__main__':               # this should always be at the end
    app.run(debug=True, host="0.0.0.0")  #5f788a
