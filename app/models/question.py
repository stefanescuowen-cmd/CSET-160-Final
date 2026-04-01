from app.extensions import db

class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey("tests.id"))
    question_text = db.Column(db.Text)
    type = db.Column(db.Enum('open'), default='open')  # only open questions

    # Relationships
    test = db.relationship("Test", back_populates="questions")
    answers = db.relationship("Answer", back_populates="question", lazy=True)