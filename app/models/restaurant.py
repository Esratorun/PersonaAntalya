from app import db
from datetime import datetime

class Restaurant(db.Model):
    """Antalya'daki restoranları ve beslenme filtrelerini tutan tablo"""
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    cuisine = db.Column(db.String(100))
    district = db.Column(db.String(100))
    address = db.Column(db.String(255))

    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.Text)
    rating = db.Column(db.Float)
    price_range = db.Column(db.String(50))

    # Eski tip boolean beslenme tercihleri (Hata vermemesi için şimdilik kalsın)
    is_vegan = db.Column(db.Boolean, default=False)
    is_vegetarian = db.Column(db.Boolean, default=False)
    is_gluten_free = db.Column(db.Boolean, default=False)

    opening_hours = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    website = db.Column(db.String(255))

    # ==========================================
    # YENİ EKLENEN SÜTUNLAR (DİNAMİK KONTROL İÇİN)
    # ==========================================
    diet_category = db.Column(db.String(50))                   # İŞTE HATAYI ÇÖZEN SÜTUN BURASI!
    price_level = db.Column(db.String(10), default="₺₺")       # Örn: ₺ (Ucuz), ₺₺ (Orta), ₺₺₺ (Pahalı)
    opening_time = db.Column(db.String(10), default="09:00")   # Açılış saati
    closing_time = db.Column(db.String(10), default="23:30")   # Kapanış saati

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Restaurant {self.name}>'