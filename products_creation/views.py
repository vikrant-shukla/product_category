from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework import generics
from django.core.cache import cache
from rest_framework.response import Response

class CategoryList(generics.ListCreateAPIView):
    """Api to get and post the data of categories from/to database"""

    queryset = Category.objects.filter(parent_category=None)
    serializer_class = CategorySerializer

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    """Api to update and delete the data of categories table"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductList(generics.ListCreateAPIView):
    """Api to get and post the data of products from/to database and 
    caching the data of table in redis and fetching the data from both redis cache and database"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        try:
            flag = False
            cache_key = 'product_list'
            cached_data = cache.get(cache_key)
            cache_disable_flag = request.data.get("cache") if request.data.get("cache") else False
            if cached_data and not cache_disable_flag:
                return Response({"data_from_cache ":cached_data})
        except Exception as error:
            print(error)
            if error.args[0].lower().find("connection refused") != -1:
                flag = True
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = {}
        if flag == False and cached_data == None :
            cache.set(cache_key, serializer.data, timeout=120)
        else:
            data["Something went in this"] = "Maybe Redis server is not working so data fetching from db or cache is disabled \
or redis cache exceeds its time limit"
        if not  data.get("Something went in this"):
            data["status"] = "Showing from db either because the cache is timed out or this is the first call"
        data["data_from_db"]= serializer.data
        return Response(data)

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    """Api to update and delete the data of Products table """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    
