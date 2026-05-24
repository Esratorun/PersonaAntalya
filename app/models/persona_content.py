from app import db
from datetime import datetime


class PersonaContent(db.Model):
    """Mekanlar için yapay zeka tarafından üretilen persona bazlı hikayeler"""
    __tablename__ = 'persona_contents'

    id = db.Column(db.Integer, primary_key=True)
    # Hangi mekan ve hangi persona için üretildiğini bağlıyoruz
    place_id = db.Column(db.Integer, db.ForeignKey('places.id', ondelete='CASCADE'), nullable=False)
    persona_id = db.Column(db.Integer, db.ForeignKey('personas.id', ondelete='CASCADE'), nullable=False)

    title = db.Column(db.String(255))
    story = db.Column(db.Text)
    interesting_facts = db.Column(db.Text)
    recommendations = db.Column(db.Text)

    ai_generated = db.Column(db.Boolean, default=True)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Aynı mekana aynı personadan iki kere içerik üretilmesini engelliyoruz
    __table_args__ = (db.UniqueConstraint('place_id', 'persona_id', name='_place_persona_uc'),)

    def __repr__(self):
        return f'<PersonaContent Place:{self.place_id} Persona:{self.persona_id}>'