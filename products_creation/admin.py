from django.contrib import admin

from products_creation.models import Category, Product

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)