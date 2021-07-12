from flask import Flask, render_template, url_for

app = Flask(__name__)                    # this gets the name of the file so Flask knows it's name

@app.route("/") #slash is hompe page                          # this tells you the URL the method below is related to
def hello_world():
    return "<p>Hello, World!</p>"        # this prints HTML to the webpage
  
@app.route("/about") #slash is home page                          # this tells you the URL the method below is related to
def about():
    return render_template('about.html', subtitle='About Page') 
  
@app.route("/home") #slash is hompe page  
def home():
    return render_template('home.html', subtitle='Home Page') 
  
if __name__ == '__main__':               # this should always be at the end
    app.run(debug=True, host="0.0.0.0")