from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_BINDS'] = {'chat': 'sqlite:///chat.db'}
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/")
def default():
    return redirect('/login/')

@app.route("/login/", methods=["GET", "POST"])
def login_controller():
    if request.method == 'POST':
        pass
    else:
        return render_template("login_page.html")

@app.route("/register/", methods=["GET", "POST"])
def register_controller():
    if request.method == 'POST':
        print(request)
        return render_template("register.html")
    else:
        return render_template("register.html")

@app.route("/profile/<username>")
def profile(username=None):
    pass

@app.route("/logout/")
def unlogger():
    pass

@app.route("/new_message/", methods=["POST"])
def new_message():
    pass

@app.route("/messages/")
def messages():
    pass

if __name__ == "__main__":
	app.run(debug=True)