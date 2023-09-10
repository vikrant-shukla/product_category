from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from products_creation.serializers import ProductSerializer
from .models import Product

def cache_update():
    try:
        cache_key = "product_list"  
        cache.delete(cache_key)
        updated_data = Product.objects.all()
        serializer = ProductSerializer(updated_data, many=True)
        data = cache.set(cache_key, serializer.data, timeout=120) 
        cached_data = cache.get(cache_key)
        print({"status":f"Cache updated!!!{data}", "data" :f"{cached_data}"})
    except Exception as error:
        if error.args[0].lower().find("connection refused") != -1:
            print({"status":f"Cache is not updated. System faced this error: {error}"})

@receiver(post_save, sender=Product)
def update_cache_post(**kwargs):
    cache_update()

@receiver(post_delete, sender=Product)
def update_cache_delete(**kwargs):
    cache_update()
