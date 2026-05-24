from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()

login_manager.login_view = 'auth.login'
login_manager.login_message = "Lütfen bu sayfayı görmek için giriş yapın."
login_manager.login_message_category = "danger"


def create_app():
    app = Flask(__name__)

    # Hafıza kaybını önlemek için ayarları buraya sabitliyoruz
    app.config['SECRET_KEY'] = 'persona-cok-gizli-anahtar-123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///personaantalya.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        # Veritabanının modeli tanıması için çağırıyoruz
        from app.models.user import User

        # Rotaları kaydediyoruz
        from app.routes.main import main_bp
        from app.routes.auth import auth_bp
        from app.routes.api import api_bp  # YENİ EKLENDİ

        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(api_bp)  # YENİ EKLENDİ

        # Tabloları oluşturuyoruz
        db.create_all()

    return app