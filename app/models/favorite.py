from app import db
from datetime import datetime


class Favorite(db.Model):
    """Kullanıcıların favori mekanları ve restoranları"""
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    # Hangi kullanıcı ekledi?
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # Neyi favoriye ekledi? (Mekan mı, restoran mı?)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id', ondelete='CASCADE'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id', ondelete='CASCADE'))

    favorite_type = db.Column(db.String(50))  # 'place' (mekan) veya 'restaurant' (restoran) olacak

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Favorite User:{self.user_id} Type:{self.favorite_type}>'