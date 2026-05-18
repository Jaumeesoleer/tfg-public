from database import db
from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import date

class User(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique = True, nullable = False)
    name = db.Column(db.String, nullable = False)
    surname = db.Column(db.String, nullable = False)
    birthdate = db.Column(db.Date, nullable = False)
    email = db.Column(db.String, unique = True, nullable = False)
    password_hash = db.Column(db.String)
    weight = db.Column(db.Float, nullable = False)
    max_hr = db.Column(db.Integer)
    rest_hr = db.Column(db.Integer, default=60)
    registration_date = db.Column(db.DateTime, server_default = db.func.now())
    last_edit = db.Column(db.DateTime, server_default = db.func.now())
    gender = db.Column(db.String, nullable=False)
    nickname = db.Column(db.String, nullable=False)
    custom_zones = db.Column(db.JSON)
    profile_image = db.Column(db.String)
    obj_distance = db.Column(db.Integer)
    level = db.Column(db.String)
    # Activity relationship
    activities = db.relationship('Activity', backref = 'User', lazy = True)
    prediction_log = db.relationship('PredictionLog', backref = 'User', lazy = True)
    model_analysis = db.relationship('ModelAnalysis', backref = 'User', lazy = True)

    @staticmethod
    def is_password_strong(password):
        if len(password) < 12:
            return False, "Password must be at least 12 characters long."
        if not re.search(r"[A-Z]", password):
            return False, "Password must contain uppercase letters."
        if not re.search(r"[a-z]", password):
            return False, "Password must contain lowercase letters."
        if not re.search(r"\d", password):
            return False, "Password must contain numbers."
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Password must contain special characters."
        return True, "Strong password."
    
    @property
    def heart_rate_zones(self):
        if self.custom_zones: return self.custom_zones
        # Fallbacks por si no hay datos definidos
        max_f = self.max_hr if self.max_hr else (220 - self._calculate_age())
        rest_f = self.rest_hr or 60
        hr_reserve = max_f - rest_f

        # Porcentajes estándar de zonas (Z1 a Z5)
        intensities = [(0.5, 0.6), (0.6, 0.7), (0.7, 0.8), (0.8, 0.9), (0.9, 1.0)]
        
        zones = []
        for i, (low, high) in enumerate(intensities):
            zones.append({
                "zone": i + 1,
                "min": round(rest_f + (hr_reserve * low)),
                "max": round(rest_f + (hr_reserve * high))
            })
        return zones

    def _calculate_age(self):
        today = date.today()
        return today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='scrypt')
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

