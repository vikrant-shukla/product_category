from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent_category = models.ForeignKey('self', null=True, blank=True, related_name='subcategories', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField(null=True, blank=False)
    category = models.ManyToManyField(Category, related_name='products')

    def __str__(self):
        return self.name