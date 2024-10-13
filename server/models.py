from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, CheckConstraint
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy




db = SQLAlchemy()

# Episodes Table
class Episode(db.Model, SerializerMixin):
    __tablename__ = "episodes"
    
    # serialize rules
    serialize_rules = ('-appearances.episode',)
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    
    # Relationship to Appearance model
    appearances = db.relationship('Appearance', back_populates='episode', cascade="all,delete-orphan")
    
    # Association to Guest
    guests = association_proxy('appearances', 'guest',
                               creator=lambda guest_obj: Appearance(guest=guest_obj))
    
    def __repr__(self):
        return f'<Episode {self.date} , Number of Episodes {self.number}>'
    
    
# Guests Table
class Guest(db.Model, SerializerMixin):
    __tablename__ = "guests"
    
    # serialize rules
    serialize_rules = ('-appearances.guest',)
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    occupation = db.Column(db.String, nullable=False)
    
    # Relationship to Appearances model
    appearances = db.relationship('Appearance', back_populates='guest', cascade="all,delete-orphan")
    
    
    # Association to Episode
    episodes = association_proxy('appearances', 'episode',
                               creator=lambda episode_obj: Appearance(episode=episode_obj))
    def __repr__(self):
        return f'<Guest {self.name} for {self.occupation}>'
    
    
# Appearances Table
class Appearance(db.Model, SerializerMixin):
    __tablename__ = "appearances"
    
    # serialize rules
    serialize_rules = ('-episode.appearances', '-guest.appearances')
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)
    
    # Relationship to Episode and Guest models
    episode = db.relationship('Episode', back_populates='appearances')
    guest = db.relationship('Guest', back_populates='appearances')
    
    # Validating rating column
    __table_args__ = (CheckConstraint('rating >= 1 AND rating <= 5', name='valid_rating'),)
    
    def __repr__(self):
        return f'<Appearance of {self.guest.name} in {self.episode.date} for {self.episode.number}>'