from django.core.cache import cache
from products_creation.serializers import ProductSerializer
from .models import Product


def cache_update():
    """function to update the cache data in redis when something changed in db"""
    try:
        cache_key = "product_list"  
        cache.delete(cache_key)
        updated_data = Product.objects.all()
        serializer = ProductSerializer(updated_data, many=True)
        cache.set(cache_key, serializer.data, timeout=120) 
        print({"status":"Cache updated!!!"})
    except Exception as error:
        if error.args[0].lower().find("connection refused") != -1:
            print({"status":f"Cache is not updated. System faced this error: {error}"})