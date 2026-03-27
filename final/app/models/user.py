from app.extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.Enum("student", "teacher", name="user_roles"), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    # Relationships
    tests = db.relationship("Test", backref="teacher", lazy=True)
    submissions = db.relationship("Submission", backref="student", foreign_keys="Submission.student_id", lazy=True)
    graded_submissions = db.relationship("Submission", backref="grader", foreign_keys="Submission.graded_by", lazy=True)

    def __repr__(self):
        return f"<User {self.name} ({self.role})>"