from app.extensions import db

class Option(db.Model):
    __tablename__ = "options"

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"))
    option_text = db.Column(db.Text)

    # Relationships
    question = db.relationship("Question", back_populates="options")