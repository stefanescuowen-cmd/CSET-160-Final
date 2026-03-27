from app.extensions import db

class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey("tests.id"), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    type = db.Column(db.Enum("open", "mcq", name="question_types"), nullable=False)

    # Relationships
    options = db.relationship("Option", backref="question", lazy=True)
    answers = db.relationship("Answer", backref="question_rel", lazy=True)

    def __repr__(self):
        return f"<Question {self.id} ({self.type})>"