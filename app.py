from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager
from flask.ext.cors import CORS

# cria o  app
app = Flask(__name__)

# configura o app a partir do settings
app.config.from_object('settings')

# configura cors
enable_cors = app.config.get("ENABLE_CORS", False)
if enable_cors:
    CORS(app, resources={
        r"/ong/*": {"origins": "*"},
        r"/user/*": {"origins": "*"},
        r"/task/*": {"origins": "*"}
    })

# configura login manager
login_manager = LoginManager()
login_manager.init_app(app)

# configura o banco
db = MongoEngine(app)

from ong.resources import ong_blueprint
from task.resources import task_blueprint
from user.resources import user_blueprint
from user.documents import UserDocument

# registra os blueprints
app.register_blueprint(ong_blueprint)
app.register_blueprint(task_blueprint)
app.register_blueprint(user_blueprint)


@login_manager.user_loader
def load_user(user_id):
    return UserDocument.objects.get(id=user_id)
