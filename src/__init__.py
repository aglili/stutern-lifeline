import flask,os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from src.database.config import db
from src.auth import auth
from flask_migrate import Migrate
from flask_cors import CORS
from src.user import user
from src.chat import chat
from src.reminder import reminder
load_dotenv()



def create_app(test_config=None):
    app = flask.Flask(__name__,instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.getenv('SECRET_KEY'),
            JWT_SECRET_KEY=os.getenv('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI'),
        )
    else:
        app.config.from_mapping(test_config)

    JWTManager(app)
    db.init_app(app)
    Migrate(app,db)
    CORS(app,resources={r"/*": {"origins": "*"}})
    app.register_blueprint(auth)
    app.register_blueprint(user)
    app.register_blueprint(chat)
    app.register_blueprint(reminder)

    return app



app = create_app()


        
