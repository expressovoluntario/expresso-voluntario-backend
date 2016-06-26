from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager
from flask.ext.cors import CORS

# Cria um app Flask
app = Flask(__name__)

# Configura o app a partir do arquivo de configurações (settings.py)
app.config.from_object('settings')

# Configura o suporte ao CORS (Cross-Origin Resource Sharing)
enable_cors = app.config.get("ENABLE_CORS", False)
if enable_cors:
    CORS(app, resources={
        r"/ong/*": {"origins": "*"},
        r"/user/*": {"origins": "*"},
        r"/task/*": {"origins": "*"},
        r"/search/*": {"origins": "*"}
    })

# Configura o LoginManager do FlaskLogin
login_manager = LoginManager()
login_manager.init_app(app)

# Configura o banco de dados
db = MongoEngine(app)

from ong.resources import ong_blueprint
from task.resources import task_blueprint
from user.resources import user_blueprint
from search.resources import search_blueprint
from user.documents import UserDocument

# Registra os blueprints
app.register_blueprint(ong_blueprint)
app.register_blueprint(task_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(search_blueprint)


@login_manager.user_loader
def load_user(user_id):
    return UserDocument.objects.get(id=user_id)
