from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class User(db.Model):
    """Define user properties."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String(128))
    # buckelists = db.relationship('Bucketlist', backref='users',
    #                             cascade='all, delete')

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)
    def save(self):
        """Define """
        db.session.add(self)
        db.session.commit

class Bucketlist(db.Model):
    """Define buckelist properties."""
    __tablename__ = "bucketlists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_on = db.Column(db.DateTime, default=datetime.now())
    items = db.relationship('Item', backref='bucketlists',
                            cascade='all, delete')

    def save(self):
        """Save bucketlist object"""
        db.session.add(self)
        db.session.commit
        
    def delete(self):
        """Delete bucketlist object"""
        db.session.delete(self)
        db.session.commit

    def __repr__(self):
            return '<Bucketlist: {}>'.format(self.name)

class Item(db.Model):
    """Define item properties."""
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))
    created_on = db.Column(db.DateTime, default=datetime.now)
    
    
    def save(self):
        """Save item object."""
        db.session.add(self)
        db.session.commit

    def delete(self):
        """Delete item object """
        db.session.delete(self)
        db.session.commit

    def __repr__(self):
            return '<Item: {}>'.format(self.name)
