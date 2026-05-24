from app import db
from datetime import datetime


class SavedRoute(db.Model):
    """Kullanıcıların oluşturduğu ve kaydettiği gezi rotaları"""
    __tablename__ = 'saved_routes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    name = db.Column(db.String(255))
    description = db.Column(db.Text)

    # Rota sırası (Hangi mekanlara hangi sırayla gidilecek? Örn: "[1, 5, 3]" gibi)
    places_order = db.Column(db.Text)

    total_distance = db.Column(db.Float)  # Toplam kilometre
    estimated_time = db.Column(db.Integer)  # Toplam dakika

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<SavedRoute {self.name}>'