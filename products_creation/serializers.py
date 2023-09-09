from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'
        # depth  = 1

    def to_representation(self, instance):
        response =  super().to_representation(instance)
        # response['parent_category'] = Category.objects.filter(parent_category = response.get("parent_category"))
        return response
    
    def get_subcategories(self, obj):
        subcategories = Category.objects.filter(parent_category=obj)
        return CategorySerializer(subcategories, many=True).data


class ProductSerializer(serializers.ModelSerializer):
    # CategorySerializer = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
        
    def to_representation(self, instance):
        response =  super().to_representation(instance)
        response["category"] = CategorySerializer(instance.category).data
        return response