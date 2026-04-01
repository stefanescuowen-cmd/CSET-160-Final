from flask import Blueprint, render_template, request, redirect, url_for
from app.extensions import db
from datetime import datetime, timedelta
from app.models import User, Test, Question, Submission, Answer

bp = Blueprint("main", __name__)

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        role = request.form.get("role")

        if not (name and email and role):
            return "All fields are required!"

        user = User(name=name, email=email, role=role)
        db.session.add(user)
        db.session.commit()
        return redirect("/accounts")

    return render_template("register.html")

# Blueprint setup
bp = Blueprint("main", __name__, template_folder="../templates")

# -----------------------
# Registration & Accounts
# -----------------------
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
    users_query = User.query
    role_filter = request.args.get("role")
    sort_by = request.args.get("sort")

    if role_filter in ("student", "teacher"):
        users_query = users_query.filter_by(role=role_filter)

    if sort_by == "name":
        users_query = users_query.order_by(User.name)
    elif sort_by == "date":
        users_query = users_query.order_by(User.created_at.desc())

    users = users_query.all()
    return render_template("accounts.html", users=users)


# ---------------
# Test Management (with Timed Test Support)
# ---------------

@bp.route("/create_test", methods=["GET", "POST"])
def create_test():
    teachers = User.query.filter_by(role="teacher").all()

    if request.method == "POST":
        title = request.form.get("title")
        teacher_id = request.form.get("teacher_id")
        is_timed = bool(request.form.get("is_timed"))
        duration = request.form.get("duration")

        if not (title and teacher_id):
            return "Title and teacher selection required!"

        test = Test(
            title=title,
            teacher_id=int(teacher_id),
            is_timed=is_timed,
            duration=int(duration) if duration else None
        )
        db.session.add(test)
        db.session.commit()
        return redirect("/tests")

    return render_template("create_test.html", teachers=teachers)


@bp.route("/tests")
def tests():
    all_tests = Test.query.all()
    return render_template("tests.html", tests=all_tests)


@bp.route("/test/<int:test_id>/add_question", methods=["POST"])
def add_question(test_id):
    question_text = request.form.get("question_text")
    q_type = request.form.get("type")

    if q_type == "mcq":
        question = Question(
            test_id=test_id,
            question_text=question_text,
            type="mcq",
            option_a=request.form.get("option_a"),
            option_b=request.form.get("option_b"),
            option_c=request.form.get("option_c"),
            option_d=request.form.get("option_d"),
            correct_answer=request.form.get("correct_answer")
        )
    else:
        question = Question(
            test_id=test_id,
            question_text=question_text,
            type="open"
        )

    db.session.add(question)
    db.session.commit()
    return redirect(f"/test/{test_id}/edit")


@bp.route("/test/<int:test_id>", methods=["GET", "POST"])
def take_test(test_id):
    test = Test.query.get_or_404(test_id)
    students = User.query.filter_by(role="student").all()

    # Pagination
    page = request.args.get("page", 1, type=int)
    per_page = 10
    questions = Question.query.filter_by(test_id=test.id)\
        .offset((page - 1) * per_page)\
        .limit(per_page).all()
    total = Question.query.filter_by(test_id=test.id).count()

    if request.method == "POST":
        try:
            student_id = int(request.form.get("student_id"))
        except (TypeError, ValueError):
            return "Invalid student selection!"

        # Find or create submission
        submission = Submission.query.filter_by(test_id=test.id, student_id=student_id).first()
        if not submission:
            submission = Submission(test_id=test.id, student_id=student_id)
            db.session.add(submission)
            db.session.commit()

        # Save answers for this page
        for question in questions:
            answer_text = request.form.get(f"question_{question.id}", "")
            answer = Answer.query.filter_by(submission_id=submission.id, question_id=question.id).first()
            if answer:
                answer.answer_text = answer_text
            else:
                answer = Answer(submission_id=submission.id, question_id=question.id, answer_text=answer_text)
                db.session.add(answer)
        db.session.commit()

        # Handle pagination buttons
        if request.form.get("next_page") == "next":
            return redirect(url_for("main.take_test", test_id=test.id, page=page+1, student_id=student_id))
        elif request.form.get("next_page") == "prev":
            return redirect(url_for("main.take_test", test_id=test.id, page=page-1, student_id=student_id))
        else:  # final submission
            return redirect("/tests")

    # Pre-fill answers for student
    student_id = request.args.get("student_id", type=int)
    answers_dict = {}
    if student_id:
        submission = Submission.query.filter_by(test_id=test.id, student_id=student_id).first()
        if submission:
            answers_dict = {a.question_id: a.answer_text for a in submission.answers}

    return render_template(
        "take_test.html",
        test=test,
        students=students,
        questions=questions,
        page=page,
        total=total,
        answers_dict=answers_dict,
        datetime=datetime,
        student_id=student_id
    )

