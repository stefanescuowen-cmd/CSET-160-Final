from flask import Blueprint, render_template, request, redirect
from app.extensions import db
from app.models import User, Test

bp = Blueprint("routes", __name__)

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        role = request.form["role"]

        user = User(name=name, email=email, role=role)
        db.session.add(user)
        db.session.commit()
        return redirect("/accounts")

    return render_template("register.html")

@bp.route("/accounts")
def accounts():
    role_filter = request.args.get("role")
    if role_filter in ("student", "teacher"):
        users = User.query.filter_by(role=role_filter).all()
    else:
        users = User.query.all()
    return render_template("accounts.html", users=users)