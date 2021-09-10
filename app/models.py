from app import db

class User(db.Model):
    login = db.Column(db.String, primary_key=True)
    password = db.Column(db.String(30), nullable=False)
    items = db.relationship('Item', backref='user', lazy=True)

    def __repr__(self):
        return f'User {self.login}'

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    owner_login = db.Column(db.String, db.ForeignKey('user.login'), nullable=False)

    def __repr__(self):
        return f'Item {self.name}'