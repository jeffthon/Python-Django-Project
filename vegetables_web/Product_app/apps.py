from django.apps import AppConfig


class ProductAppConfig(AppConfig):
    name = 'Product_app'
    default_auto_field = 'django.db.models.BigAutoField'
    def ready(self):
        import Product_app.signals
