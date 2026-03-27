from app.extensions import db

class Test(db.Model):
    __tablename__ = "tests"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    is_timed = db.Column(db.Boolean, default=False)
    duration = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    # Relationships
    questions = db.relationship("Question", backref="test", lazy=True)
    submissions = db.relationship("Submission", backref="test_rel", lazy=True)

    def __repr__(self):
        return f"<Test {self.title}>"