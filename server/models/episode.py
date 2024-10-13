from utilis import db
import datetime as dt

class Episode(db.Model):
    __tablename__ = 'episodes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False , default= dt.datetime.utcnow)
    number = db.Column(db.Integer, nullable=False)

    appearances = db.relationship('Appearance', back_populates='episode', cascade='all, delete-orphan')
  

    def __repr__(self):
        return f'<Episode {self.date}, {self.number}>'