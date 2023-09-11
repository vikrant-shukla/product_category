from django.db.models.signals import  post_delete
from django.dispatch import receiver
from products_creation.utils import cache_update
from .models import Product

@receiver(post_delete, sender=Product)
def update_cache_delete(**kwargs):
    """Signal to Update the redis cache when something is deleted from db"""
    
    cache_update()
