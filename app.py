from flask import Flask
from flask.ext.mongoengine import MongoEngine

# cria o  app
app = Flask(__name__)

# configura o app a partir do settings
app.config.from_object('settings')

# configura o banco
db = MongoEngine(app)

from ong.resources import ong_blueprint

# registra os blueprints
app.register_blueprint(ong_blueprint)
