from flask_admin import  AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import FileUploadField
from wtforms import ValidationError
from flask_login import  current_user 
from werkzeug.utils import secure_filename
import os

def allowed_file_extensions(form, field):
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    if field.data is None:
        return
    filename = field.data.filename.lower()
    if not any(filename.endswith(ext) for ext in allowed_extensions):
        raise ValidationError('Invalid file extension. Only JPG, JPEG, WEBP and PNG files are allowed.')

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    
class AdminHistory(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    
    
class PackageModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    
    form_extra_fields = {
        'photo': FileUploadField('Photo', base_path='website/static', validators=[allowed_file_extensions])
    }

    def on_model_change(self, form, model, is_created):
        if form.photo.data:
            filename = secure_filename(form.photo.data.filename)
            file_path = os.path.join('/static', filename)
            form.photo.data.save(file_path)
            model.image_url = file_path
        else:
            model.image_url = model.image_url

        super().on_model_change(form, model, is_created)
