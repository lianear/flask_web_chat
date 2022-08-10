import re
from flask import Flask, render_template, url_for, jsonify, request, redirect
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
    def __repr__(self):
        return f'<User {self.username}, {self.password}>'

class Chat(db.Model):
    __bind_key__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'message': self.message,
            'date_created': self.date_created
        }


@app.route("/")
def default():
    return redirect('/login/')

@app.route("/login/", methods=["GET", "POST"])
def login_controller():
    if request.method == 'POST':
        entered_username = request.form['login_user']
        entered_password = request.form['login_pw']
        results = db.session.query(User).filter(User.username == entered_username).all()
        if len(results) == 0:
            app.logger.error("Username Not Registered")
            return render_template("login_page.html")
        elif len(results) > 1:
            app.logger.error("Multiple Registered Accounts With Username = " + str(entered_username))
            return render_template("login_page.html")
        actual_password = results[0].password
        if actual_password == entered_password:
            return redirect(f'/profile/{entered_username}')
        else:
            app.logger.error("Incorrect Password!")
            return render_template("login_page.html")

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
            #app.logger.error(e)
            return render_template("register.html")

    else:
        return render_template("register.html")

@app.route("/profile/<username>")
def profile(username=None):
    return render_template("chat_page.html", username=username)

@app.route("/logout/")
def unlogger():
    return redirect('/')

@app.route("/new_message/", methods=["POST"])
def new_message():
    #app.logger.info(f"New Message Route {request.method}")
    m_author = request.form['username']
    m_msg = request.form['message']
             
    new_chat = Chat(username = m_author, message = m_msg)
    try:
        db.session.add(new_chat)
        db.session.commit()
        app.logger.info("Message Sent!")
        return redirect(f'/profile/{m_author}')
    except Exception as e:
        app.logger.error("Could Not Add Chat To Database")
        app.logger.error(e)
        return redirect(f'/profile/{m_author}')


@app.route("/messages/")
def messages():
    chats = Chat.query.order_by(Chat.date_created).all()

    return jsonify([i.serialize() for i in chats])

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)