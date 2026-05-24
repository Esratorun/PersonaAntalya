from app import db
from datetime import datetime


class Place(db.Model):
    """Antalya'daki turistik mekanların tutulacağı tablo"""
    __tablename__ = 'places'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), index=True)

    # Konum bilgileri (Google Maps ve mesafe hesaplama için kritik)
    address = db.Column(db.String(255))
    district = db.Column(db.String(100), index=True)
    latitude = db.Column(db.Float, nullable=False, index=True)
    longitude = db.Column(db.Float, nullable=False, index=True)

    # Detay bilgileri
    image_url = db.Column(db.Text)
    rating = db.Column(db.Float, default=0.0)
    opening_hours = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    website = db.Column(db.String(255))
    entrance_fee = db.Column(db.Float)
    average_visit_time = db.Column(db.Integer)  # Dakika cinsinden (Rota hesaplaması için)
    best_time_to_visit = db.Column(db.String(100))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Place {self.name}>'