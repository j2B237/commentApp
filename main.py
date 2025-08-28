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

comments = []


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))
    


@app.route("/", methods=["POST", "GET"])
def index():
    """ Home page"""
    
    if request.method == "GET":
        return render_template("index.html", comments=comments)
    
    comments.append(request.form["contents"])
    return redirect(url_for('index'))
    

