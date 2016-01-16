from app import db

class TaskDocument(db.Document):
    title = db.StringField()