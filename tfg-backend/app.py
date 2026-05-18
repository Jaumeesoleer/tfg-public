from flask import Flask
from flask_cors import CORS
from config import Config
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate


import os

from database import db

def create_app():
        app = Flask(__name__)
        app.config.from_object(Config)
        db.init_app(app)
        jwt = JWTManager(app)

        from models.activity import Activity
        from models.activityStream import ActivityStream
        from models.predictionLog import PredictionLog
        from models.user import User 
        migrate = Migrate(app, db)


        # Vue connection
        # app.py dentro de create_app()
        CORS(app, 
            supports_credentials=True, 
            origins=[os.environ.get('FRONTEND_URL')],
            allow_headers=["Content-Type", "Authorization", "X-CSRF-TOKEN"],
            methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"])



        

        """
        with app.app_context():
            try:
                from models.activity import Activity
                from models.activityStream import ActivityStream
                from models.predictionLog import PredictionLog
                from models.user import User 
                db.create_all()
            except Exception as e:
                print(f"❌ Error creando tablas: {e}")
"""

        from routes.activity_routes import activity_bp
        from routes.auth_routes import user_bp
        from routes.upload_routes import upload_bp
        from routes.predict_routes import predict_bp
        from routes.support_routes import support_bp

        app.register_blueprint(activity_bp, url_prefix = '/api/activities')
        app.register_blueprint(user_bp, url_prefix = '/api/auth')
        app.register_blueprint(upload_bp, url_prefix = '/api/upload')
        app.register_blueprint(predict_bp, url_prefix = '/api/prediction')
        app.register_blueprint(support_bp, url_prefix = '/api/support')
        
        return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)