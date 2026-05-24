from app import db
from datetime import datetime


class Review(db.Model):
    """Kullanıcıların mekanlara yaptığı yorumları ve verdiği puanları tutar"""
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)

    # Hangi kullanıcı yaptı?
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # Hangi mekana veya restorana yapıldı? (İkisinden biri dolu olacak)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id', ondelete='CASCADE'), nullable=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id', ondelete='CASCADE'), nullable=True)

    # Verilen Puan ve Yorum
    rating = db.Column(db.Integer, nullable=False)  # 1 ile 5 arası
    comment = db.Column(db.Text, nullable=True)

    # Ne zaman yapıldı?
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Yorumu kimin yaptığını kolayca çekmek için ilişki kuruyoruz
    user = db.relationship('User', backref=db.backref('reviews', lazy=True, cascade="all, delete-orphan"))