# Generated by Django 4.2.4 on 2023-09-08 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products_creation', '0003_remove_category_parent_category_parent_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
