from app.extensions import db

class Test(db.Model):
    __tablename__ = "tests"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    teacher_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    is_timed = db.Column(db.Boolean, default=False)
    duration = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationships
    teacher = db.relationship("User", back_populates="tests_created")
    questions = db.relationship("Question", back_populates="test", lazy=True)
    submissions = db.relationship("Submission", back_populates="test", lazy=True)