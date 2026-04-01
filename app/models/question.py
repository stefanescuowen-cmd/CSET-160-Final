from app.extensions import db

class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey("tests.id"))
    question_text = db.Column(db.Text)
    type = db.Column(db.Enum('open', 'mcq'), default='open')  # now supports MCQ

    # MCQ-specific fields
    option_a = db.Column(db.String(255))
    option_b = db.Column(db.String(255))
    option_c = db.Column(db.String(255))
    option_d = db.Column(db.String(255))
    correct_answer = db.Column(db.String(1))  # 'A', 'B', 'C', or 'D'

    # Relationships
    test = db.relationship("Test", back_populates="questions")
    answers = db.relationship("Answer", back_populates="question", lazy=True)