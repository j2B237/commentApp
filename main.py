from flask import (Flask, render_template, redirect, request, url_for)


app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=["POST", "GET"])
def index():
    """ Home page"""

    comments = []
    if request.method == "POST":
        
        comment = request.form['contents']
        print("Comment: ", comment)
        comments.append(comment)
        return redirect(url_for('index'))
    
    return render_template("index.html", comments=comments)

