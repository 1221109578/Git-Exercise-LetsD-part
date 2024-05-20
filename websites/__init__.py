from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_admin import Admin

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
 
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Packages

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    from .admin import MyModelView, MyAdminIndexView, MyAdminPackageView
    adminview = Admin(app, index_view=MyAdminIndexView())
    adminview.add_view(MyModelView(User, db.session))
    adminview.add_view(MyAdminPackageView(Packages, db.session))

    return app

def create_database(app):
    if not path.exists('websites/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
