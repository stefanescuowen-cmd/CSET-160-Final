from ..extensions import db

class Test(db.Model):
    __tablename__ = 'tests'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 'users', not 'user'
    is_timed = db.Column(db.Boolean, default=False)
    duration = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())