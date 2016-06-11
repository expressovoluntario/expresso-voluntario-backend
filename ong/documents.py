import datetime, json
import mongoengine
from flask.json import jsonify
from task.documents import TaskDocument
from app import db #Objeto do Flask Mongo-Engine


class OngDocument(db.Document):
    createdAt = db.DateTimeField(default=datetime.datetime.now)
    updatedAt = db.DateTimeField(default=datetime.datetime.now)
    name = db.StringField(required=True)
    description = db.StringField()
    purpose = db.StringField()
    phone1 = db.StringField()
    phone2 = db.StringField()
    email = db.StringField()
    site = db.StringField()
    address = db.DictField()
    addressNumber = db.StringField()
    logoUrl = db.StringField()
    tasks = db.ListField(db.ReferenceField(TaskDocument, reverse_delete_rule=mongoengine.PULL))

    indexes = {
        'tasks': tasks
    }

    def to_dict(self):
        return {
            'id': str(self.id),
            '_id': str(self.id),
            'createdAt': self.createdAt.strftime("%Y-%m-%d %H:%M:%S"),
            'updatedAt': self.updatedAt.strftime("%Y-%m-%d %H:%M:%S"),
            'name': self.name,
            'description': self.description,
            'purpose': self.purpose,
            'phone1': self.phone1,
            'phone2': self.phone2,
            'email': self.email,
            'site': self.site,
            'address': self.address,
            'addressNumber': self.addressNumber,
            'logoUrl': self.logoUrl,
            'tasks': json.dumps([t.to_dict() for t in self.tasks])
        }
