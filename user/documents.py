import datetime
import mongoengine
from flask.ext.login import UserMixin
from app import db
from ong.documents import OngDocument

class UserDocument(db.Document, UserMixin):
    name = db.StringField(required=True)
    email = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    createdAt = db.DateTimeField(default=datetime.datetime.now)
    ong_id = db.ReferenceField(OngDocument, reverse_delete_rule=mongoengine.PULL)

    def get_id(self):
        return str(self.id)

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'createdAt': self.createdAt.strftime("%Y-%m-%d %H:%M:%S"),
            'id': self.get_id(),
            'ong_id': str(self.ong_id),
            'is_authenticated': self.is_authenticated
        }
