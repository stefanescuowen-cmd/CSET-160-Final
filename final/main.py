from flask import Flask, render_template, request, redirect
from app.config import Config
from app.extensions import db
from app.models.user import User
from app.models.test import Test

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# ------
# Routes
# ------

@app.route("/register", methods=["GET", "POST"])
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


@app.route("/accounts")
def accounts():
    role_filter = request.args.get("role")
    if role_filter in ("student", "teacher"):
        users = User.query.filter_by(role=role_filter).all()
    else:
        users = User.query.all()
    return render_template("accounts.html", users=users)


@app.route("/create_test", methods=["GET", "POST"])
def create_test():
    teachers = User.query.filter_by(role="teacher").all()
    if request.method == "POST":
        title = request.form["title"]
        teacher_id = request.form["teacher_id"]
        is_timed = bool(request.form.get("is_timed"))
        duration = request.form.get("duration") or None

        test = Test(title=title, teacher_id=teacher_id, is_timed=is_timed, duration=duration)
        db.session.add(test)
        db.session.commit()
        return redirect("/tests")

    return render_template("create_test.html", teachers=teachers)


@app.route("/tests")
def tests():
    all_tests = Test.query.all()
    return render_template("tests.html", tests=all_tests)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)    