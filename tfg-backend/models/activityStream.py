from database import db

class ActivityStream(db.Model):
    __tablename__ = 'ActivityStream'
    activity_stream_id = db.Column(db.Integer, primary_key = True)
    activity_id = db.Column(db.Integer, db.ForeignKey('Activity.activity_id'))
    altitude = db.Column(db.Float)
    current_speed = db.Column(db.Float)
    timestamp = db.Column(db.Integer, nullable = False)
    heartrate = db.Column(db.Integer, nullable = False)
    grade = db.Column(db.Float)
    distance = db.Column(db.Float, nullable = False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)