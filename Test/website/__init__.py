from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_admin import Admin
from flask_socketio import SocketIO, emit

db = SQLAlchemy()
DB_NAME = "database.db"
socketio = SocketIO()

def create_app():
    # Initialize Flask and SocketIO
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'pew'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    socketio.init_app(app) 

    from .client import client
    from .auth import auth
    from .chat import chat_function

    # Include or register into this package for the other python files
    app.register_blueprint(client, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(chat_function, url_prefix='/')

    from .models import User, TravelPackage, Booking
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    from .admin import MyModelView,MyAdminIndexView, PackageModelView, AdminHistory
    # Creates admin's modelview
    adminview = Admin(app, index_view=MyAdminIndexView())
    adminview.add_view(MyModelView(User, db.session))
    adminview.add_view(PackageModelView(TravelPackage, db.session))
    adminview.add_view(AdminHistory(Booking, db.session))

    return app

# Create database
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
