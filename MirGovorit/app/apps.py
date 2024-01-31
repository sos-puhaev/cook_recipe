from django.apps import AppConfig

class AppConfig(AppConfig):
    name = 'app'
    
class SaveProductConfig(AppConfig):
    name = 'app'
    default_auto_field = 'django.db.models.BigAutoField'
    
    def ready(self):
        import app.signals
