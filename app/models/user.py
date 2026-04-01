from app.extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    role = db.Column(db.Enum("student", "teacher"))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationships
    submissions = db.relationship("Submission", back_populates="student", foreign_keys="Submission.student_id")
    graded_submissions = db.relationship("Submission", back_populates="grader", foreign_keys="Submission.graded_by")
    tests_created = db.relationship("Test", back_populates="teacher")