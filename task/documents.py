import datetime
from app import db


class TaskDocument(db.Document):
    createdAt = db.DateTimeField(default=datetime.datetime.now)
    title = db.StringField(required=True)
    description = db.StringField(required=True)

    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'id': str(self.id)
        }
