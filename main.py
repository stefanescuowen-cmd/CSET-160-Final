import os
from flask import Flask, render_template, request, redirect
from app.config import Config
from app.extensions import db
from app.models import User, Test, Question, Option, Submission, Answer

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# ------
# Routes
# ------

# ----------------------- 
# Registration & Accounts
# -----------------------

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


# --------------- 
# Test Management
# ---------------

@app.route("/create_test", methods=["GET", "POST"])
def create_test():
    teachers = User.query.filter_by(role="teacher").all()
    if request.method == "POST":
        title = request.form["title"]
        teacher_id = request.form["teacher_id"]

        test = Test(title=title, teacher_id=teacher_id)
        db.session.add(test)
        db.session.commit()
        return redirect("/tests")

    return render_template("create_test.html", teachers=teachers)


@app.route("/tests")
def tests():
    all_tests = Test.query.all()
    return render_template("tests.html", tests=all_tests)


@app.route("/test/<int:test_id>/add_question", methods=["POST"])
def add_question(test_id):
    test = Test.query.get_or_404(test_id)

    question_text = request.form["question_text"]

    # All questions are open-ended
    question = Question(test_id=test_id, question_text=question_text)
    db.session.add(question)
    db.session.commit()

    return redirect(f"/test/{test_id}/edit")


@app.route("/test/<int:test_id>", methods=["GET", "POST"])
def take_test(test_id):
    test = Test.query.get_or_404(test_id)
    students = User.query.filter_by(role="student").all()

    if request.method == "POST":
        # Validate student selection
        try:
            student_id = int(request.form["student_id"])
        except ValueError:
            return "Invalid student selection!"

        student = User.query.filter_by(id=student_id, role="student").first()
        if not student:
            return "Selected user is not a valid student!"

        # Prevent multiple submissions
        existing = Submission.query.filter_by(test_id=test.id, student_id=student_id).first()
        if existing:
            return "You have already submitted this test!"

        # Create submission
        submission = Submission(test_id=test.id, student_id=student_id)
        db.session.add(submission)
        db.session.commit()

        # Save answers
        for question in test.questions:
            answer_text = request.form.get(f"question_{question.id}", "")
            answer = Answer(submission_id=submission.id, question_id=question.id, answer_text=answer_text)
            db.session.add(answer)
        db.session.commit()

        return redirect("/tests")

    return render_template("take_test.html", test=test, students=students)


@app.route("/test/<int:test_id>/edit", methods=["GET", "POST"])
def edit_test(test_id):
    test = Test.query.get_or_404(test_id)
    teachers = User.query.filter_by(role="teacher").all()

    if request.method == "POST":
        test.title = request.form["title"]
        test.teacher_id = request.form["teacher_id"]
        db.session.commit()
        return redirect("/tests")

    return render_template("edit_test.html", test=test, teachers=teachers)


@app.route("/test/<int:test_id>/delete", methods=["POST"])
def delete_test(test_id):
    test = Test.query.get_or_404(test_id)
    db.session.delete(test)
    db.session.commit()
    return redirect("/tests")


@app.route("/test/<int:test_id>/submissions")
def view_submissions(test_id):
    test = Test.query.get_or_404(test_id)
    submissions = Submission.query.filter_by(test_id=test.id).all()
    return render_template("submissions.html", test=test, submissions=submissions)


@app.route("/question/<int:question_id>/edit", methods=["GET", "POST"])
def edit_question(question_id):
    question = Question.query.get_or_404(question_id)
    if request.method == "POST":
        question.question_text = request.form["question_text"]
        db.session.commit()
        return redirect(f"/test/{question.test_id}/edit")
    return render_template("edit_question.html", question=question)


@app.route("/question/<int:question_id>/delete", methods=["POST"])
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    test_id = question.test_id
    db.session.delete(question)
    db.session.commit()
    return redirect(f"/test/{test_id}/edit")


# -----------------
# Grading & Results
# -----------------

@app.route("/submission/<int:submission_id>/grade", methods=["GET", "POST"])
def grade_submission(submission_id):
    submission = Submission.query.get_or_404(submission_id)
    teachers = User.query.filter_by(role="teacher").all()

    if request.method == "POST":
        submission.marks = request.form["marks"]
        submission.graded_by = request.form["teacher_id"]
        db.session.commit()
        return redirect(f"/test/{submission.test_id}/submissions")

    return render_template("grade_submission.html", submission=submission, teachers=teachers)


@app.route("/student/<int:student_id>/results")
def student_results(student_id):
    student = User.query.get_or_404(student_id)
    submissions = Submission.query.filter_by(student_id=student.id).all()
    return render_template("student_results.html", student=student, submissions=submissions)


@app.route("/tests/summary")
def tests_summary():
    tests = Test.query.all()

    tests_info = []
    for t in tests:
        student_count = Submission.query.filter_by(test_id=t.id).count()

        tests_info.append({
            "id": t.id,
            "title": t.title,
            "teacher": t.teacher.name,
            "student_count": student_count
        })

    return render_template("tests_summary.html", tests=tests_info)


@app.route("/test/<int:test_id>/summary")
def test_summary(test_id):
    test = Test.query.get_or_404(test_id)
    submissions = Submission.query.filter_by(test_id=test.id).all()

    return render_template(
        "test_summary.html",
        test=test,
        submissions=submissions
    )

# ----------
# Run server
# ----------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5001)))