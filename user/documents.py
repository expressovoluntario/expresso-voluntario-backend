import datetime
import mongoengine
from app import db
from ong.documents import OngDocument

class UserDocument(db.Document):
    name = db.StringField(required=True)
    email = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    createdAt = db.DateTimeField(default=datetime.datetime.now)
    ongId = db.ReferenceField(OngDocument, reverse_delete_rule=mongoengine.PULL)

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'createdAt': self.createdAt.strftime("%Y-%m-%d %H:%M:%S"),
            'id': str(self.id),
            'ongId': str(self.ongId),
        }
