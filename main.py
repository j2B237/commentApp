from flask import (Flask, render_template, redirect, request, url_for)
from flask_sqlalchemy import SQLAlchemy


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

db = SQLAlchemy(app)


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))



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
    
    if request.method == "POST":

        codepin = request.form["digit0"] + request.form["digit1"] + request.form["digit2"] + request.form["digit3"]
        phone   = request.form["phone"].replace('-','')

        if phone != "785879012" or codepin != "1234":
            return render_template("login.html", error=True)
        
    return redirect(url_for("index"))

