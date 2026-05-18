from database import db

class PredictionLog(db.Model):
    __tablename__ = 'PredictionLog'
    prediction_log_id = db.Column(db.Integer, primary_key= True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))
    last_activity_id = db.Column(db.Integer, db.ForeignKey('Activity.activity_id'))
    created_at = db.Column(db.Date, server_default=db.func.now())

    pred_5k = db.Column(db.Integer, nullable = False)
    pred_10k = db.Column(db.Integer, nullable = False)
    pred_21k = db.Column(db.Integer, nullable = False)
    pred_42k = db.Column(db.Integer, nullable = False)

    mae = db.Column(db.Float)
    model_version = db.Column(db.String, default='running_model_v1_may')

    