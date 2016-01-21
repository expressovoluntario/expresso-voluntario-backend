import bcrypt
import datetime
import mongoengine
from flask.ext.login import UserMixin
from app import db
from ong.documents import OngDocument


class UserDocument(db.Document, UserMixin):
    name = db.StringField(required=True)
    email = db.StringField(required=True, unique=True)
    _password = db.BinaryField(required=True, max_length=255)
    createdAt = db.DateTimeField(default=datetime.datetime.now)
    ong_id = db.ReferenceField(OngDocument, reverse_delete_rule=mongoengine.PULL)

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        try:
            password = kwargs['_password']
        except AttributeError:
            pass
        else:
            if not isinstance(password, bytes):
                self._password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def check_password(self, guessed_password):
        return bcrypt.hashpw(guessed_password.encode(), self.password) == self.password

    def get_id(self):
        return str(self.id)

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'createdAt': self.createdAt.strftime("%Y-%m-%d %H:%M:%S"),
            'id': self.get_id(),
            'ong_id': str(self.ong_id),
            'is_authenticated': self.is_authenticated
        }
