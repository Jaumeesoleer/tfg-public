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
        CORS(app, resources={r"/api/*": {"origins": "https://tfg-public.vercel.app"}}, supports_credentials=True)

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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)