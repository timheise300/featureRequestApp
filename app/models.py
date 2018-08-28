from app import db

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clientName = db.Column(db.String(64), nullable=False)
    featureRequests = db.relationship('FeatureRequest', backref='clientName', lazy='dynamic')

    def __repr__(self):
        return '<Client {}>'.format(self.clientName)

class FeatureRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True, nullable=False)
    description = db.Column(db.String(1000))
    clientPriority = db.Column(db.Integer, unique=True, nullable=False)
    targetDate = db.Column(db.Date, nullable=False)
    productArea = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<FeatureRequest {}>'.format(self.title)
