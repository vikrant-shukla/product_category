from django.apps import AppConfig


class ProductsCreationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products_creation'

    def ready(self):
        import products_creation.signal_handler