import datetime
from app import db


class TaskDocument(db.Document):
    createdAt = db.DateTimeField(default=datetime.datetime.now)
    updatedAt = db.DateTimeField(default=datetime.datetime.now)
    title = db.StringField(required=True)
    description = db.StringField(required=True)
    status = db.StringField()
    recurrence = db.BooleanField()
    tags = db.ListField(db.StringField()) #TODO: alterar para linha abaixo quando TagDocument estiver ok
    # tags = db.ListField(db.ReferenceField(TagDocument, reverse_delete_rule=mongoengine.PULL))

    def to_dict(self):
        return {
            'id': str(self.id),
            'createdAt': self.createdAt.strftime("%Y-%m-%d %H:%M:%S"),
            'updatedAt': self.updatedAt.strftime("%Y-%m-%d %H:%M:%S"),
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'recurrence': self.recurrence,
            'tags': self.tags #TODO: Isso aqui é assim mesmo?
        }