@bp.route("/test/<int:test_id>/edit", methods=["GET", "POST"])
def edit_test(test_id):
    test = Test.query.get_or_404(test_id)
    teachers = User.query.filter_by(role="teacher").all()

    if request.method == "POST":
        test.title = request.form.get("title")
        test.teacher_id = int(request.form.get("teacher_id"))
        test.is_timed = bool(request.form.get("is_timed"))
        duration = request.form.get("duration")
        test.duration = int(duration) if duration else None
        db.session.commit()
        return redirect("/tests")

    return render_template("edit_test.html", test=test, teachers=teachers)


@bp.route("/test/<int:test_id>/delete", methods=["POST"])
def delete_test(test_id):
    test = Test.query.get_or_404(test_id)
    db.session.delete(test)
    db.session.commit()
    return redirect("/tests")


@bp.route("/test/<int:test_id>/submissions")
def view_submissions(test_id):
    test = Test.query.get_or_404(test_id)
    submissions = Submission.query.filter_by(test_id=test.id).all()
    return render_template("submissions.html", test=test, submissions=submissions)


@bp.route("/question/<int:question_id>/edit", methods=["GET", "POST"])
def edit_question(question_id):
    question = Question.query.get_or_404(question_id)

    if request.method == "POST":
        question.question_text = request.form.get("question_text")
        question.type = request.form.get("type", question.type)

        if question.type == "mcq":
            question.option_a = request.form.get("option_a")
            question.option_b = request.form.get("option_b")
            question.option_c = request.form.get("option_c")
            question.option_d = request.form.get("option_d")
            question.correct_answer = request.form.get("correct_answer")
        else:
            # Clear MCQ fields if switching back
            question.option_a = None
            question.option_b = None
            question.option_c = None
            question.option_d = None
            question.correct_answer = None

        db.session.commit()
        return redirect(f"/test/{question.test_id}/edit")

    return render_template("edit_question.html", question=question)


@bp.route("/question/<int:question_id>/delete", methods=["POST"])
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    test_id = question.test_id
    db.session.delete(question)
    db.session.commit()
    return redirect(f"/test/{test_id}/edit")


# -----------------
# Grading & Results
# -----------------
@bp.route("/submission/<int:submission_id>/grade", methods=["GET", "POST"])
def grade_submission(submission_id):
    submission = Submission.query.get_or_404(submission_id)
    teachers = User.query.filter_by(role="teacher").all()

    if request.method == "POST":
        submission.marks = int(request.form.get("marks"))
        submission.graded_by = int(request.form.get("teacher_id"))
        db.session.commit()
        return redirect(f"/test/{submission.test_id}/submissions")

    return render_template("grade_submission.html", submission=submission, teachers=teachers)


@bp.route("/student/<int:student_id>/results")
def student_results(student_id):
    student = User.query.get_or_404(student_id)
    submissions = Submission.query.filter_by(student_id=student.id).all()
    return render_template("student_results.html", student=student, submissions=submissions)


@bp.route("/tests/summary")
def tests_summary():
    tests = Test.query.all()
    tests_info = []
    for t in tests:
        student_count = Submission.query.filter_by(test_id=t.id).count()
        tests_info.append({
            "id": t.id,
            "title": t.title,
            "teacher": t.teacher.name if t.teacher else "N/A",
            "student_count": student_count
        })
    return render_template("tests_summary.html", tests=tests_info)


@bp.route("/test/<int:test_id>/summary")
def test_summary(test_id):
    test = Test.query.get_or_404(test_id)
    submissions = Submission.query.filter_by(test_id=test.id).all()
    return render_template("test_summary.html", test=test, submissions=submissions)