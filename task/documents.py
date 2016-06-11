import datetime, json
from app import db


class TaskDocument(db.Document):
    createdAt = db.DateTimeField(default=datetime.datetime.now)
    updatedAt = db.DateTimeField(default=datetime.datetime.now)
    title = db.StringField(required=True)
    description = db.StringField(required=True)
    status = db.StringField(default="Em aberto")
    tags = db.ListField(db.StringField())

    def to_dict(self):
        return {
            'id': str(self.id),
            '_id': str(self.id),
            'createdAt': self.createdAt.strftime("%Y-%m-%d %H:%M:%S"),
            'updatedAt': self.updatedAt.strftime("%Y-%m-%d %H:%M:%S"),
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'tags': self.tags
        }
