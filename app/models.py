from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    items = db.relationship('Item', backref='user', lazy=True)

    def __repr__(self):
        return f'User {self.login}'

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    owner_login = db.Column(db.String, db.ForeignKey('user.login'), nullable=False)

    def __repr__(self):
        return f'Item {self.name}'
    
class Link(db.Model):
    _from = db.Column(db.String, nullable=False)
    _to = db.Column(db.String, nullable=False)
    _text = db.Column(db.String, primary_key=True)

    def __repr__(self):
        return f'Link {self._text} from {self._from} to {self._to}'