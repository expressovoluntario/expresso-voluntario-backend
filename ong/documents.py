import mongoengine
from task.documents import TaskDocument
from app import db


class OngDocument(db.Document):

    name = db.StringField(required=True)
    description = db.StringField()
    tasks = db.ListField(db.ReferenceField(TaskDocument, reverse_delete_rule=mongoengine.PULL))

    indexes = {
        'tasks': tasks
    }

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': str(self.id)
        }