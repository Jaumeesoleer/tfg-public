from database import db
from sqlalchemy import CheckConstraint

class Activity(db.Model):
    __tablename__ = 'Activity'
    activity_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    external_id = db.Column(db.BigInteger, nullable = False, unique = True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))
    type = db.Column(db.String)
    title = db.Column(db.String)
    distance = db.Column(db.Float, nullable = False)
    mov_time = db.Column(db.Integer, nullable = False)
    elp_time = db.Column(db.Integer, nullable = False)
    workout_density = db.Column(db.Float, nullable = False)
    date = db.Column(db.DateTime)
    avg_heartrate = db.Column(db.Float, nullable = False)
    max_heartrate = db.Column(db.Integer, nullable = True)
    avg_pace = db.Column(db.Float, nullable = False)
    max_pace = db.Column(db.Float, nullable = False)
    positive_slope = db.Column(db.Integer, nullable = False)
    start_lat = db.Column(db.Numeric(precision=9, scale=6))
    start_lng = db.Column(db.Numeric(precision=9, scale=6))
    perceived_effort = db.Column(db.Integer)
    # Activity stream relationship
    activity_stream = db.relationship('ActivityStream', backref = 'Activity', lazy = True)
    prediction_log = db.relationship('PredictionLog', backref = 'Activity', lazy = True)
    __table_args__ = (
        CheckConstraint(
            "type IN ('Run', 'Walk', 'VirtualRun')", 
            name="check_activity_type"
    ),)