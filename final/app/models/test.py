from ..extensions import db

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)  # Capital S here
    teacher_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    is_timed = db.Column(db.Boolean, default=False)
    duration = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    teacher = db.relationship("User", backref="tests")
    questions = db.relationship("Question", backref="test", cascade="all, delete-orphan")