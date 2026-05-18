from database import db
from sqlalchemy.dialects.postgresql import JSONB

class ModelAnalysis(db.Model):
    __tablename__ = 'ModelAnalysis'
    analysis_id = db.Column(db.Integer, primary_key= True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))
    generated_at = db.Column(db.Date, server_default=db.func.now())
    model_version = db.Column(db.String, default='running_model_v1_may')
    ml_points = db.Column(JSONB)
    riegel_curve = db.Column(JSONB)
    user_bests = db.Column(JSONB)
    model_metrics = db.Column(JSONB)

    runs_used = db.Column(db.Integer, nullable = False)
    train_samples = db.Column(db.Integer, nullable = False)
    test_samples = db.Column(db.Integer, nullable = False)
    r2_avg = db.Column(db.Integer, nullable = False)
    mae_avg = db.Column(db.Integer, nullable = False)
    
