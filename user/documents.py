import datetime
from app import db

class UserDocument(db.Document):
    name = db.StringField(required=True)
    email = db.StringField(required=True)
    password = db.StringField(required=True)
    createdAt = db.DateTimeField(default=datetime.datetime.now)

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'createdAt': self.createdAt.strftime("%Y-%m-%d %H:%M:%S"),
            'id': str(self.id)
        }
