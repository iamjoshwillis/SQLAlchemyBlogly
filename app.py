from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import text
from models import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route("/")
def show_home():
    users = User.query.all()
    return render_template("home.html", users=users)

@app.route("/add-user")
def show_add_page():
    return render_template("add-user.html")

@app.route("/add-user", methods=["POST"])
def add_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f"/user/{new_user.id}")

@app.route("/user/<int:user_id>")
def show_user_page(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user.html", user=user)

@app.route("/user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    User.query.filter(User.id == user_id).delete()
    db.session.commit()

    return redirect("/")

@app.route("/user/<user_id>/edit")
def show_edit_page(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edit-user.html", user=user)

@app.route("/user/<int:user_id>/edit", methods=["POST"])
def commit_edit(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]

    db.session.add(user)
    db.session.commit()

    return redirect(f"/user/{user.id}")