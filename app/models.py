from app import app
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    feature_requests = db.relationship('FeatureRequest')

    def __repr__(self):
        return '<Client %r>' % self.name

    __str__ = __repr__

    
class FeatureRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey(Client.id), nullable=False)
    client_priority = db.Column(db.Integer)
    target_date = db.Column(db.String(25), nullable=False)
    product_area = db.Column(db.String(65), nullable=False)

    def from_dict(self, data):
        for field in ['title', 'description', 'client_id', 'client_priority', 'target_date', 'product_area']:
            if field in data:
                setattr(self, field, data[field])

    def __repr__(self):
        return '<FeatureRequest %r>' % self.title

    __str__ = __repr__

