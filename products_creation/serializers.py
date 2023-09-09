from rest_framework import serializers
from .models import Category, Product

# class SubCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['name']

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    # parent_category = SubCategorySerializer(read_only =True)

    class Meta:
        model = Category
        fields = ["id","parent_category",'name', "subcategories"]
        # fields = ["id",'name',"parent_category", "subcategories"]

    # def get_parent_category(self, obj):
    #     if obj.parent_category is not None:
    #         return CategorySerializer(obj.parent_category).data
    #     else:
    #         return None
 
    def get_subcategories(self, obj):
        subcategories = Category.objects.filter(parent_category=obj)
        return CategorySerializer(subcategories, many=True).data


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
        
    def to_representation(self, instance):
        response =  super().to_representation(instance)
        response["category"] = CategorySerializer(instance.category).data
        return response