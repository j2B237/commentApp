from flask import (Flask, render_template, redirect, request, url_for)


app = Flask(__name__)
app.config["DEBUG"] = True
comments = []

@app.route("/", methods=["POST", "GET"])
def index():
    """ Home page"""
    
    if request.method == "GET":
        return render_template("index.html", comments=comments)
    
    comments.append(request.form["contents"])
    return redirect(url_for('index'))
    

