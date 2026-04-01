from app.extensions import db

class Submission(db.Model):
    __tablename__ = "submissions"

    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey("tests.id"))
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    marks = db.Column(db.Integer)
    graded_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    submitted_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    is_late = db.Column(db.Boolean, default=False)

    # Relationships
    test = db.relationship("Test", back_populates="submissions")
    student = db.relationship("User", back_populates="submissions", foreign_keys=[student_id])
    grader = db.relationship("User", back_populates="graded_submissions", foreign_keys=[graded_by])
    answers = db.relationship("Answer", back_populates="submission", lazy=True)