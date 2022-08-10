from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_BINDS'] = {'chat': 'sqlite:///chat.db'}
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class Chat(db.Model):
    __bind_key__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    message = db.Column(db.String(200), nullable=False)
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
    app.logger.info(f"Register Route {request.method}")
    if request.method == 'POST':

        r_username = request.form['register_user']
        r_email = request.form['register_email']
        r_pw_1 = request.form['register_pw_1']
        r_pw_2 = request.form['register_pw_2']
        
        if r_pw_1 != r_pw_2:
            app.logger.error("Register Failed: Passwords Did Not Match!")
            return render_template("register.html")
        
        new_user = User(username = r_username, email = r_email, password = r_pw_1)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(f'/profile/{r_username}')
        except Exception as e:
            app.logger.error("Could Not Add User To Database")
            app.logger.error(e)
            return render_template("register.html")

    else:
        return render_template("register.html")

@app.route("/profile/<username>")
def profile(username=None):
    return render_template("chat_page.html")

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
    db.create_all()
    app.run(debug=True)