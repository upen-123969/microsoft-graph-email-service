from flask import Flask
from .config import Config
from .extensions import mongo
from .routes.api import api_blueprint
from .tasks.scheduler import init_scheduler

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    mongo.init_app(app)
    
    # Register blueprints
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    # Initialize scheduler
    init_scheduler(app)
    
    return app