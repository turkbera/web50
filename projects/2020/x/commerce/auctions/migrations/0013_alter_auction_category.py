# Generated by Django 4.2.3 on 2023-07-17 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_alter_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='category',
            field=models.TextField(blank=True, default='Default Category'),
        ),
    ]
