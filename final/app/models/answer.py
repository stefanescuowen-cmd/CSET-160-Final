from app.extensions import db

class Answer(db.Model):
    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey("submissions.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    answer_text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Answer {self.id}>"