from utilis import db
from sqlalchemy.orm import validates
class Appearance(db.Model):
    __tablename__ = 'appearances'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)

    episode = db.relationship('Episode', back_populates='appearance')
    guest = db.relationship('Guest', back_populates='appearance')

    @validates('rating')
    def validate_rating(self, key, rating):
        if rating < 1 or rating > 5:
            raise ValueError('Rating must be between 1 and 5 (inclusive).')
        return rating
    
    def __repr__(self):
        return f'<Appearance id={self.id}, rating={self.rating}, episode_id={self.episode_id}, guest_id={self.guest_id}>'