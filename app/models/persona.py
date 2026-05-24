from app import db
from datetime import datetime


class Persona(db.Model):
    """Gezgin personaları ve tema ayarlarını tutan tablo"""
    __tablename__ = 'personas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    emoji = db.Column(db.String(10))
    description = db.Column(db.Text)

    # CSS ve Tasarım için tema ayarları
    color = db.Column(db.String(7))
    secondary_color = db.Column(db.String(7))
    font_family = db.Column(db.String(100))
    characteristics = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Bu personaya ait üretilen hikayelerle bağlantı kuruyoruz
    contents = db.relationship('PersonaContent', backref='persona', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Persona {self.name}>'