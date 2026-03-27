from app.extensions import db

class Submission(db.Model):
    __tablename__ = "submissions"

    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey("tests.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    marks = db.Column(db.Integer, nullable=True)
    graded_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    submitted_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    is_late = db.Column(db.Boolean, default=False)

    __table_args__ = (db.UniqueConstraint("test_id", "student_id", name="unique_test_student"),)

    # Relationships
    answers = db.relationship("Answer", backref="submission", lazy=True)

    def __repr__(self):
        return f"<Submission {self.id} for Test {self.test_id}>"