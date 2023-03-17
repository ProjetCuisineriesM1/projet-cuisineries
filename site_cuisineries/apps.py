from django.apps import AppConfig
from django.db.models.signals import post_migrate


class SiteCuisineriesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'site_cuisineries'
    verbose_name="Les Cuisineries"
    def ready(self):
        from .signals import populate_models
        post_migrate.connect(populate_models, sender=self)
