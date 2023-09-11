from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """Serialize the data of categories and also create category and subcategory"""

    subcategories = serializers.SerializerMethodField()
    parent_category_name = serializers.CharField(source='parent_category.name', read_only=True)

    class Meta:
        model = Category
        fields = ["id", "parent_category_name", "parent_category", 'name', "subcategories"]

    def create(self, validated_data):
        parent_category_data = validated_data.pop('parent_category', None)
        name = validated_data['name']
        existing_category = Category.objects.filter(name=name).first()
        if existing_category:
            return existing_category

        if parent_category_data:
            parent_category, created = Category.objects.get_or_create(name=parent_category_data)
            category = Category.objects.create(parent_category=parent_category, **validated_data)
        else:
            category = Category.objects.create(**validated_data)
        return category

    def get_subcategories(self, obj):
        subcategories = obj.subcategories.all()
        serializer = CategorySerializer(subcategories, many=True)
        return serializer.data


class ProductSerializer(serializers.ModelSerializer):
    """Serialize the data of categories and also create, read, update and delete Product
      and subcategory and also updating the redis cache when data is newly created and updated"""

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        from products_creation.utils import cache_update
        category_data = validated_data.pop('category', [])
        product = Product.objects.create(**validated_data)
        for category_info in category_data:
            category_name = category_info.name  
            if category_name:
                category, created = Category.objects.get_or_create(name=category_name)
                product.category.add(category)
        cache_update()
        return product

    def update(self, instance, validated_data):
        from products_creation.utils import cache_update
        if 'category' in validated_data:
                new_categories = validated_data.pop('category')
                instance.category.set(new_categories) 
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        cache_update()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        category_ids = representation['category']
        category_names = []
        for category_id in category_ids:
            category = Category.objects.get(id=category_id)
            category_names.append(category.name)
        representation['category'] = category_names
        return representation