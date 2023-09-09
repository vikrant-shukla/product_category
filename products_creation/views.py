from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework import generics
from rest_framework.views import APIView
from django.core.cache import cache
from rest_framework.response import Response

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.filter(parent_category=None)
    serializer_class = CategorySerializer

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        try:
            flag = False
            cache_key = 'product_list'
            cached_data = cache.get(cache_key)
            if cached_data:
                return Response({"data_from_cache ":cached_data})
        except Exception as error:
            if error.args[0].lower().find("connection refused") != -1:
                flag = True
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = {}
        if flag == False and cached_data == None :
            cache.set(cache_key, serializer.data, timeout=120)
        else:
            data["error_message"] = "Maybe Redis server is not working so data fetching from db"
        data["data_from_db"]= serializer.data
        return Response(data)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    
