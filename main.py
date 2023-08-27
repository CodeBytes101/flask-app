from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message
import json

with open("config.json", "r") as config_file:
    params = json.load(config_file)["params"]


app = Flask(__name__)

app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params["email"],
    MAIL_PASSWORD=params["password"],
)
mail = Mail(app)
if params["local_server"] == "True":
    app.config["SQLALCHEMY_DATABASE_URI"] = params["local_uri"]
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params["prod_uri"]

db = SQLAlchemy(app)


class Contact(db.Model):
    Sno = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    phone_no = db.Column(db.String(20), nullable=False)
    message = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(), nullable=False)


class codebytes(db.Model):
    Sno = db.Column(db.Integer(), primary_key=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(), nullable=False)
    by = db.Column(db.String(20), nullable=False)
    fname = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(), nullable=False)


@app.route("/post/<string:post_slug>", methods=["GET"])
def post_route(post_slug):
    post = codebytes.query.filter_by(slug=post_slug).first()
    return render_template("post.html", params=params, post=post)


@app.route("/index.html")
def home():
    return render_template("index.html")


@app.route("/about.html")
def about():
    return render_template("about.html", params=params)


@app.route("/contact.html", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        number = request.form.get("number")
        message = request.form.get("message")
        entry = Contact(
            name=name,
            phone_no=number,
            email=email,
            date=datetime.now(),
            message=message,
        )
        db.session.add(entry)
        db.session.commit()
        msg = Message(
            f"New Message from {name}",
            sender=email,
            recipients=["roshanleharwani@gmail.com"],
        )
        msg.body = f"{message}\n\nMobile Number:{number}\n\nEmail: {email}"
        mail.send(msg)
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
