from rest_framework import serializers


from .models import Category, Product

# class SubCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['name']

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    parent_category_name = serializers.CharField(source='parent_category.name', read_only=True)

    class Meta:
        model = Category
        fields = ["id", "parent_category_name", "parent_category", 'name', "subcategories"]

    def create(self, validated_data):
        parent_category_data = validated_data.pop('parent_category', None)
        name = validated_data['name']

        # Check if a category with the same name exists
        existing_category = Category.objects.filter(name=name).first()
        
        if existing_category:
            # If the category already exists, return it
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
    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        from products_creation.signal_handler import cache_update
        category_data = validated_data.pop('category', [])
        product = Product.objects.create(**validated_data)
        for category_info in category_data:
            category_name = category_info.name  
            if category_name:
                category, created = Category.objects.get_or_create(name=category_name)
                product.category.add(category)
        cache_update()
        return product

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        category_ids = representation['category']
        category_names = []
        for category_id in category_ids:
            category = Category.objects.get(id=category_id)
            category_names.append(category.name)
        representation['category'] = category_names
        print(representation)
        return representation
    # def to_representation(self, instance):
    #     response =  super().to_representation(instance)
    #     response["category_data"] = CategorySerializer(instance.category).data
    #     return response
