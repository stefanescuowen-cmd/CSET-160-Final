from app.extensions import db

class Answer(db.Model):
    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey("submissions.id"))
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"))
    answer_text = db.Column(db.Text)

    # Relationships
    submission = db.relationship("Submission", back_populates="answers")
    question = db.relationship("Question", back_populates="answers")