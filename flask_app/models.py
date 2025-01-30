from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150), nullable=True)  # 場所
    link = db.Column(db.String(300), nullable=True)      # リンク

    def __init__(self, name, location=None, link=None):
        self.name = name
        self.location = location
        self.link = link

    def __repr__(self):
        return f'<Item {self.name}>'