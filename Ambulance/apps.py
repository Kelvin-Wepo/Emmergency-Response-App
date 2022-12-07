from django.apps import AppConfig


class AmbulanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Ambulance'
    
    # handles the signals that we will be using to create the profiles.
    def ready(self):
        import Ambulance.signals 

   