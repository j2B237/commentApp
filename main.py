from flask import (Flask, render_template, redirect, request, url_for)
from flask_sqlalchemy import SQLAlchemy
from flask_login import (login_user, UserMixin, LoginManager)
from flask_bcrypt import Bcrypt

import os

app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="root",
    password="Ladife2025",
    hostname="127.0.0.1:3306",
    databasename="comments",
)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299

app.secret_key = os.urandom(16)

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

# Initialize app extension
db.init_app(app)
login_manager.init_app(app)
bcrypt.init_app(app)

class User(db.Model, UserMixin):

    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    phone_number = db.Column(db.String(10), nullable=False, unique=True)
    codepin_hashed = db.Column(db.String(128), nullable=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError("Le code pin n'est pas accessible en lecture")
    
    @password.setter
    def password(self, codepin):
        self.codepin_hashed = bcrypt.generate_password_hash(codepin)

    def verify_password(self, codepin):
        return bcrypt.check_password_hash(self.codepin_hashed, codepin)


class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/", methods=["POST", "GET"])
def index():
    """ Home page"""
    
    if request.method == "GET":
        return render_template("index.html", comments=Comment.query.all())
    
    if request.form["contents"] != "":
        comment = Comment(content=request.form["contents"])
        db.session.add(comment)
        db.session.commit()
    
    return redirect(url_for('index'))

@app.route("/login/", methods=["POST", "GET"])
def login():
    """ Login page """

    if request.method == "GET":
        return render_template("login.html", error=False)
    
    codepin = request.form["digit0"] + request.form["digit1"] + request.form["digit2"] + request.form["digit3"]
    phone   = request.form["phone"].replace('-','')

    current_user = User.query.filter_by(phone_number=phone).first()
    if current_user is None:
        return render_template("login.html", error=True)

    if not current_user.verify_password(codepin):
        return render_template("login.html", error=True)
        
    login_user = current_user
    return redirect(url_for("index"))

