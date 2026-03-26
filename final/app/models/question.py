from app import db

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey("test.id"), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(10), nullable=False)