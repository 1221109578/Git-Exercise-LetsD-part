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

    from.models import User, Seasons, TravelPackage, Booking

    with app.app_context():
        db.create_all()
        Events() # Insert data after creating the tables
        

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    from .admin import MyModelView, MyAdminIndexView, MyAdminPackageView, AdminHistory
    adminview = Admin(app, index_view=MyAdminIndexView())
    adminview.add_view(MyModelView(User, db.session))
    adminview.add_view(MyModelView(Seasons, db.session))
    adminview.add_view(MyAdminPackageView(TravelPackage, db.session))
    adminview.add_view(AdminHistory(Booking, db.session))

    return app

def create_database(app):
    if not path.exists('websites/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

#Inserting data into table Seasons
def Events():
    from .models import Seasons

    if Seasons.query.first() is None:
    # List of eventsw
        main_events = [
            {"event_name": "Jorvik Viking Festivals", "country": "United Kingdom", "date": "20-27 February 2024", "event_id": "1"},
            {"event_name": "Coastival Arts Festival", "country": "United Kingdom", "date": "22-24 February 2024", "event_id": "1"},
            {"event_name": "St. Moritz Gourmet Festival", "country": "Switzerland", "date": "29/1/2024 to 3/2/2024", "event_id": "1"},
            {"event_name": "Alte Silvester", "country": "Switzerland", "date": "30/12/2023 and 13/1/2024", "event_id": "1"},
            {"event_name": "Tollwood Winter Festival", "country": "Germany", "date": "November to December", "event_id": "1"},
            {"event_name": "Epiphany", "country": "Germany", "date": "6/1/2024", "event_id": "1"},
            {"event_name": "Reykjavík Winter Lights Festival", "country": "Iceland", "date": "February 2024", "event_id": "1"},
            {"event_name": "Dark Music Days", "country": "Iceland", "date": "January 2024", "event_id": "1"},
            {"event_name": "Trojan Festival", "country": "Turkey", "date": "August 2024", "event_id": "2"},
            {"event_name": "Stonehenge Summer Solstice", "country": "United Kingdom", "date": "18-22 June 2024", "event_id": "2"},
            {"event_name": "Reykjavik Culture Night", "country": "Iceland", "date": "3rd week of August 2024", "event_id": "2"},
            {"event_name": "Den Rhein in Flammen", "country": "Germany", "date": "August 2024", "event_id": "2"},
            {"event_name": "Kieler Woche", "country": "Germany", "date": "May 2024", "event_id": "3"},
            {"event_name": "Reykjavik Arts Festival", "country": "Iceland", "date": "May 2024", "event_id": "3"},
            {"event_name": "Finale Nationale de la Race d'Hérens", "country": "Switzerland", "date": "May 2024", "event_id": "3"},
            {"event_name": "Liverpool Sound City", "country": "United Kingdom", "date": "4-5 May 2024", "event_id": "3"},
            {"event_name": "Cappadox Festival", "country": "Turkey", "date": "May 2024", "event_id": "3"},
            {"event_name": "Longleat Festival of Light", "country": "United Kingdom", "date": "11/11/2023 to 3/1/2024", "event_id": "4"},
            {"event_name": "Chestnut Festival", "country": "Switzerland", "date": "mid October 2024", "event_id": "4"},
            {"event_name": "Imagine Peace Tower", "country": "Iceland", "date": "9/10/2024 to 8/12/2024", "event_id": "4"},
            {"event_name": "Berlin Festival of Lights", "country": "Germany", "date": "October 2024", "event_id": "4"}
        ]

        for event_data in main_events:
            event1 = Seasons(**event_data)
            db.session.add(event1)
            
    else:
        print("Data already exists, skipping insertion.")

    db.session.commit()