from flask_admin import  AdminIndexView
from flask_admin.contrib.sqla import ModelView
from wtforms import ValidationError
from flask_login import  current_user 
from werkzeug.utils import secure_filename
import os

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    
class MyAdminPackageView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

class AdminHistory(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin